import requests
import hashlib
import re

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    try:
        res = requests.get(url)
        if res.status_code != 200:
            raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
        return res
    except requests.exceptions.RequestException as err:
        print ("Network error: ",err)
        return None

def get_password_leaks_count(hashes, hash_to_check):
    if hashes is not None:
        hashes = (line.split(':') for line in hashes.text.splitlines())
        for h, count in hashes:
            if h == hash_to_check:
                return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def password_strength(password):
    password_requirements = [
        "[A-Z]",                         # at least one uppercase letter
        "[a-z]",                         # at least one lowercase letter
        "[0-9]",                         # at least one digit
        '[!@#$%^&*(),.?":{}|<>\[\]]',    # at least one special character 
        ".{8,}"                          # at least 8 characters long
    ]
    strength = 'Strong password'
    for requirement in password_requirements:
        if not re.search(requirement, password):
            strength = 'Password does not meet all requirements'
            break
    return strength

def check_passwords(password): 
    if not isinstance(password, str):
        return 'Invalid input. Password must be a string.'
    strength = password_strength(password)
    count = pwned_api_check(password)
    if count:
        print(f'password was found {count} times... you should probably change your password')
    print(f'{strength}')
    print()
    return strength