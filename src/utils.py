""" Useful utils module """


def is_prime(n: int) -> bool:
    """
    Checks if a number n is prime
    :param n: Integer number to test
    :return: Boolean value - True if n is prime, else False
    """

    if n < 2:
        return False

    i: int = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1

    return True
