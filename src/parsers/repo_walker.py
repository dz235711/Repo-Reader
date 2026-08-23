from pathlib import Path
from typing import Generator, Callable
from collections.abc import Iterable
from contextlib import contextmanager

from configs.vcs import get_vcs_profile, VcsProfile, Vcs
from configs.languages import get_language_profiles
from configs.languages import Language

from .repo_tree import Root, Directory, File, FSItem

type _IgnoreRule = Callable[[Path], bool]


def walk_repo(
    indexing_languages: Iterable[Language], repository_root: Path, repository_vcs: Vcs
) -> Root:
    language_profiles = get_language_profiles(indexing_languages)
    language_extensions = frozenset().union(
        *[prof.extensions for prof in language_profiles]
    )

    root_dir = _walk_directory(
        repository_root,
        repository_root,
        [lambda path: path.suffix not in language_extensions],
        get_vcs_profile(repository_vcs),
    )

    return Root(
        abs_path=repository_root,
        directory=root_dir,
    )


@contextmanager
def _ignore_rules_context(
    abs_path: Path, ignore_rules: list[_IgnoreRule], vcs_profile: VcsProfile
) -> Generator[None, None, None]:
    ignore_file = abs_path / vcs_profile.ignore_filename
    has_ignore_file = ignore_file.exists()
    if has_ignore_file:
        ignore_rules.append(vcs_profile.ignore_parser(ignore_file))
        try:
            yield
        finally:
            if has_ignore_file:
                ignore_rules.pop()
    else:
        yield


def _walk_repo(
    abs_root: Path,
    abs_path: Path,
    ignore_rules: list[_IgnoreRule],
    vcs_profile: VcsProfile,
) -> FSItem | None:
    rel_path = abs_path.relative_to(abs_root)
    if abs_path.is_dir():
        return _walk_directory(abs_root, abs_path, ignore_rules, vcs_profile)
    else:
        if not any(rule(abs_path) for rule in ignore_rules):
            return File(rel_path=rel_path)
    return None


def _walk_directory(
    abs_root: Path,
    abs_path: Path,
    ignore_rules: list[_IgnoreRule],
    vcs_profile: VcsProfile,
) -> Directory:
    with _ignore_rules_context(abs_path, ignore_rules, vcs_profile):
        children = (
            _walk_repo(abs_root, child, ignore_rules, vcs_profile)
            for child in abs_path.iterdir()
        )
        return Directory(
            rel_path=abs_path.relative_to(abs_root),
            children=tuple(child for child in children if child is not None),
        )
