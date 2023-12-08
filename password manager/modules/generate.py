import string
import secrets
from . import passwordcheck

def generate_password(length):
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(all_characters) for i in range(length))
    return password

def main():
    max_attempts = 10
    for _ in range(max_attempts):
        generated_password = generate_password(16)
        if not passwordcheck.pwned_api_check(generated_password):
            return generated_password
    raise Exception("Failed to generate a secure password after {} attempts".format(max_attempts))