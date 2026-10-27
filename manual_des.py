# Initial Permutation (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Final Permutation (IP^-1)
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Permuted Choice 1 (PC-1)
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Permuted Choice 2 (PC-2)
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Number of left shifts for each round
SHIFT_SCHEDULE = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]

# Expansion permutation (E)
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# Permutation P
P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

# DES S-Boxes
S_BOXES = [
    [
        [14, 4,  13, 1,  2,  15, 11, 8,  3,  10, 6,  12, 5,  9,  0,  7],
        [0,  15, 7,  4,  14, 2,  13, 1,  10, 6,  12, 11, 9,  5,  3,  8],
        [4,  1,  14, 8,  13, 6,  2,  11, 15, 12, 9,  7,  3,  10, 5,  0],
        [15, 12, 8,  2,  4,  9,  1,  7,  5,  11, 3,  14, 10, 0,  6,  13]
    ],
    [
        [15, 1,  8,  14, 6,  11, 3,  4,  9,  7,  2,  13, 12, 0,  5,  10],
        [3,  13, 4,  7,  15, 2,  8,  14, 12, 0,  1,  10, 6,  9,  11, 5],
        [0,  14, 7,  11, 10, 4,  13, 1,  5,  8,  12, 6,  9,  3,  2,  15],
        [13, 8,  10, 1,  3,  15, 4,  2,  11, 6,  7,  12, 0,  5,  14, 9]
    ],
    [
        [10, 0,  9,  14, 6,  3,  15, 5,  1,  13, 12, 7,  11, 4,  2,  8],
        [13, 7,  0,  9,  3,  4,  6,  10, 2,  8,  5,  14, 12, 11, 15, 1],
        [13, 6,  4,  9,  8,  15, 3,  0,  11, 1,  2,  12, 5,  10, 14, 7],
        [1,  10, 13, 0,  6,  9,  8,  7,  4,  15, 14, 3,  11, 5,  2,  12]
    ],
    [
        [7,  13, 14, 3,  0,  6,  9,  10, 1,  2,  8,  5,  11, 12, 4,  15],
        [13, 8,  11, 5,  6,  15, 0,  3,  4,  7,  2,  12, 1,  10, 14, 9],
        [10, 6,  9,  0,  12, 11, 7,  13, 15, 1,  3,  14, 5,  2,  8,  4],
        [3,  15, 0,  6,  10, 1,  13, 8,  9,  4,  5,  11, 12, 7,  2,  14]
    ],
    [
        [2,  12, 4,  1,  7,  10, 11, 6,  8,  5,  3,  15, 13, 0,  14, 9],
        [14, 11, 2,  12, 4,  7,  13, 1,  5,  0,  15, 10, 3,  9,  8,  6],
        [4,  2,  1,  11, 10, 13, 7,  8,  15, 9,  12, 5,  6,  3,  0,  14],
        [11, 8,  12, 7,  1,  14, 2,  13, 6,  15, 0,  9,  10, 4,  5,  3]
    ],
    [
        [12, 1,  10, 15, 9,  2,  6,  8,  0,  13, 3,  4,  14, 7,  5,  11],
        [10, 15, 4,  2,  7,  12, 9,  5,  6,  1,  13, 14, 0,  11, 3,  8],
        [9,  14, 15, 5,  2,  8,  12, 3,  7,  0,  4,  10, 1,  13, 11, 6],
        [4,  3,  2,  12, 9,  5,  15, 10, 11, 14, 1,  7,  6,  0,  8,  13]
    ],
    [
        [4,  11, 2,  14, 15, 0,  8,  13, 3,  12, 9,  7,  5,  10, 6,  1],
        [13, 0,  11, 7,  4,  9,  1,  10, 14, 3,  5,  12, 2,  15, 8,  6],
        [1,  4,  11, 13, 12, 3,  7,  14, 10, 15, 6,  8,  0,  5,  9,  2],
        [6,  11, 13, 8,  1,  4,  10, 7,  9,  5,  0,  15, 14, 2,  3,  12]
    ],
    [
        [13, 2,  8,  4,  6,  15, 11, 1,  10, 9,  3,  14, 5,  0,  12, 7],
        [1,  15, 13, 8,  10, 3,  7,  4,  12, 5,  6,  11, 0,  14, 9,  2],
        [7,  11, 4,  1,  9,  12, 14, 2,  0,  6,  10, 13, 15, 3,  5,  8],
        [2,  1,  14, 7,  4,  10, 8,  13, 15, 12, 9,  0,  3,  5,  6,  11]
    ]
]


# HELPER FUNCTIONS
def permute(block, table):
    return ''.join(block[i - 1] for i in table)


def xor_bits(a, b):
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))


def left_shift(bits, count):
    return bits[count:] + bits[:count]


def ascii_key_to_hex(key_ascii: str) -> str:

    if not isinstance(key_ascii, str):
        raise TypeError("Key harus string ASCII")
    if len(key_ascii) != 8:
        raise ValueError(
            f"Key DES harus tepat 8 karakter ASCII, dapat {len(key_ascii)}: {key_ascii!r}"
        )
    try:
        key_bytes = key_ascii.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError(f"Key harus ASCII murni, dapat: {key_ascii!r}")
    return key_bytes.hex().upper()


# KEY SCHEDULE
def generate_round_keys(key_hex: str):
    """Generate 16 round key dari key hex (16 char)."""
    if len(key_hex) != 16:
        raise ValueError(f"Key hex harus 16 karakter, dapat {len(key_hex)}")

    key_bin = bin(int(key_hex, 16))[2:].zfill(64)

    key_56 = permute(key_bin, PC1)

    C = key_56[:28]
    D = key_56[28:]

    round_keys = []

    for shift in SHIFT_SCHEDULE:
        C = left_shift(C, shift)
        D = left_shift(D, shift)

        combined = C + D

        round_key = permute(combined, PC2)

        round_keys.append(round_key)

    return round_keys



