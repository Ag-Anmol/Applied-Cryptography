'''
Elgamal Digital Signature Scheme Assignment
'''


'''
Assumption user knows the prime numbers and primitive root to enter and co prime numbers. (co-prime condition is handled
in case inputs wrong input)
'''

# Function: Modular Inverse
def mod_inv(a, b):
    """
    Function to calculate the modular inverse of a with respect to b.
    Uses the Extended Euclidean Algorithm to compute gcd(a, b) and 
    coefficients x and y such that ax + by = gcd(a, b).
    """

    if b == 0:
        return a, 1, 0  # Base case: when b = 0, gcd is a, coefficients are 1, 0
    gcd, x, y = mod_inv(b, a % b)  # Recursively calculate the modular inverse
    return gcd, y, (x - (a // b) * y)  # Return gcd and the coefficients

# 1. Key Generation
def generate_keys(p, g):
    """
    Function to generate public and private keys for the ElGamal signature scheme.
    p: a large prime number
    g: a generator of the group Z_p^*
    Returns the public key (p, g, y) and the private key x
    """
    x = int(input(f"Enter the Private key, Xa (in between [2,{p-2}]): "))  # Private key x is a random integer between 1 and p-2
    y = pow(g, x, p)  # Public key y = g^x mod p
    return (p, g, y), x  # Return public key and private key

# 2. Signing a Message
def sign_message(message, private_key, p, g):
    """
    Function to sign a message using the private key in the ElGamal signature scheme.
    message: The message to sign
    private_key: The private key x
    p, g: Public parameters (prime p and generator g)
    Returns the signature (r, s)
    """

    h = message % p  # Reduce the hash value modulo p

    # Step 2: Choose a random k between 1 and p-1 such that gcd(k, p-1) = 1
    while True:
        k = int(input(f"Enter the k which is co-prime with {p-1}: "))  # Random value k in the range [1, p-1]
        if mod_inv(p - 1, k)[0] == 1:  # Check if k is coprime with p-1
            break  # If so, break the loop

    # Step 3: Calculate r = g^k mod p
    r = pow(g, k, p)  # r is g raised to the power of k modulo p

    # Step 4: Calculate the modular inverse of k modulo p-1
    k_inv = mod_inv(k, p - 1)[1]  # Find the modular inverse of k modulo p-1
    if k_inv < 0:  # If the modular inverse is negative, make it positive
        k_inv += p - 1
    
    print(f"k mod inverse {p-1}:",k_inv)

    # Step 5: Calculate s = k^-1 * (h - x * r) mod (p-1)
    s = (k_inv * (h - private_key * r)) % (p - 1)  # Calculate s based on h, r, and private key x

    return (r, s)  # Return the signature (r, s)

# 3. Verifying the Signature
def verify_signature(message, signature, public_key, p, g):
    """
    Function to verify the validity of a signature on a message using the public key.
    message: The message to verify
    signature: The signature (r, s) to verify
    public_key: The public key (p, g, y)
    p, g: Public parameters (prime p and generator g)
    Returns True if the signature is valid, False otherwise
    """
    r, s = signature  # Extract the signature values r and s
    y = public_key[2]  # Public key component y (y = g^x mod p)

    # Step 1: Hash the message (using SHA-256) and reduce it modulo p
    h = message % p  # Reduce the hash value modulo p

    # Step 2: Check if r and s are within valid ranges
    if not (1 <= r < p and 1 <= s < p - 1):  # r and s should be in the range [1, p-1]
        return False  # If not, return False

    # Step 3: Calculate v1 = (y^r * r^s) mod p and v2 = g^h mod p
    v1 = (pow(y, r, p) * pow(r, s, p)) % p  # Calculate v1 using public key y
    v2 = pow(g, h, p)  # Calculate v2 using the generator g and the hashed message

    # Step 4: If v1 == v2, the signature is valid
    print("v1:", v1)  # Print v1 for debugging purposes
    print("v2:", v2)  # Print v2 for debugging purposes

    return v1 == v2  # Return True if the signature is valid, else False

# Main Program
if __name__ == "__main__":
    p = int(input("Enter the prime number(p): "))  # A small prime number (for testing purposes)
    g = int(input(f"Enter the primitive root of {p} (alpha or g): "))  # A generator for the group Z_p^* (primitive root)

    # Key Generation
    print("=" * 19 + "Key Generation" + "=" * 20)
    public_key, private_key = generate_keys(p, g)  # Generate public and private keys
    print(f"Public Key: {public_key}")  # Print the public key
    print(f"Private Key, Xa: {private_key}")  # Print the private key
    print()

    # Signature Generation
    print("=" * 16 + "Signature Generation" + "=" * 16)
    message = int(input("Enter the message (in int): "))  # Get the message to sign
    signature = sign_message(message, private_key, p, g)  # Generate the signature
    print(f"Signature: {signature}")  # Print the signature
    print()

    # Signature Verification
    print("=" * 15 + "Signature Verification" + "=" * 15)
    is_valid = verify_signature(message, signature, public_key, p, g)  # Verify the signature
    print(f"Signature Valid: {is_valid}")  # Print whether the signature is valid
    print()



'''
Example Output :

Enter the prime number(p): 19
Enter the primitive root of 19 (alpha or g): 10
===================Key Generation====================
Enter the Private key, Xa (in between [2,17]): 16
Public Key: (19, 10, 4)
Private Key, Xa: 16

================Signature Generation================
Enter the message (in int): 14
Enter the k which is co-prime with 18: 5
k mod inverse 18: 11
Signature: (3, 4)

===============Signature Verification===============
v1: 16
v2: 16
Signature Valid: True


'''
