from modules import passwordcheck, clipboardautoclear, generate, trust, savepassword, key
import os
import getpass

def secure_getpass(prompt):
    return getpass.getpass(prompt)

run = True
key_file_path = os.path.join("D:/", '.env')
db_path = "D:/passwords.db"

user_password = secure_getpass("Enter a password to protect the key: ")
pkey = key.keys(key_file_path, user_password)
if pkey == "Incorrect password":
    print("Incorrect password. Exiting.")
    exit()
max_attempts = 1
attempts = 0
# Main loop
while run:
    try:
        trust_manager = trust.DeviceTrustManager()
        run = trust_manager.assess_device_trust()
        if not run:
            attempts += 1
            if attempts >= max_attempts:
                print("Exiting.")
                break
        toiminto = input("Function (copy (c), save (s), quit (q), check password strength (p), get all (g)) ")

        valid_commands = ["c", "s", "q", "p", "g"]
        if toiminto not in valid_commands:
            print("Invalid command.")
            break
        else:
            def get_password(site):
                if not site:
                    print("Site cannot be empty.")
                    return
                return savepassword.decrypt_password_from_db(site, db_path, pkey)
            if toiminto == "c":
                site = input("Site ")
                print(get_password(site))
            elif toiminto == "s":
                site = input("Site ")
                user = input("User ")
                while True:
                    genereoi = input("Generate or own password (g/o) ")
                    if genereoi.lower() not in ["g", "o"]:
                        print("Invalid input. Please enter 'g' for generate or 'o' for own password.")
                        continue
                    if genereoi == "g":
                        salasana = generate.main()
                        break
                    elif genereoi == "o":
                        salasana = secure_getpass("Password ")
                        while passwordcheck.password_strength(salasana) != 'Strong password':
                            passwordcheck.check_passwords(salasana)
                            salasana = secure_getpass("Password ")
                        break
                savepassword.save_password_to_db(site, user, salasana, db_path, pkey)
                print("Saved")
            elif toiminto == "p":
                passwords = savepassword.get_all_passwords(db_path, pkey)
                for password_info in passwords:
                    site, password = password_info
                    count = passwordcheck.pwned_api_check(password)
                    if count:
                        print(f'Password for {site} was found {count} times... you should probably change your password')
            elif toiminto == "g":
                print(savepassword.get_all_data(db_path, pkey))
            elif toiminto == "q":
                break
            key.hide_file(key_file_path)
            key.hide_file(db_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        continue

clipboardautoclear.main()