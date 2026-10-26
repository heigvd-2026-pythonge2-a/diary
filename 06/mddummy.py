def mddummy(message):
    """Hachage jouet inspiré de MD5. Didactique uniquement, aucune sécurité."""
    if isinstance(message, str):
        message = message.encode("utf-8")

    MASK = 0xFFFFFFFF
    K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a]
    S = [7, 12, 17, 22, 5, 9]

    # 1. Remplissage : 0x80, des zéros, puis la longueur sur 8 octets
    length = (len(message) * 8).to_bytes(8, "little")
    message += b"\x80"
    message += b"\x00" * ((56 - len(message) % 64) % 64)
    message += length

    # 2. État initial : quatre registres de 32 bits
    a0, b0, c0, d0 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476

    # 3. Traitement par blocs de 64 octets (16 mots de 32 bits)
    for off in range(0, len(message), 64):
        M = [int.from_bytes(message[off + 4 * j: off + 4 * j + 4], "little") for j in range(16)]
        A, B, C, D = a0, b0, c0, d0

        for i in range(64):
            # Une fonction booléenne différente par tour de 16 étapes
            if i < 16:
                F = (B & C) | (~B & D)
            elif i < 32:
                F = (D & B) | (~D & C)
            elif i < 48:
                F = B ^ C ^ D
            else:
                F = C ^ (B | (~D & MASK))

            # Mélange : addition, rotation, puis permutation des registres
            F = (F + A + K[i % 6] + M[i % 16]) & MASK
            s = S[i % 6]
            rot = ((F << s) | (F >> (32 - s))) & MASK
            A, B, C, D = D, (B + rot) & MASK, B, C

        # 4. On ajoute le résultat du bloc à l'état courant
        a0, b0, c0, d0 = [(x + y) & MASK for x, y in zip((a0, b0, c0, d0), (A, B, C, D))]

    # 5. Condensat : concaténation des quatre registres
    return b"".join(x.to_bytes(4, "little") for x in (a0, b0, c0, d0)).hex()


if __name__ == "__main__":
    for m in ["", "a", "abc", "abd"]:
        print(repr(m), mddummy(m))
