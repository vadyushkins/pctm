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


binary_palindromes = [
    list(bin(x)[2:] + bin(x)[::-1][:-2])
    for x in range(42)
]

primes = [x for x in range(8) if is_prime(x)]

params = [
             {
                 'path': 'resources/machines/binary_palindrome_tm.txt'
                 , 'word': list(word)
             }
             for word in binary_palindromes
         ] + [
             {
                 'path': 'resources/machines/primality_check_lba.txt'
                 , 'word': list(f'${"a" * n}#')
             }
             for n in primes
         ]


@pytest.fixture(scope='session', params=params)
def suite(request):
    return request.param
