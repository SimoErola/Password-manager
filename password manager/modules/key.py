from Cryptodome.Hash import SHA256
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Random import get_random_bytes
import os
import subprocess

def keys(key_file_path, user_password):
    try:
        if not os.path.isfile(key_file_path):
            salt = get_random_bytes(16)
            key = PBKDF2(user_password, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
            with open(key_file_path, "wb") as f:
                f.write(salt + key)
        else:
            with open(key_file_path, "rb") as f:
                salt_key = f.read()
                salt = salt_key[:16]
                key = salt_key[16:]
                key_check = PBKDF2(user_password, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
                if key != key_check:
                    return "Incorrect password"
        return key  # Return the key
    except IOError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def hide_file(file_path):
    try:
        if os.name == "nt":
            subprocess.check_call(["attrib", "+H", file_path])
    except subprocess.CalledProcessError as e:
        print(f"Unable to hide file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")