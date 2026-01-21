from typing import Any, Dict


class MergeDicts:
    @staticmethod
    def merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
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
