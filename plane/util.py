def is_prime(n):
    if not isinstance(n, int):
        # raise ValueError("Integer should be given.")
        return False

    if n <= 0:
        # raise ValueError("Positive number should be given.")
        return False

    if n == 1:
        return False
    if n < 4:
        return True

    for i in range(2, n):
        if n % i == 0:
            return False
        if n < i*i:
            break

    return True
