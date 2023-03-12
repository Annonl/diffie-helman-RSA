from math import gcd
from random import randint
from typing import Tuple
from random import randrange

def generate_keys(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    n = p * q
    phi = (p - 1) * (q - 1)
    e = choose_e(phi)
    d = find_d(e, phi)
    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key

def choose_e(phi: int) -> int:
    e = randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = randint(2, phi - 1)
    return e

def find_d(e: int, phi: int) -> int:
    d = extended_gcd(e, phi)[1]
    return d % phi

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def encrypt(public_key: Tuple[int, int], plaintext: int) -> int:
    n, e = public_key
    return pow(plaintext, e, n)

def decrypt(private_key: Tuple[int, int], ciphertext: int) -> int:
    n, d = private_key
    return pow(ciphertext, d, n)

def generate_key(prime, alpha):
    secret_key = randint(2, prime - 2)
    
    public_key = pow(alpha, secret_key, prime)
    
    return secret_key, public_key

def compute_secret(prime, alpha, B, secret_key):
    shared_secret = pow(B, secret_key, prime)
    
    return shared_secret

def generate_prime(n_bits: int) -> int:
    while True:
        p = randrange(pow(2, n_bits - 1) - 1, pow(2, n_bits), 2)
    
        if is_prime(p):
            return p

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def find_primitive_roots(p: int):
    primitive_roots = []
    for g in range(1, p):
        is_primitive_root = True
        for i in range(1, p - 1):
            if pow(g, i, p) == 1:
                is_primitive_root = False
                break
        if is_primitive_root:
            return g
    return primitive_roots

if __name__ == "__main__":
    side = int(input("Введите сторону:\n 1 - Первая сторона\n 2 - Вторая сторона\n"))
    if side == 1:
        p = generate_prime(10)
        g = find_primitive_roots(p)
        print("p = " + str(p) + " g = " + str(g))
        a_secret, a_public = generate_key(p, g)
        print("Public = " + str(a_public) + " Secret = " + str(a_secret))
        b_public = int(input("Введите публичный ключ 2 стороны: "))
        a_shared_secret = compute_secret(p, g, b_public, a_secret)
        print("----------------------------")
        public_key, private_key = generate_keys(generate_prime(10), generate_prime(10))
        print(str(public_key) + " " + str(private_key))
        n = int(input("Введите публичный ключ 2 стороны: "))
        d = int(input("Введите публичный ключ 2 стороны: "))
        pub_key = (n, d)

        ciphertext = encrypt(pub_key, a_shared_secret)
        print(ciphertext)

        c = int(input("Введите зашифрованное сообщение:"))
        decrypted_text = decrypt(private_key, c)
        if decrypted_text == a_shared_secret:
            print("Аутентификация прошла")
        else:
            print("Аутентификация не прошла")
    
    elif side == 2:
        p = int(input("Введите p: "))
        g = int(input("Введите g: "))
        b_secret, b_public = generate_key(p, g)
        print("Public = " + str(b_public) + " Secret = " + str(b_secret))
        a_public = int(input("Введите публичный ключ 1 стороны: "))
        b_shared_secret = compute_secret(p, g, a_public, b_secret)
        print("----------------------------")
        public_key, private_key = generate_keys(generate_prime(10), generate_prime(10))
        print(str(public_key) + " " + str(private_key))
        n = int(input("Введите публичный ключ 1 стороны: "))
        d = int(input("Введите публичный ключ 1 стороны: "))
        pub_key = (n, d)

        ciphertext = encrypt(pub_key, b_shared_secret)
        print(ciphertext)

        c = int(input("Введите зашифрованное сообщение:"))

        decrypted_text = decrypt(private_key, c)      
        if decrypted_text == b_shared_secret:
            print("Аутентификация прошла")
        else:
            print("Аутентификация не прошла")
    