from typing import Iterable



def NonSpaceEitherOne(sources: tuple[Iterable], arguments: dict=None) -> Iterable:

    for l, r in (p for l in sources for p in l):
        assert any((l, r)) or not all((l, r)), f"非空二选一插件不能处理同时有值或同时为空的值对，{l} ： {r}"

        yield (l if l else r, )