# S-BOX SUBSTITUTION
def sbox_substitution(bits):
    """48-bit → 32-bit via 8 S-Box."""
    result = ""

    for i in range(8):
        block = bits[i * 6:(i + 1) * 6]

        row = int(block[0] + block[5], 2)
        column = int(block[1:5], 2)

        value = S_BOXES[i][row][column]

        result += bin(value)[2:].zfill(4)

    return result


# FEISTEL FUNCTION
def feistel(right, round_key):
    expanded = permute(right, E)
    xored = xor_bits(expanded, round_key)
    substituted = sbox_substitution(xored)
    result = permute(substituted, P)
    return result


# DES BLOCK (Encrypt / Decrypt)
def des_block(block_hex, round_keys):
    if len(block_hex) != 16:
        raise ValueError(f"Block hex harus 16 karakter, dapat {len(block_hex)}")

    block_bin = bin(int(block_hex, 16))[2:].zfill(64)

    permuted = permute(block_bin, IP)

    left = permuted[:32]
    right = permuted[32:]

    for round_key in round_keys:
        new_left = right
        new_right = xor_bits(left, feistel(right, round_key))

        left = new_left
        right = new_right

    combined = right + left

    result = permute(combined, FP)

    return hex(int(result, 2))[2:].upper().zfill(16)


def encrypt_block(plaintext_hex, key_hex):
    round_keys = generate_round_keys(key_hex)
    return des_block(plaintext_hex, round_keys)


def decrypt_block(ciphertext_hex, key_hex):
    round_keys = generate_round_keys(key_hex)
    round_keys.reverse()
    return des_block(ciphertext_hex, round_keys)


# PADDING PKCS#5
def pad_data(data: bytes) -> bytes:
    padding_length = 8 - (len(data) % 8)
    return data + bytes([padding_length]) * padding_length


def unpad_data(data: bytes) -> bytes:
    if not data:
        raise ValueError("Data kosong, tidak ada padding")

    padding_length = data[-1]

    if padding_length < 1 or padding_length > 8:
        raise ValueError(f"Padding tidak valid: {padding_length}")

    if data[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Padding tidak konsisten (mungkin key salah)")

    return data[:-padding_length]


# ENKRIPSI / DEKRIPSI TEKS (Format Tugas: ASCII key, Hex ciphertext)
def encrypt_text(text: str, key_ascii: str) -> str:
    
    if not isinstance(text, str):
        raise TypeError("Plaintext harus string ASCII")

    key_hex = ascii_key_to_hex(key_ascii)

    data = text.encode("ascii")
    data = pad_data(data)

    ciphertext = ""

    for i in range(0, len(data), 8):
        block = data[i:i + 8]
        block_hex = block.hex().upper()
        encrypted_block = encrypt_block(block_hex, key_hex)
        ciphertext += encrypted_block

    return ciphertext


def decrypt_text(ciphertext_hex: str, key_ascii: str) -> str:
    
    if not isinstance(ciphertext_hex, str):
        raise TypeError("Ciphertext harus Hex string")

    ciphertext_hex = ciphertext_hex.strip().replace(" ", "").upper()

    if len(ciphertext_hex) % 16 != 0:
        raise ValueError(
            f"Panjang ciphertext Hex harus kelipatan 16, dapat {len(ciphertext_hex)}"
        )

    key_hex = ascii_key_to_hex(key_ascii)

    decrypted_data = bytearray()

    for i in range(0, len(ciphertext_hex), 16):
        block_hex = ciphertext_hex[i:i + 16]
        decrypted_block = decrypt_block(block_hex, key_hex)
        decrypted_data.extend(bytes.fromhex(decrypted_block))

    decrypted_data = unpad_data(decrypted_data)

    return decrypted_data.decode("ascii")



if __name__ == "__main__":
    print()
    print("=" * 60)
    print("TEST DES MANUAL")
    print("=" * 60)

    print("\n[1] Test Vector FIPS 46-3")
    pt_hex = "0123456789ABCDEF"
    key_hex = "133457799BBCDFF1"
    expected = "85E813540F0AB405"

    result = encrypt_block(pt_hex, key_hex)
    print(f"    Plaintext  : {pt_hex}")
    print(f"    Key        : {key_hex}")
    print(f"    Expected   : {expected}")
    print(f"    Got        : {result}")
    print(f"    Status     : {'PASS' if result == expected else 'FAIL'}")


    print("\n[2] Enkripsi & Dekripsi Text (Key ASCII, Ciphertext Hex)")
    key_ascii = "AliceKey"   # 8 karakter ASCII, bisa diubah
    message = "Halo Semuanya, semangat bergembira!"

    print(f"    Original   : {message}")
    print(f"    Key (ASCII): {key_ascii}")

    ciphertext = encrypt_text(message, key_ascii)
    print(f"    Ciphertext : {ciphertext}")

    decrypted = decrypt_text(ciphertext, key_ascii)
    print(f"    Decrypted  : {decrypted}")

    print(f"    Status     : {'PASS' if decrypted == message else 'FAIL'}")

    print("\n" + "=" * 60)
    ok1 = (result == expected)
    ok2 = (decrypted == message)
    if ok1 and ok2:
        print("HASIL: SEMUA TEST LULUS ")
    else:
        print("HASIL: ADA TEST GAGAL ")
    print("=" * 60)