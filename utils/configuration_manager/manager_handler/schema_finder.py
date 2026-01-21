from pathlib import Path
from typing import List, Optional

from utils import CONFIG_DEFAULT_SCHEMAS


class SchemaFinder:
    def __init__(self, schemas_dir: Path):
        self.schemas_dir = schemas_dir

    def find_all(self) -> List[Path]:
        found: List[Path] = []
        for name in CONFIG_DEFAULT_SCHEMAS:
            p = self.schemas_dir / name
            if p.exists() and p.is_file():
                found.append(p)
        return found

    def find_first(self) -> Optional[Path]:
        for name in CONFIG_DEFAULT_SCHEMAS:
            p = self.schemas_dir / name
            if p.exists() and p.is_file():
                return p
        return None
