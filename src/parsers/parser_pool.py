from functools import cache

from frozendict import frozendict

from configs.languages import Language

from .protocols import Parser
from .python.parser import Parser as PythonParser

_PARSER_MAP = frozendict(
    {
        Language.PYTHON: PythonParser,
    }
)


class Parser_Pool:

    __slots__ = ("_parsers",)

    def __init__(self):
        self._parsers: dict[Language, Parser] = {}

    def get_parser(self, language: Language) -> Parser:
        return self._parsers.setdefault(language, _PARSER_MAP[language]())


@cache
def get_parser_pool() -> Parser_Pool:
    return Parser_Pool()
