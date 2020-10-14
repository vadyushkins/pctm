import pytest


def is_prime(n):
    if n < 2:
        return False

    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1

    return True


primes = [x for x in range(12) if is_prime(x)]

params = [
    {
        'path': 'resources/grammars/primality_check_csg.txt'
        , 'word': 'a' * p
    }
    for p in primes
]


@pytest.fixture(scope='session', params=params)
def suite(request):
    return request.param
