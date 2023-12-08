from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import sqlite3


def save_password_to_db(site, user, password, db_path, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_user = cipher.encrypt(pad(user.encode(), AES.block_size))
    encrypted_password = cipher.encrypt(pad(password.encode(), AES.block_size))
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Passwords (site BLOB, user BLOB, password BLOB)")
    c.execute("INSERT INTO Passwords VALUES (?, ?, ?)", (site, encrypted_user, encrypted_password))
    conn.commit()
    conn.close()


def decrypt_password_from_db(site, db_path, key):
    cipher = AES.new(key, AES.MODE_ECB)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM Passwords WHERE site = ?", (site,))
    row = c.fetchone()
    if row is None:
        return None
    site, encrypted_user, encrypted_password = row
    conn.close()
    decrypted_user = unpad(cipher.decrypt(encrypted_user), AES.block_size).decode()
    decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size).decode()
    with open("D:/pass.log", "w") as f:
        f.write(f"{site}  was read")
    return site, decrypted_user, decrypted_password


def get_all_passwords(db_path, key):
    cipher = AES.new(key, AES.MODE_ECB)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM Passwords")
    rows = c.fetchall()
    passwords = []
    for row in rows:
        site, encrypted_user, encrypted_password = row
        decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size).decode()
        passwords.append((site, decrypted_password))
    conn.close()
    return passwords

def get_all_data(db_path, key):
    cipher = AES.new(key, AES.MODE_ECB)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM Passwords")
    rows = c.fetchall()
    data = []
    for row in rows:
        site, encrypted_user, encrypted_password = row
        decrypted_user = unpad(cipher.decrypt(encrypted_user), AES.block_size).decode()
        decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size).decode()
        data.append((site, decrypted_user, decrypted_password))
    conn.close()
    return data
