import io
import json
import re
from pathlib import Path
from typing import Any, Iterable


class JSONC:
    _surrogate_pair_re = re.compile(
        r"\\u(d[89ab][0-9a-fA-F]{2})\\u(d[cdef][0-9a-fA-F]{2})",
        re.IGNORECASE,
    )
    _single_esc_re = re.compile(r"\\u([0-9a-fA-F]{4})")
    _trailing_commas_re = re.compile(r",(\s*[\]}])")

    # =========================
    # Public API
    # =========================

    def load(self, path: Path | str) -> Any:
        path = Path(path)

        if not path.exists():
            return {}

        raw = path.read_text(encoding="utf-8")
        if not raw.strip():
            return {}

        clean = self._preprocess(raw)

        try:
            data = json.loads(clean)
        except json.JSONDecodeError as e:
            snippet = self._format_error_snippet(clean, e.lineno, e.colno, context=2)
            hints = self._diagnose_json_error(clean, e.lineno, e.colno, e.msg)
            raise JsoncParseError(path, e.lineno, e.colno, e.msg, snippet, hints) from e

        return self._decode_u_escapes_any(data)

    def loads(self, content: str) -> Any:
        if not content.strip():
            return {}

        clean = self._preprocess(content)
        data = json.loads(clean)
        return self._decode_u_escapes_any(data)

    def dump(
        self,
        data: Any,
        path: Path | str,
        *,
        indent: int = 2,
        ensure_ascii: bool = False,
    ) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            self.dumps(data, indent=indent, ensure_ascii=ensure_ascii),
            encoding="utf-8",
        )

    def dumps(
        self,
        data: Any,
        *,
        indent: int = 2,
        ensure_ascii: bool = False,
    ) -> str:
        return json.dumps(
            data,
            indent=indent,
            ensure_ascii=ensure_ascii,
            default=self._json_default,
        )

    # aliases
    def read(self, path: Path | str) -> dict[str, Any]:
        data = self.load(path)
        return data if isinstance(data, dict) else {}

    def write(
        self,
        path: Path | str,
        data: dict[str, Any],
        *,
        indent: int = 2,
    ) -> None:
        self.dump(data, path, indent=indent)

    def get_data(self, path: Path | str) -> dict[str, Any]:
        data = self.load(path)
        return data if isinstance(data, dict) else {}

    def get_path(
        self,
        path: Path | str,
        keypath: str,
        default: Any = None,
    ) -> tuple[Any, bool]:
        data = self.get_data(path)
        return self._get_by_path(data, keypath.split("."), default)

    def update(self, path: Path | str, keypath: str, new_value: Any) -> bool:
        path = Path(path)
        if path.exists():
            text = path.read_text(encoding="utf-8")
            span = self._find_value_span_jsonc(text, keypath.split("."))
            if span is not None:
                v_start, v_end = span
                serialized = self._serialize_json_literal(new_value)
                new_text = text[:v_start] + serialized + text[v_end:]
                if new_text != text:
                    path.write_text(new_text, encoding="utf-8")
                    return True
                return False

        data = self.get_data(path)
        changed = self._set_by_path(data, keypath.split("."), new_value)
        if changed:
            self.write(path, data)
        return changed

    def append(self, path: Path | str, keypath: str, value: Any) -> bool:
        path = Path(path)

        if path.exists():
            text = path.read_text(encoding="utf-8")
            span = self._find_value_span_jsonc(text, keypath.split("."))
            if span is not None:
                start, end = span
                arr_start = self._skip_ws_and_comments(text, start)
                if arr_start < len(text) and text[arr_start] == "[":
                    serialized = self._serialize_json_literal(value)
                    new_text = self._append_into_array_literal(
                        text, arr_start, end, serialized
                    )
                    if new_text != text:
                        path.write_text(new_text, encoding="utf-8")
                        return True
                    return False

        data = self.get_data(path)
        changed = self._append_by_path(data, keypath.split("."), value)
        if changed:
            self.write(path, data)
        return changed

    def length(self, data: dict[str, Any]) -> int:
        return len(data)

    # =========================
    # Preprocess / decode
    # =========================

    def _preprocess(self, raw: str) -> str:
        clean = self._strip_comments(raw)
        clean = self._remove_trailing_commas(clean)
        return clean

    def _strip_comments(self, raw: str) -> str:
        output = io.StringIO()
        inside_str = False
        escaped = False

        for line in raw.splitlines():
            new_line: list[str] = []
            i = 0

            while i < len(line):
                ch = line[i]

                if inside_str:
                    new_line.append(ch)
                    if escaped:
                        escaped = False
                    elif ch == "\\":
                        escaped = True
                    elif ch == '"':
                        inside_str = False
                    i += 1
                    continue

                if ch == '"':
                    inside_str = True
                    new_line.append(ch)
                    i += 1
                    continue

                if ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
                    break

                new_line.append(ch)
                i += 1

            output.write("".join(new_line) + "\n")

        return output.getvalue()

    def _remove_trailing_commas(self, s: str) -> str:
        return self._trailing_commas_re.sub(r"\1", s)

    def _decode_u_escapes_str(self, s: str) -> str:
        def repl_pair(match: re.Match[str]) -> str:
            hi = int(match.group(1), 16)
            lo = int(match.group(2), 16)
            cp = 0x10000 + ((hi - 0xD800) << 10) + (lo - 0xDC00)
            return chr(cp)

        def repl_single(match: re.Match[str]) -> str:
            return chr(int(match.group(1), 16))

        if "\\u" not in s:
            return s

        s = self._surrogate_pair_re.sub(repl_pair, s)
        s = self._single_esc_re.sub(repl_single, s)
        return s

    def _decode_u_escapes_any(self, obj: Any) -> Any:
        if isinstance(obj, str):
            return self._decode_u_escapes_str(obj)
        if isinstance(obj, list):
            return [self._decode_u_escapes_any(item) for item in obj]
        if isinstance(obj, dict):
            return {
                key: self._decode_u_escapes_any(value) for key, value in obj.items()
            }
        return obj

    # =========================
    # Dict path helpers
    # =========================

    def _get_by_path(
        self,
        data: dict[str, Any],
        parts: Iterable[str],
        default: Any = None,
    ) -> tuple[Any, bool]:
        current: Any = data
        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return default, False
            current = current[part]
        return current, True

    def _set_by_path(
        self,
        data: dict[str, Any],
        parts: list[str],
        value: Any,
    ) -> bool:
        current: dict[str, Any] = data
        for part in parts[:-1]:
            next_value = current.get(part)
            if not isinstance(next_value, dict):
                next_value = {}
                current[part] = next_value
            current = next_value

        last = parts[-1]
        if current.get(last) == value:
            return False

        current[last] = value
        return True

    def _append_by_path(
        self,
        data: dict[str, Any],
        parts: list[str],
        value: Any,
    ) -> bool:
        current: dict[str, Any] = data
        for part in parts[:-1]:
            next_value = current.get(part)
            if not isinstance(next_value, dict):
                next_value = {}
                current[part] = next_value
            current = next_value

        last = parts[-1]
        arr = current.get(last)

        if arr is None:
            current[last] = [value]
            return True

        if not isinstance(arr, list):
            current[last] = [arr, value]
            return True

        arr.append(value)
        return True

    # =========================
    # Serialization helpers
    # =========================

    def _json_default(self, obj: Any) -> str:
        if isinstance(obj, Path):
            return str(obj)
        return str(obj)

    def _serialize_json_literal(self, value: Any) -> str:
        if value is True:
            return "true"
        if value is False:
            return "false"
        if value is None:
            return "null"
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))

    # =========================
    # In-place JSONC editing helpers
    # =========================

    def _find_value_span_jsonc(
        self,
        s: str,
        segs: list[str],
    ) -> tuple[int, int] | None:
        n = len(s)

        def skip_ws_and_comments(j: int) -> int:
            return self._skip_ws_and_comments(s, j)

        def scan_string(j: int) -> int:
            assert s[j] == '"'
            j += 1
            escaped = False

            while j < n:
                ch = s[j]
                if escaped:
                    escaped = False
                    j += 1
                    continue
                if ch == "\\":
                    escaped = True
                    j += 1
                    continue
                if ch == '"':
                    return j + 1
                j += 1

            return j

        def read_string_value(j: int) -> tuple[str, int]:
            j0 = j
            j = scan_string(j)
            raw = s[j0:j]

            try:
                value = json.loads(raw)
            except Exception:
                value = raw.strip('"')

            return value, j

        def find_value_end(j: int) -> int:
            j = skip_ws_and_comments(j)
            if j >= n:
                return j

            ch = s[j]
            if ch == '"':
                return scan_string(j)

            if ch == "{":
                return scan_balanced(j, "{", "}")

            if ch == "[":
                return scan_balanced(j, "[", "]")

            k = j
            while k < n and s[k] not in ",}\n]":
                k += 1
            return k

        def scan_balanced(start: int, opener: str, closer: str) -> int:
            depth = 0
            k = start
            in_str = False
            escaped = False
            in_line_comment = False

            while k < n:
                c = s[k]

                if in_line_comment:
                    if c == "\n":
                        in_line_comment = False
                    k += 1
                    continue

                if in_str:
                    if escaped:
                        escaped = False
                    elif c == "\\":
                        escaped = True
                    elif c == '"':
                        in_str = False
                    k += 1
                    continue

                if c == "/" and k + 1 < n and s[k + 1] == "/":
                    in_line_comment = True
                    k += 2
                    continue

                if c == '"':
                    in_str = True
                    k += 1
                    continue

                if c == opener:
                    depth += 1
                elif c == closer:
                    depth -= 1
                    if depth == 0:
                        return k + 1

                k += 1

            return k

        def find_in_object(j: int, key: str) -> tuple[int, int] | None:
            j += 1  # skip {
            while True:
                j = skip_ws_and_comments(j)
                if j >= n or s[j] == "}":
                    return None

                if s[j] != '"':
                    j += 1
                    continue

                found_key, j2 = read_string_value(j)
                j = skip_ws_and_comments(j2)

                if j >= n or s[j] != ":":
                    j += 1
                    continue

                j += 1
                value_start = skip_ws_and_comments(j)
                value_end = find_value_end(value_start)

                if found_key == key:
                    return value_start, value_end

                j = value_end
                while j < n and s[j] not in ",}":
                    j += 1
                if j < n and s[j] == ",":
                    j += 1

        i = self._skip_ws_and_comments(s, 0)
        if i >= n or s[i] != "{":
            return None

        cur = i
        for idx, seg in enumerate(segs):
            span = find_in_object(cur, seg)
            if span is None:
                return None

            v_start, v_end = span
            if idx == len(segs) - 1:
                return v_start, v_end

            next_start = self._skip_ws_and_comments(s, v_start)
            if next_start >= n or s[next_start] != "{":
                return None

            cur = next_start

        return None

    def _skip_ws_and_comments(self, s: str, j: int) -> int:
        n = len(s)
        in_line_comment = False

        while j < n:
            ch = s[j]

            if in_line_comment:
                if ch == "\n":
                    in_line_comment = False
                j += 1
                continue

            if ch in " \t\r\n":
                j += 1
                continue

            if ch == "/" and j + 1 < n and s[j + 1] == "/":
                in_line_comment = True
                j += 2
                continue

            break

        return j

    def _append_into_array_literal(
        self,
        s: str,
        arr_start: int,
        arr_end: int,
        item: str,
    ) -> str:
        assert s[arr_start] == "["
        assert s[arr_end - 1] == "]"

        j = self._skip_ws_and_comments(s, arr_start + 1)
        if j < arr_end and s[j] == "]":
            return s[: arr_end - 1] + item + s[arr_end - 1 :]

        return s[: arr_end - 1] + ", " + item + s[arr_end - 1 :]

    # =========================
    # Error diagnostics
    # =========================

    def _format_error_snippet(
        self,
        text: str,
        lineno: int,
        colno: int,
        context: int = 2,
    ) -> str:
        lines = text.splitlines()
        idx = max(0, min(lineno - 1, len(lines) - 1))
        start = max(0, idx - context)
        end = min(len(lines), idx + context + 1)
        width = len(str(end))

        out: list[str] = []
        for i in range(start, end):
            num = str(i + 1).rjust(width)
            line = lines[i]
            out.append(f"{num} | {line}")
            if i == idx:
                caret = " " * max(0, colno - 1)
                out.append(f"{' ' * width} | {caret}^")
        return "\n".join(out)

    def _diagnose_json_error(
        self,
        text: str,
        lineno: int,
        colno: int,
        msg: str,
    ) -> list[str]:
        hints: list[str] = []
        lines = text.splitlines()
        line = lines[lineno - 1] if 0 <= lineno - 1 < len(lines) else ""

        if "Expecting property name enclosed in double quotes" in msg:
            m = re.search(r"^\s*([A-Za-z_][\w\-]*)\s*:", line)
            if m:
                key = m.group(1)
                hints.append(f'Key {key} must be quoted: "{key}": ...')
            hints.append(
                "Check for a trailing comma before the closing '}' or ']' on the previous line."
            )

        if "Expecting ',' delimiter" in msg:
            hints.append(
                "A comma may be missing between fields. Add ',' after the previous item."
            )

        if "Unterminated string" in msg:
            hints.append(
                'Unterminated string. Ensure quotes are paired and inner quotes are escaped: \\".'
            )

        if "Invalid control character" in msg:
            hints.append(
                r"Invalid control character. Escape backslashes and specials: '\\', '\n', '\t'."
            )

        if "Expecting value" in msg:
            hints.append(
                "Expecting value. Ensure a valid value appears after ':' and there is no stray comma."
            )

        return hints
