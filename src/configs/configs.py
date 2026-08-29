from tomllib import load as load_toml
from pathlib import Path
from functools import cache

from pydantic import BaseModel

from adaptors.pydantic import FrozenDict

from .languages import Language
from .vcs import Vcs


class _Git(BaseModel):
    respect_gitignore: bool


class _Repository(BaseModel):
    root: Path
    vcs: Vcs
    git: _Git


class _Ignore(BaseModel):
    extra: frozenset[str]


class _Indexing(BaseModel):
    languages: FrozenDict[Language, str]


class Config(BaseModel):
    repository: _Repository
    ignore: _Ignore
    indexing: _Indexing

    @classmethod
    def load(cls, path: Path) -> Config:
        with open(path, "rb") as f:
            data = load_toml(f)
        return cls(**data)


_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.toml"


@cache
def get_config() -> Config:
    return Config.load(_CONFIG_PATH)
