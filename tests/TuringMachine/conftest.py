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


@pytest.fixture(scope='session', params=[
    {
        'TuringMachine': 'resources/machines/binary_palindrome_tm.txt'
        , 'word': list('101101')
    }
    , {
        'TuringMachine': 'resources/machines/primality_check_lba.txt'
        , 'word': list('$aaaaa#')
    }
])
def manual_suite(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'TuringMachine': 'resources/machines/binary_palindrome_tm.txt'
        , 'accepted_words': [list(bin(x)[2:] + bin(x)[::-1][:-2]) for x in range(42)]
        , 'not_accepted_words': [list(str(0) + bin(x)[2:] + bin(x)[::-1][:-2] + str(1)) for x in range(42)]
    }
    , {
        'TuringMachine': 'resources/machines/primality_check_lba.txt'
        , 'accepted_words': [list(f'${"a" * x}#') for x in range(42) if is_prime(x)]
        , 'not_accepted_words': [list(f'${"a" * x}#') for x in range(42) if not is_prime(x)]
    }
])
def automatic_suite(request):
    return request.param
