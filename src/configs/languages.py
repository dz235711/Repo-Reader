from dataclasses import dataclass
from enum import StrEnum
from collections.abc import Iterable

from frozendict import frozendict


class Language(StrEnum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CSHARP = "csharp"
    RUBY = "ruby"
    PHP = "php"
    GO = "go"
    RUST = "rust"
    SWIFT = "swift"
    KOTLIN = "kotlin"


@dataclass(frozen=True, slots=True, kw_only=True)
class LanguageProfile:
    language: Language
    extensions: frozenset[str]


_LANGUAGE_PROFILES = frozendict(
    {
        Language.PYTHON: LanguageProfile(
            language=Language.PYTHON,
            extensions=frozenset({".py"}),
        ),
    }
)

_EXTENSION_TO_LANGUAGE_PROFILE_MAP = frozendict(
    {ext: prof for prof in _LANGUAGE_PROFILES.values() for ext in prof.extensions}
)


def get_language_profiles(languages: Iterable[Language]) -> list[LanguageProfile]:
    return [_LANGUAGE_PROFILES[language] for language in languages]


def get_language_profile(language: Language) -> LanguageProfile:
    return get_language_profiles([language])[0]


def get_language_profile_by_extension(extension: str) -> LanguageProfile:
    return _EXTENSION_TO_LANGUAGE_PROFILE_MAP[extension]
