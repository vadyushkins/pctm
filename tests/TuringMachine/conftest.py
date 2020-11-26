import pytest

params = [
    {
        'path': 'resources/primality_check_lba.txt'
        , 'word': list(f'${"a" * n}#')
    }
    for n in range(100)
]


@pytest.fixture(scope='session', params=params)
def suite(request):
    return request.param
