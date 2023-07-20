import random
import string
import hashlib
import os


UNICODE_LIMIT = 1024


def generate_salt(length: int = 20):
    charset = string.ascii_letters = string.digits
    random_string = ''.join(random.choice(charset) for _ in range(length))
    return random_string


def split_password(password: str):
    return password.strip().split(' ')


def improve_passwords(passwords: list[str], salt: str) -> list[str]:
    return [hashlib.blake2b((salt + pw).encode('utf-8')).hexdigest() for pw in passwords]


def encrypt(file_path: str, password: str, salt: str = ''):
    passwords = improve_passwords(split_password(password), salt)
    print(passwords[::-1])

    with open(file_path, 'r') as file:
        text = file.read()

    for pw in passwords:
        encrypted_text = ""
        pw_length = len(pw)
        i = 0

        for char in text:
            encrypted_text += chr((ord(char) + ord(pw[i])) % UNICODE_LIMIT)
            i = (i + 1) % pw_length

        text = encrypted_text

    with open(file_path, 'w') as file:
        file.write(text)

    # encrypted_filename = f'{file_path}.enc'
    # os.rename(file_path, encrypted_filename)


def decrypt(file_path: str, password: str, salt: str = ''):
    passwords = improve_passwords(split_password(password)[::-1], salt)
    print(passwords)

    with open(file_path, 'r') as file:
        text = file.read()

    for pw in passwords:
        decrypted_text = ""
        pw_length = len(pw)
        i = 0

        for char in text:
            decrypted_text += chr((ord(char) - ord(pw[i])) % UNICODE_LIMIT)
            i = (i + 1) % pw_length

        text = decrypted_text

    with open(file_path, 'w') as file:
        file.write(text)

    # decrypted_filename = file_path.replace('.enc', '')
    # os.rename(file_path, decrypted_filename)
