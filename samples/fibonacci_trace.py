import sys


def fib(n):
    """Return the n'th fibonacci number."""

    if n <= 1:
        import pdb; pdb.set_trace()
        return 1

    return fib(n-1) + fib(n-2)


if __name__ == '__main__':
    print (fib(int(sys.argv[-1])))
