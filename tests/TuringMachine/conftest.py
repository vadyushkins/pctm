import pytest

from src.utils import is_prime

params = [
             {
                 'path': 'resources/machines/binary_palindrome_tm.txt'
                 , 'word': list(bin(x)[2:] + bin(x)[::-1][:-2])
             }
             for x in range(42)
         ] + [
             {
                 'path': 'resources/machines/primality_check_lba.txt'
                 , 'word': list(f'${"a" * n}#')
             }
             for n in range(24) if is_prime(n)
         ]


@pytest.fixture(scope='session', params=params)
def suite(request):
    return request.param
