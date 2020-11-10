import pytest

from src.utils import is_prime

params = [
    {
        'path': 'resources/primality_check_ug.txt'
        , 'word': 'a' * p
    }
    for p in range(16) if is_prime(p)
]


@pytest.fixture(scope='session', params=params)
def suite(request):
    return request.param
