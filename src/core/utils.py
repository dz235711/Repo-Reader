from collections.abc import Callable, Generator, Iterable

type NestedIterable[T] = Iterable[NestedIterable[T] | T]


def flatten[T](
    items: NestedIterable[T], terminators: tuple[type[T]]
) -> Generator[T, None, None]:
    for item in items:
        if isinstance(item, Iterable) and not isinstance(item, terminators):
            yield from flatten(item, terminators)
        else:
            yield item


def map_t[T, U](func: Callable[[T], U], items: Iterable[T]) -> tuple[U, ...]:
    return tuple(map(func, items))
