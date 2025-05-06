import asyncio

from tracardi.context import ServerContext, Context, get_context
from tracardi.service.decorators.function_memory_cache import cache_for, cache, async_cache_for, delete_cache, has_cache
import time


@cache_for(0.5, max_size=2, allow_null_values=False)
def x(a):
    return a


@async_cache_for(0.5, max_size=2, allow_null_values=False)
async def y(a):
    return a


def test_positive_path():
    with ServerContext(Context(production=True)):

        context = get_context()
        context_hash = context.__hash__()
        fnc_str = f"{context_hash}:unit.test_function_memory_cache:x"

        assert x(1) == 1
        assert x(2) == 2

        assert fnc_str in cache

        assert cache[fnc_str].name == fnc_str
        assert len(cache[fnc_str].memory_buffer) == 2

        assert x(3) == 3
        assert x(4) == 4

        time.sleep(1)

        assert x(5) == 5

        assert len(cache[fnc_str].memory_buffer) == 1


def test_async_positive_path():
    async def main():
        with ServerContext(Context(production=True)):

            context = get_context()
            context_hash = context.__hash__()
            fnc_str = f"{context_hash}:unit.test_function_memory_cache:y"

            assert await y(1) == 1
            assert await y(2) == 2

            assert fnc_str in cache
            assert cache[fnc_str].name == fnc_str
            assert len(cache[fnc_str].memory_buffer) == 2

            assert await y(3) == 3
            assert await y(4) == 4

            await asyncio.sleep(1)

            assert await y(5) == 5

            assert len(cache[fnc_str].memory_buffer) == 1

    asyncio.run(main())



def test_delete():
    with ServerContext(Context(production=True)):

        context = get_context()
        context_hash = context.__hash__()
        fnc_str = f"{context_hash}:unit.test_function_memory_cache:x"

        assert x(1) == 1
        assert fnc_str in cache
        assert len(cache[fnc_str].memory_buffer) == 1

        delete_cache(x, 1)

        assert len(cache[fnc_str].memory_buffer) == 0


def test_multi_tenant():
    with ServerContext(Context(production=True)):
        assert 1 == x(1)
        assert has_cache(x, 1)
        delete_cache(x, 1)
        assert not has_cache(x, 1)

    with ServerContext(Context(production=False)):
        assert 1 == x(1)

    with ServerContext(Context(production=True)):
        assert not has_cache(x, 1)
        with ServerContext(Context(production=False)):
            assert has_cache(x, 1)
