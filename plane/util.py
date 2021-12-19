from typing import Dict


def is_prime(n: int) -> bool:
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


def factorize(n: int) -> Dict[int, int]:
    factor = {}
    for i in range(2, n):  # range 가 리스트를 미리 생성해 두지 않아 complexity 에 영향이 없음
        if n < i*i:
            break

        p = 0
        while n % i == 0:
            p += 1
            n //= i
        if p > 0:
            factor[i] = p

    if n > 1:
        factor[n] = 1

    return factor
