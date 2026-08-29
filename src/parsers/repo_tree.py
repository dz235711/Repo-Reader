from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True, kw_only=True)
class Root:
    abs_path: Path
    directory: Directory


type FSItem = Directory | File


@dataclass(frozen=True, slots=True, kw_only=True)
class Directory:
    rel_path: Path
    children: tuple[FSItem, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class File:
    rel_path: Path
