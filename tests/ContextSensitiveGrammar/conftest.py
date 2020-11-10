import pytest

from src.utils import is_prime

params = [
    {
        'path': 'resources/grammars/primality_check_csg.txt'
        , 'word': 'a' * p
    }
    for p in range(24) if is_prime(p)
]


@pytest.fixture(scope='session', params=params)
def suite(request):
    return request.param
