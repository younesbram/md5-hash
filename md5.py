# Bare-bones MD5 implementation - ultra fast with no external dependencies

# MD5 constants
A, B, C, D = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

# Precomputed T table
T = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
]

# Shift amounts
S = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]

# Index mapping for message block access
IDX = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12,
    5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2,
    0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9
]

# Fast rotate left
def rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

# Core functions
def F(x, y, z): return (x & y) | (~x & z)
def G(x, y, z): return (x & z) | (y & ~z)
def H(x, y, z): return x ^ y ^ z
def I(x, y, z): return y ^ (x | ~z)

# Core functions as array for fast lookup
FUNCS = [F, G, H, I]

def md5_block(block, state):
    """Process a single 64-byte block"""
    a, b, c, d = state
    
    # Convert block to 16 little-endian words
    X = []
    for i in range(0, 64, 4):
        val = block[i] | (block[i+1] << 8) | (block[i+2] << 16) | (block[i+3] << 24)
        X.append(val)
    
    # Main loop
    aa, bb, cc, dd = a, b, c, d
    
    for i in range(64):
        round_idx = i >> 4  # Fast integer division by 16
        f = FUNCS[round_idx](bb, cc, dd)
        
        temp = (aa + f + T[i] + X[IDX[i]]) & 0xFFFFFFFF
        temp = rotl(temp, S[i])
        temp = (temp + bb) & 0xFFFFFFFF
        
        aa, bb, cc, dd = dd, temp, bb, cc
    
    # Add result to state
    return (
        (a + aa) & 0xFFFFFFFF,
        (b + bb) & 0xFFFFFFFF,
        (c + cc) & 0xFFFFFFFF,
        (d + dd) & 0xFFFFFFFF
    )

def md5(message):
    """Compute MD5 of a message (string or bytes)"""
    # Convert to bytes if string
    if isinstance(message, str):
        message = bytearray(message.encode())
    elif not isinstance(message, bytearray):
        message = bytearray(message)
    
    # Initialize state
    state = (A, B, C, D)
    
    # Get message length in bits
    msg_len_bits = len(message) * 8
    
    # Padding: append bit 1 followed by zeros
    message.append(0x80)
    while (len(message) % 64) != 56:
        message.append(0)
    
    # Append length as little-endian 64-bit value
    message.extend(msg_len_bits.to_bytes(8, byteorder='little'))
    
    # Process message in 64-byte blocks
    for i in range(0, len(message), 64):
        state = md5_block(message[i:i+64], state)
    
    # Convert state to hex
    return ''.join(x.to_bytes(4, byteorder='little').hex() for x in state)

def md5_file(filename):
    """Compute MD5 of a file by reading it in chunks"""
    # Initialize state
    state = (A, B, C, D)
    file_size = 0
    
    # Process file in chunks
    chunk_size = 8192  # 8KB for efficient I/O
    remainder = bytearray()
    
    try:
        with open(filename, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                
                file_size += len(data)
                data = remainder + data
                remainder = bytearray()
                
                # Process complete 64-byte blocks
                for i in range(0, len(data) // 64 * 64, 64):
                    state = md5_block(data[i:i+64], state)
                
                # Keep remainder for next iteration
                remainder = data[len(data) // 64 * 64:]
        
        # Final padding
        remainder.append(0x80)
        
        # If we can't fit length in this block, pad and process it first
        if len(remainder) > 56:
            remainder.extend(b'\x00' * (64 - len(remainder)))
            state = md5_block(remainder, state)
            remainder = bytearray()
        
        # Pad to 56 bytes
        remainder.extend(b'\x00' * (56 - len(remainder)))
        
        # Append length (64 bits)
        bit_len = (file_size * 8) & 0xFFFFFFFFFFFFFFFF
        remainder.extend(bit_len.to_bytes(8, byteorder='little'))
        
        # Process final block
        state = md5_block(remainder, state)
        
        # Convert to hex
        return ''.join(x.to_bytes(4, byteorder='little').hex() for x in state)
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Test vector
        test = "hello world"
        print(f"MD5 of '{test}': {md5(test)}")
    else:
        # File hash
        filename = sys.argv[1]
        print(f"Calculating MD5 of file: {filename}")
        hash_result = md5_file(filename)
        if hash_result:
            print(f"MD5: {hash_result}")
