from lab2 import app
from flask import render_template, request
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


def extended_euclidean (a, b):
    phi = a

    x1 = 1
    x2 = 0
    y1 = 0
    y2 = 1

    while b:
        q = a // b
        a = b
        b = a % b
        x1 = x2
        x2 = x1 - x2 * q
        y1 = y2
        y2 = y1 - y2 * q

    print('x, y ', x1, ' ', y1)

    d = phi + y1

    return d


def gcd_extended(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = gcd_extended(b % a, a)
        return (g, x - (b // a) * y, y)


def mod_inverse(e, phi):
    g, x, y = gcd_extended(e, phi)
    if g != 1:
        raise Exception('Обратное по модулю число не может быть найдено')
    else:
        return x % phi


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

    #d = pow(e, -1, phi)
    #d = extended_euclidean(e, phi)
    d = mod_inverse(e, phi)    

    return [p, q, phi, n, e, d]


@app.route('/cipher', methods=['POST'])
def cipher():
    phrase = request.form.get('phrase')
    e = int(request.form.get('e'))
    n = int(request.form.get('n'))

    encoded_phrase = [ord(c) for c in phrase]
    cipher_phrase = [pow(c, e, n) for c in encoded_phrase]

    return cipher_phrase