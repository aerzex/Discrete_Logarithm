import sys 
import os
import math
lab1_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'algorithms'))
sys.path.append(lab1_path)
from algorithms import algorithm_fast_pow, algorithm_comprasion, algorithm_rho_pollard_fact

def algorithm_rho_pollard():
    u, v = 2, 2
    a = int(input("Enter number a: "))
    b = int(input("Enter number b: "))
    p = int(input("Enter number p: "))
    c = [u, v]
    d = c
    for _ in range(1000):
        c = spfunc(a, b, c, p)
        d = spfunc(a, b, spfunc(a, b, d, p), p)
        c_i = (algorithm_fast_pow(a, c[0]) * algorithm_fast_pow(b, c[1])) % p
        d_i = (algorithm_fast_pow(a, d[0]) * algorithm_fast_pow(b, d[1])) % p
        if(c_i == d_i):
            a_d = (c[1] - d[1]) % (p - 1)
            b_d = (d[0] - c[0]) % (p - 1)
            return algorithm_comprasion(a_d, b_d, p - 1)



def spfunc(a, b, c, p):
    c_i = (algorithm_fast_pow(a, c[0]) * algorithm_fast_pow(b, c[1])) % p
    if c_i < p // 2:
        return (c[0] + 1) % (p - 1), c[1] % (p - 1)
    else:
        return c[0] % (p - 1), (c[1] + 1) % (p - 1)

def main():
    print(algorithm_rho_pollard())

main()

