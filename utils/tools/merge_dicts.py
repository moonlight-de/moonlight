from typing import Any, Dict

type AnyDict = Dict[str, Any]


class MergeDicts:
    @staticmethod
    def merge(base: AnyDict, override: AnyDict) -> AnyDict:
        """
        Mutates `base` by applying `override` on top (recursive).
        Returns base for convenience.
        """
        for k, v in override.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                MergeDicts.merge(base[k], v)
            else:
                base[k] = v
        return base
