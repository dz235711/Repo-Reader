from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from frozendict import frozendict
from gitignore_parser import parse_gitignore


class Vcs(StrEnum):
    GIT = "git"
    MERCURIAL = "mercurial"
    SUBVERSION = "subversion"
    BAZAAR = "bazaar"
    FOSSIL = "fossil"
    CVS = "cvs"


@dataclass(frozen=True, slots=True, kw_only=True)
class VcsProfile:
    vcs: Vcs
    ignore_parser: Callable[[Path], Callable[[Path], bool]]
    ignore_filename: str


_VCS_PROFILES = frozendict(
    {
        Vcs.GIT: VcsProfile(
            vcs=Vcs.GIT,
            ignore_parser=parse_gitignore,
            ignore_filename=".gitignore",
        ),
    }
)


def get_vcs_profile(vcs: Vcs) -> VcsProfile:
    return _VCS_PROFILES[vcs]
