import pytest

from src.utils import is_prime

params = [
    {
        'path': 'resources/primality_check_lba.txt'
        , 'word': list(f'${"a" * n}#')
    }
    for n in range(24) if is_prime(n)
]


@pytest.fixture(scope='session', params=params)
def suite(request):
    return request.param
