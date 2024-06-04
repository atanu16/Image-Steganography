import cv2
import string
import os

d = {}
c = {}

for i in range(256):
    d[chr(i % 256)] = i
    c[i] = chr(i % 256)

# Define encryption function
def encrypt_image(x, key, text):
    kl = 0
    z = 0  # decides plane
    n = 0  # number of row
    m = 0  # number of column

    l = len(text)
    length_bytes = l.to_bytes(4, 'big')  # Convert length to 4 bytes

    # Calculate a simple checksum of the key
    key_checksum = sum(d[char] for char in key) % 256

    # Hide the key checksum first
    x[n, m, z] = key_checksum
    n += 1
    if n == x.shape[0]:
        n = 0
        m += 1
        if m == x.shape[1]:
            m = 0
            z += 1
            if z == 3:
                raise ValueError("Image too small to hide data")

    # Hide the length of the text
    for byte in length_bytes:
        x[n, m, z] = byte ^ d[key[kl]]
        kl = (kl + 1) % len(key)
        n += 1
        if n == x.shape[0]:
            n = 0
            m += 1
            if m == x.shape[1]:
                m = 0
                z += 1
                if z == 3:
                    raise ValueError("Image too small to hide data")

    # Hide the actual text
    kl = 0
    for i in range(l):
        x[n, m, z] = d[text[i]] ^ d[key[kl]]
        kl = (kl + 1) % len(key)
        n += 1
        if n == x.shape[0]:
            n = 0
            m += 1
            if m == x.shape[1]:
                m = 0
                z += 1
                if z == 3:
                    raise ValueError("Image too small to hide data")

    cv2.imwrite("encrypted_img.jpg", x)
    os.startfile("encrypted_img.jpg")
    print("Data Hiding in Image completed successfully.")

# Define decryption function
def decrypt_image(x, key):
    kl = 0
    z = 0  # decides plane
    n = 0  # number of row
    m = 0  # number of column

    # Extract the key checksum
    extracted_checksum = x[n, m, z]
    n += 1
    if n == x.shape[0]:
        n = 0
        m += 1
        if m == x.shape[1]:
            m = 0
            z += 1
            if z == 3:
                raise ValueError("Error extracting checksum")

    # Calculate the expected checksum
    expected_checksum = sum(d[char] for char in key) % 256

    if extracted_checksum != expected_checksum:
        raise ValueError("Wrong key")

    length_bytes = bytearray()
    for _ in range(4):  # Extract the length of the hidden text
        length_bytes.append(x[n, m, z] ^ d[key[kl]])
        kl = (kl + 1) % len(key)
        n += 1
        if n == x.shape[0]:
            n = 0
            m += 1
            if m == x.shape[1]:
                m = 0
                z += 1
                if z == 3:
                    raise ValueError("Error extracting length")

    text_length = int.from_bytes(length_bytes, 'big')
    decrypt = ""

    for _ in range(text_length):  # Extract the actual hidden text
        decrypted_value = x[n, m, z] ^ d[key[kl]]
        if decrypted_value in c:
            decrypt += c[decrypted_value]
        else:
            raise ValueError(f"Decrypted value {decrypted_value} out of bounds")
        kl = (kl + 1) % len(key)
        n += 1
        if n == x.shape[0]:
            n = 0
            m += 1
            if m == x.shape[1]:
                m = 0
                z += 1
                if z == 3:
                    raise ValueError("Error extracting text")

    return decrypt

# Load the image
x = cv2.imread("1.jpg")
i = x.shape[0]
j = x.shape[1]
print(f"Image dimensions: {i} x {j}")

def print_menu():
    print("\n" + "="*40)
    print("     IMAGE STEGANOGRAPHY TOOL")
    print("="*40)
    print("1. Encrypt Text in Image")
    print("2. Decrypt Text from Image")
    print("3. Exit")
    print("="*40)

while True:
    print_menu()
    choice = int(input("Enter your choice: "))
    if choice == 1:
        key = input("Enter key to edit (Security Key): ")
        text = input("Enter text to hide: ")
        encrypt_image(x, key, text)

    elif choice == 2:
        key1 = input("Re-enter key to extract text: ")
        try:
            decrypted_text = decrypt_image(x, key1)
            print("Encrypted text was: ", decrypted_text)
        except ValueError as e:
            print(e)

    elif choice == 3:
        print("Exiting.")
        break

    else:
        print("Invalid choice. Please try again.")

