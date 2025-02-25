# Message Digest Algorithm 5

## Mathematical Foundation

The MD5 algorithm follows the classic Merkle–Damgård construction which forms the foundation of many cryptographic hash functions. It processes messages in blocks of 512 bits (64 bytes), transforming each through a compression function that uses an internal state of 128 bits (represented as four 32-bit words A, B, C, D).

The core mathematical operations in MD5 are:

1. **Initialization Vector (IV)**: The constants A, B, C, D (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476) initialize the state.

2. **Message Padding**: The algorithm pads the message to ensure its length is congruent to 448 modulo 512 bits. This is accomplished by appending a '1' bit followed by enough '0' bits, then adding the original message length as a 64-bit value.

3. **Compression Function**: Each 512-bit block updates the state through 64 steps divided into four rounds of 16 operations. Each operation is of the form:
   ```
   a = b + ((a + F(b,c,d) + X[k] + T[i]) <<< s)
   ```
   Where F is one of four nonlinear functions, X[k] is a message word, T[i] is a precomputed constant, and <<< s represents left rotation by s bits.

4. **The Four Nonlinear Functions**:
   - F(x,y,z) = (x & y) | (~x & z) [bitwise: OR of AND operations]
   - G(x,y,z) = (x & z) | (y & ~z) [similar to F but with different variables]
   - H(x,y,z) = x ⊕ y ⊕ z [bitwise XOR, a parity function]
   - I(x,y,z) = y ⊕ (x | ~z) [a nonlinear function designed for diffusion]

## Cryptographic Vulnerabilities

MD5's mathematical weaknesses primarily stem from:

1. **Insufficient Diffusion**: The algorithm doesn't propagate changes efficiently enough between message blocks.

2. **Differential Cryptanalysis**: Wang et al. discovered that carefully crafted differences in input can be controlled to produce identical hashes.

3. **Limited State Size**: The 128-bit state is too small by modern standards, making collision finding feasible with current computing power.

## Chosen-Prefix Collision Attack

A chosen-prefix collision attack is particularly powerful because it allows an attacker to create two files with arbitrary distinct prefixes that hash to the same value.

Please make one and PR this repo
