import pytest

params = [
    {
        'path': 'resources/primality_check_ug.txt'
        , 'word': 'a' * p
    }
    for p in range(14)
]


@pytest.fixture(scope='session', params=params)
def suite(request):
    return request.param
