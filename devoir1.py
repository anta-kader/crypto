import math
import random

def euclide(a, b):
    return a//b, a%b

#Calcul de PGCD - euclide étentdu
def pgcd(a, b):
    q, r = euclide(a, b)
    while(r > 0):
        a, b = b, r
        q, r = euclide(a, b)
    return b

def bezout(a,b):
    x0, y0 = 1, 0
    x1, y1 = 0, 1
    q, r = euclide(a, b)
    n = 0
    while(r > 0):
        x0, y0, x1, y1 = x1, y1, q*x1 + x0, q*y1 + y0
        a, b = b, r
        q, r = euclide(a, b)
        n += 1
    return b, math.pow(-1, n-1)*x1 , math.pow(-1, n)*y1

def inverse(a, n):
    pgcd_result = pgcd(a, n)
    if(pgcd_result == 1):
        return bezout(a, n)[1]%n
    else:
        return None

def exponentiation(a, e, m):
    r = 1
    while e > 0:
        if e % 2 == 1:
            r = r * a % m
        e /= 2
        a = (a*a) % m
    return r

def chinese_rest(c1, m1, c2, m2):
    M, M1, M2 = m1*m2, m2, m1
    y1, y2 = inverse(M1, m1), inverse(M2, m2)
    return (c1*y1*M1 + c2*y2*M2) % M

def prime_fact(a):
    result = []
    max = math.floor(math.sqrt(a))
    f = 2
    while(f <= max):
        while((a % f) == 0):
            result.append(f)
            a /= f
        f += 1
    if a > 1:
        result.append(a)
    return result

def phi(a):
    prime_factors = prime_fact(a)
    size = len(prime_factors)
    result = 1
    if size == 1:
        result = a - 1
    else:
        for i in range(0, size):
            f = prime_factors[i]
            e = prime_factors.count(f)
            result *= math.pow(f, e-1)*(f-1)
            i += e-1
    return result

def erastostene (n):
    res = False
    if len(prime_fact(n)) == 1:
        res = True
    return res

def rabin_miller (n):
    res = False
    if n % 2 == 1 and n > 1:
        a = random.randint(1, n) #a in N; a < n
        s = 0
        d = n-1
        while n % 2 == 0: #2^s*d = n - 1
            s += 1
            d /= 2
        if a ** d % n == 1 :
            res = True
            r = s - 1
            while r > 0:
                if a**(2**r * d) % n == -1:
                    res = False
                r -= 1
    return res

def rabin_miller_it (n, i):
    res = False
    if n % 2 == 1 and n > 1:
        a = random.randint(1, n) #a in N; a < n
        s = 0
        d = n-1
        while n % 2 == 0: #2^s*d = n - 1
            s += 1
            d /= 2
        if a ** d % n == 1 :
            res = True
            if(s > 1):
                while i > 0:
                    r = random.randint(1, s - 1)
                    if a**(2**r * d) % n == -1:
                        res = False
                    i -= 1
    return res


def random_prime_int (n):
    value = 0
    all_values = list(range(0, (2**n) - 1))
    size = len(all_values)
    found = False
    while(not found and size > 0):
        i = random.randint(0, size)
        value = all_values[i]
        found = rabin_miller(value)
        if not found:
            size -= 1
            all_values.pop(i)
    if found:
        return value
    else:
        return False
