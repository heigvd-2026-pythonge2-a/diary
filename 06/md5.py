"""MD5 (RFC 1321) en Python pur, sans aucune bibliothèque."""

# Décalages de rotation par tour (4 tours de 16 opérations)
S = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

# Constantes K[i] = floor(abs(sin(i + 1)) * 2^32), précalculées pour éviter math
K = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
]

MASK = 0xFFFFFFFF


def _rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & MASK


def _pad(message):
    bit_len = (len(message) * 8) & 0xFFFFFFFFFFFFFFFF
    message += b"\x80"
    message += b"\x00" * ((56 - len(message) % 64) % 64)
    return message + bit_len.to_bytes(8, "little")


def md5(message):
    if isinstance(message, str):
        message = message.encode("utf-8")

    a0, b0, c0, d0 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
    data = _pad(bytes(message))

    for off in range(0, len(data), 64):
        M = [int.from_bytes(data[off + 4 * j: off + 4 * j + 4], "little") for j in range(16)]
        A, B, C, D = a0, b0, c0, d0

        for i in range(64):
            if i < 16:
                F, g = (B & C) | (~B & D), i
            elif i < 32:
                F, g = (D & B) | (~D & C), (5 * i + 1) % 16
            elif i < 48:
                F, g = B ^ C ^ D, (3 * i + 5) % 16
            else:
                F, g = C ^ (B | (~D & MASK)), (7 * i) % 16

            F = (F + A + K[i] + M[g]) & MASK
            A, D, C = D, C, B
            B = (B + _rotl(F, S[i])) & MASK

        a0 = (a0 + A) & MASK
        b0 = (b0 + B) & MASK
        c0 = (c0 + C) & MASK
        d0 = (d0 + D) & MASK

    return b"".join(x.to_bytes(4, "little") for x in (a0, b0, c0, d0))


def md5_hex(message):
    return md5(message).hex()


if __name__ == "__main__":
    # Vecteurs de test officiels de la RFC 1321
    vectors = {
        "": "d41d8cd98f00b204e9800998ecf8427e",
        "a": "0cc175b9c0f1b6a831c399e269772661",
        "abc": "900150983cd24fb0d6963f7d28e17f72",
        "message digest": "f96b697d7cb7938d525a2f31aaf161d0",
        "abcdefghijklmnopqrstuvwxyz": "c3fcd3d76192e4007dfb496cca67e13b",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
            "d174ab98d277d9f5a5611c2c9f419d9f",
        "1234567890" * 8: "57edf4a22be3c955ac49da2e2107b67a",
    }
    for msg, expected in vectors.items():
        got = md5_hex(msg)
        print(("OK  " if got == expected else "FAIL"), got, repr(msg[:30]))
