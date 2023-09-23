from lab2 import app
from flask import render_template
import random, math


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, num // 2):
        if num % i == 0:
            return False
    return True


def generate_prime(min_val, max_val):
    prime = random.randint(min_val, max_val)
    while not is_prime(prime):
        prime = random.randint(min_val, max_val)
    return prime


def mod_inverse(e, m):
    for d in range(3, m):
        if (d * e) % m == 1:
            return d
    raise ValueError('Обратное по модулю число не может быть найдено для e = {e} и phi = {phi}')

def extended_euclidean (a, b):
    phi = a

    x1 = 0
    x2 = 1
    y1 = 1
    y2 = 0

    while b > 0:
        q = a // b
        r = a - q * b
        x = x2 - q * x1
        y = y2 - q * y1
        a = b
        b = r
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y

    print(x2, ' ', y2)

    d = phi - abs(min(x2, y2))

    return d


@app.route('/generate_keys', methods = ['POST'])
def generate_keys():
    MIN_GEN = math.pow(2, 16)
    MAX_GEN = math.pow(2, 20)

    p = generate_prime(MIN_GEN, MAX_GEN)
    q = generate_prime(MIN_GEN, MAX_GEN)

    while p == q:
        q = generate_prime(MIN_GEN, MAX_GEN)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(3, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(3, phi - 1)

    #d = mod_inverse(e, phi)

    d = extended_euclidean(phi, e)

    return [p, q, phi, n, e, d]