from pathlib import Path


class JsoncParseError(Exception):
    def __init__(
        self,
        path: Path,
        lineno: int,
        colno: int,
        msg: str,
        snippet: str,
        hints: list[str] | None = None,
    ) -> None:
        super().__init__(
            f"Parse error in '{path}': line {lineno}, column {colno}: {msg}"
        )
        self.path = path
        self.lineno = lineno
        self.colno = colno
        self.msg = msg
        self.snippet = snippet
        self.hints = hints or []

    def pretty(self) -> str:
        lines: list[str] = []
        lines.append("[bold red]┌─ JSONC parse error[/bold red]")
        lines.append(f"[red]│[/red] File   : [cyan]{self.path}[/cyan]")
        lines.append(f"[red]│[/red] Line   : [yellow]{self.lineno}[/yellow]")
        lines.append(f"[red]│[/red] Column : [yellow]{self.colno}[/yellow]")
        lines.append(f"[red]│[/red] Reason : [magenta]{self.msg}[/magenta]")
        lines.append("[red]├─ Snippet[/red]")

        for line in self.snippet.splitlines():
            if line.strip().endswith("^"):
                lines.append(f"[red]│[/red] [green]{line}[/green]")
            else:
                lines.append(f"[red]│[/red] {line}")

        if self.hints:
            lines.append("[red]├─ Hints[/red]")
            for hint in self.hints:
                lines.append(f"[red]│[/red] • {hint}")

        lines.append("[red]└──────────────────────────────────────────────────[/red]")
        return "\n".join(lines)
