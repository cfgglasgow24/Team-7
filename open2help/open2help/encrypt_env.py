"""
This script is single use and meant to encrypt the .env file 
for further security
WARNING: do not overwrite .env file in /app/ directory; data loss
will occurs for keys
"""

from cryptography.fernet import Fernet

# Generate Fernet key [USE ONCE]
def get_fernet():
    key = Fernet.generate_key()

    return key

def get_content():
    with open('.env.encrypted', 'rb') as file:
        content = file.read()

    file.close()

    return content

def encrypt(cipher_suite):
    content = get_content()
    encrypted_content = cipher_suite.encrypt(content)

    with open('.env.encrypted', 'wb') as file:
        file.write(encrypted_content)

    file.close()

def decrypt(cipher_suite):
    # read encrypted contents
    with open('.env.encrypted', 'rb') as file:
        encrypted_content = file.read()

    # replace encrypted contents with decrypted ones
    decrypted_content = cipher_suite.decrypt(encrypted_content)

    # Decrypt contents of .env file
    with open('.env.encrypted', 'wb') as file:
        file.write(decrypted_content)

    file.close()

def main():
    var = str(input("Encrypt or decrypt? [e/d]:"))

    if var == "e":
        encrypt(Fernet(b'wl5CNUsE7fCJ8YA_q9j6ZDiSE8SKzfVh4a4tFZrgAdg='))
    elif var == "d":
        decrypt(Fernet(b'wl5CNUsE7fCJ8YA_q9j6ZDiSE8SKzfVh4a4tFZrgAdg='))

if __name__ == "__main__":
    main()