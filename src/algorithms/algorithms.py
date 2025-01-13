import random
import math

def algorithm_evklid_extended(x, y):
    if x == 0:
        return (y, 0, 1)
    else:
        d, x1, y1 = algorithm_evklid_extended(y % x, x)
        return (d, y1 - (y // x) * x1, x1)
    
def algorithm_fast_pow(x, y, modulus=None):
    if y < 0:
        if modulus is None:
            return 1 / algorithm_fast_pow(x, -y)
        else:
            inverse = algorithm_evklid_extended(x, modulus)[1]
            if inverse is None:
                raise ValueError("Modular inverse does not exist")
            return inverse * algorithm_fast_pow(x, -y, modulus) % modulus
    result = 1
    base = x if modulus is None else x % modulus
    y = abs(y)
    while y > 0:
        if y & 1:
            result = (result * base) % modulus if modulus else result * base
        base = (base * base) % modulus if modulus else base * base
        y >>= 1
    return result

def algorithm_Yakobi_symbol(a, n):
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be an odd positive integer")
    
    a = a % n
    result = 1
    
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        
        a, n = n, a
        
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        
        a = a % n
    
    if n == 1:
        return result
    else:
        return 0
    
def algorithm_Fermat_test(n, k=10):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True

    for _ in range(k):
        a = random.randint(2, n - 2)
        if algorithm_fast_pow(a, n - 1, n) != 1:
            return False
    return True

def algorithm_Solovay_Strassen_test(n, k=10):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = algorithm_Yakobi_symbol(a, n)
        if x == 0 or algorithm_fast_pow(a, (n - 1) // 2, n) != x % n: # x = (a ^ ((n - 1) / 2)) mod n
            return False
    return True

def algorithm_Miller_Rabin_test(n, k=None):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # n - 1 = 2^s * d
    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    if k is None:
        k = int(math.log2(n))

    for _ in range(k):
        a = random.randint(2, n - 2) # a ^ d = 1 mod n
        x = algorithm_fast_pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = algorithm_fast_pow(x, 2, n) # x^(2^s) = n - 1 mod n
            if x == n - 1:
                break
        else:
            return False

    return True

def algorithm_comprasion(a ,b ,m):
    GCD, x, _ = algorithm_evklid_extended(a, m)
    if b % GCD != 0:
        return None
    
    a //= GCD
    b //= GCD
    m //= GCD
    x = (x * b) % m
    
    solutions = []
    for k in range(GCD):
        solutions.append(x + k * m)
    
    return solutions

def chinese_remainder_theorem(system):
    M = 1
    for _, _, m in system:
        M *= m
    
    x = 0
    for _, b, m in system:
        Mi = M // m
        _, Mi_inv, _ = algorithm_evklid_extended(Mi, m)
        x += b * Mi * Mi_inv
    
    return x % M, M

def algorithm_comprasion_system(system):
    solved_system = []
    for a, b, m in system:
        solutions = algorithm_comprasion(a, b, m)
        if solutions is None:
            return None
        solved_system.append((a, solutions[0], m))
    
    return chinese_remainder_theorem(solved_system)


def algorithm_generate_prime(bit_length):
    prime = 1
    for _ in range(bit_length - 1):
        prime <<= random.randint(0, 1)

    prime |= 1

    while True:
        if algorithm_Miller_Rabin_test(prime):
            return prime
        
def algorithm_second_degree_comparison(a, p):
    if algorithm_Yakobi_symbol(a, p) != 1:
        raise ValueError(f"The number {a} is not a quadratic residue modulo {p}.")

    while True:
        N = random.randint(2, p - 1) 
        if algorithm_Yakobi_symbol(N, p) == -1:
            break

    k = 0
    h = p - 1
    while h % 2 == 0:
        h //= 2
        k += 1

    a1 = algorithm_fast_pow(a, (h + 1) // 2, p)
    a2 = algorithm_fast_pow(a, h, p)
    N1 = algorithm_fast_pow(N, h, p)
    N2 = 1

    for i in range(k):
        b = a1 * N2 % p
        c = a2 * algorithm_fast_pow(b, 2, p) % p
        print(k - 2 -i)
        d = algorithm_fast_pow(c, algorithm_fast_pow(2, k - 2 - i, p), p)

        j = 0 if d == 1 else 1
        N2 = N2 * algorithm_fast_pow(N1, algorithm_fast_pow(2, i, p) * j, p) % p

    x = a1 * N2 % p
    return [x, p - x] 

def algorithm_Polynomial_Field(p, degree):
    choice = input("Choose operation: 1 - add polynomials, 2 - muiltiply polynomials, help - show example of cofficients input\nChoice: ")
    if choice == '1':
        print("Enter coefficients for the first polynomial")
        a = list(map(int, input().split()))
        print("Enter coefficients for the second polynomial")
        b = list(map(int, input().split()))
        print(algorithm_add_polynomials(a, b, p))
    elif choice == '2':
        print("Enter coefficients for the first polynomial")
        a = list(map(int, input().split()))
        print("Enter coefficients for the second polynomial")
        b = list(map(int, input().split()))
        print("Enter coefficients for the irreducible polynomial")
        irreducible = list(map(int, input().split()))
        print(algorithm_mul_polynomials(a, b, p, irreducible))
    elif choice == "help":
        print("Example of coefficients input:")
    else:
        print("Invalid choice")

def algorithm_add_polynomials(a, b, p):
    length = max(len(a), len(b))
    result = [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(length)]
    return [coef % p for coef in result]

def algorithm_mul_polynomials(a, b, p, irreducible):
    result = [0] * (len(a) + len(b) - 1)

    for i in range(len(a)):
        for j in range(len(b)):
            result[i + j] += a[i] * b[j]
            result[i + j] %= p

    while len(result) >= len(irreducible):
        if result[0] == 0:
            result.pop(0)
            continue
        factor = result[0]
        for i in range(len(irreducible)):
            result[i] -= irreducible[i] * factor
            result[i] %= p
        result.pop(0)
    return result