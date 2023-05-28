import random


def modularExponentiation(a, b, n):
    b_bin = bin(b)[2:]
    current = a % n
    if b_bin[-1] == "1":
        result = current
    else:
        result = 1

    # start at second last bit
    i = len(b_bin) - 2
    while i >= 0:
        current = (current * current) % n
        if b_bin[i] == "1":
            result = (result * current) % n
        i -= 1
    return result


def millerRabin(n, k):
    if n == 2 or n == 3:
        return "prime"
    if n & 1 == 0:
        return "composite"

    s = 0
    t = n - 1

    while t is int and t & 1 == 0:
        s = s + 1
        t = t / 2

    for i in range(k):
        a = random.randint(2, n - 2)
        if modularExponentiation(a, n - 1, n) != 1:
            return "composite"

        for j in range(s):
            exponent = t << j
            current = modularExponentiation(a, exponent, n)
            if current == 1 and (prev != 1 and prev != n - 1):
                return "composite"
            else:
                prev = current
    return "prime"

print(millerRabin(7331, 10))
