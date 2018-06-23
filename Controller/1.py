from types import coroutine


@coroutine
def switch():
    yield


def run(coros):
    """Execute a list of co-routines until all have completed."""
    # Copy argument list to avoid modification of arguments.
    coros = list(coros)

    while len(coros):
        # Copy the list for iteration, to enable removal from original
        # list.
        for coro in list(coros):
            try:
                coro.send(None)
            except StopIteration:
                coros.remove(coro)


async def coro1():
    print("C1: Start")
    await switch()
    print("C1: a")
    await switch()
    print("C1: b")
    await switch()
    print("C1: c")
    await switch()
    print("C1: Stop")


async def coro2():
    print("C2: Start")
    await switch()
    print("C2: a")
    await switch()
    print("C2: b")
    await switch()
    print("C2: c")
    await switch()
    print("C2: Stop")

def main(msg):
    print(msg)
    run([coro1(), coro2()])

if __name__  == "__main__":
    main('hello')