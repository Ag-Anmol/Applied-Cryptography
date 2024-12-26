"""
AES Block Cipher Encryption Assignment
"""


# AES S-Box and Inverse S-Box
S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]

# Round constants used in key expansion
RCON = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
]

# Function to perform byte substitution (SubBytes)
def sub_bytes(state):
    return [[S_BOX[b] for b in row] for row in state]  # Substitute each byte using S_BOX

# Function to shift rows (ShiftRows)
def shift_rows(state):
    for r in range(1, 4):  # Shift rows 1 to 3
        state[r] = state[r][r:] + state[r][:r]  # Circular shift
    return state

# Function to mix columns (MixColumns)
def mix_columns(state):
    new_state = [[0] * 4 for _ in range(4)]  # Initialize new state
    for c in range(4):  # For each column
        new_state[0][c] = (mul(0x02, state[0][c]) ^ mul(0x03, state[1][c]) ^ state[2][c] ^ state[3][c]) % 256
        new_state[1][c] = (state[0][c] ^ mul(0x02, state[1][c]) ^ mul(0x03, state[2][c]) ^ state[3][c]) % 256
        new_state[2][c] = (state[0][c] ^ state[1][c] ^ mul(0x02, state[2][c]) ^ mul(0x03, state[3][c])) % 256
        new_state[3][c] = (mul(0x03, state[0][c]) ^ state[1][c] ^ state[2][c] ^ mul(0x02, state[3][c])) % 256
    return new_state

# Function to multiply two bytes in GF(2^8)
def mul(x, y):
    result = 0
    while y:
        if y & 1:  # If the least significant bit is set
            result ^= x  # Add x to result
        x = (x << 1) ^ (0x1b if x & 0x80 else 0)  # Shift x and apply reduction if necessary
        y >>= 1  # Shift y to the right
    return result

# Key expansion function to generate round keys from the original key
def key_expansion(key):
    round_keys = [key[i:i + 4] for i in range(0, 16, 4)]  # Initial 4 round keys from the key
    for i in range(4, 44):  # Generate keys up to 44 (10 rounds + 1)
        temp = round_keys[i - 1][:]  # Copy the last round key
        if i % 4 == 0:  # Every 4th key requires special processing
            temp = [S_BOX[b] for b in temp[1:] + temp[:1]]  # Rotate and substitute
            temp[0] ^= RCON[i // 4 - 1]  # Apply the round constant
        rk = [round_keys[i - 4][j] ^ temp[j] for j in range(4)]  # XOR with the previous round key
        round_keys.append(rk)  # Append the new round key
    return [round_keys[i:i + 4] for i in range(0, len(round_keys), 4)]  # Return round keys as 4x4 arrays

# Function to transpose the state
def transpose(state):
    return [[state[r][c] for r in range(4)] for c in range(4)]  # Swap rows and columns

# Function to add round key (XOR operation)
def add_round_key(state, round_key):
    return [[state[r][c] ^ round_key[r][c] for c in range(4)] for r in range(4)]  # XOR each byte

# Function to print the state in a readable format
def print_state(state, round_num, func):
    print(f"State: round-{round_num}: {func}:")
    for row in state:
        print(" ".join(f"{b:02x}" for b in row))  # Print each byte in hex
    print()

# AES encryption function
def aes_encrypt(plaintext, key, rounds=10):
    # Ensure the plaintext and key are both 16 bytes (128 bits)
    if len(plaintext) != 16 or len(key) != 16:
        raise ValueError("Both plaintext and key must be 16 bytes (128 bits).")

    # Initial setup
    state = [list(plaintext[i:16:4]) for i in range(0, 4)]  # Convert plaintext to state array (4x4)
    round_keys = key_expansion(key)  # Generate round keys
    print_state(state, 0, 'start round')

    # Initial round
    state = add_round_key(state, transpose(round_keys[0]))  # Add the first round key
    print_state(state, 0, 'round key')

    # 9 main rounds
    for i in range(1, rounds + 1):
        state = sub_bytes(state)  # Apply SubBytes transformation
        print_state(state, i, 'sub bytes')
        
        state = shift_rows(state)  # Apply ShiftRows transformation
        print_state(state, i, 'shift rows')
        
        if i != 10:  # MixColumns only in the first 9 rounds
            state = mix_columns(state)
            print_state(state, i, 'mix columns')
        
        k = transpose(round_keys[i])  # Get the round key for this round
        print_state(k, i, 'round key')
        state = add_round_key(state, k)  # Add the round key
        print_state(state, i + 1, 'start state')

    return transpose(state)  # Return the final state transposed

# Main function to handle user input and invoke AES encryption
def main():
    # Input from user
    plaintext = input("Enter 16-byte plaintext (in hex): ").replace(" ", "")  # Read and format plaintext
    key = input("Enter 16-byte key (in hex): ").replace(" ", "")  # Read and format key
    rounds = int(input("Enter the number of rounds (in int <= 10 and >0): "))  # Read number of rounds

    # Convert hex to byte arrays
    plaintext_bytes = [int(plaintext[i:i + 2], 16) for i in range(0, len(plaintext), 2)]
    key_bytes = [int(key[i:i + 2], 16) for i in range(0, len(key), 2)]

    # Ensure correct sizes
    if len(plaintext_bytes) != 16 or len(key_bytes) != 16:
        print("Both plaintext and key must be 16 bytes.")
        return

    # Encrypt the plaintext
    ciphertext = aes_encrypt(plaintext_bytes, key_bytes, rounds)

    # Convert ciphertext to hex and print
    ciphertext_hex = ''.join(f'{byte:02x}' for row in ciphertext for byte in row)
    print("Ciphertext (hex):", ciphertext_hex)

# Entry point of the script
if __name__ == "__main__":
    main()
