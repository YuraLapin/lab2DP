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

    x, xx, y, yy = 1, 0, 0, 1

    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q

    print('x, y ', x, ' ', y)

    d = phi + y

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

    d = extended_euclidean(phi, e)

    for i in range(1, 1000):
        if pow(699, i, 779) == 21:
            print("qwe: ", i)

    return [p, q, phi, n, e, d]


@app.route('/cipher', methods=['POST'])
def cipher():
    phrase = request.form.get('phrase')
    e = int(request.form.get('e'))
    n = int(request.form.get('n'))

    encoded_phrase = [ord(c) for c in phrase]
    cipher_phrase = [pow(c, e, n) for c in encoded_phrase]

    return cipher_phrase