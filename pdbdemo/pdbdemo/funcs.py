import itertools


def calc_sum(*args):

    result = 0

    for a in args:
        result += a

    return result


def product_inverses(ints):

    result = 1.0

    for i in ints:
        result = result * (1.0 / i)

    return result


def try_product_inverses(ints):

    result = 1.0

    try:
        for i in ints:
            result = result * (1.0 / i)
    except Exception:
        import pdb; pdb.post_mortem()

    return result


def compound(*ints):

    return calc_sum(
        *[try_product_inverses(x)
          for x in itertools.combinations(ints, len(ints) / 2)]
    )

if __name__ == '__main__':

    print sum(*range(0, 10))
