import serial
import hashlib

# Define the SHA-1 hash function
def sha1(data):
    def left_rotate(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    def process_chunk(chunk, h0, h1, h2, h3, h4):
        w = [0] * 80
        for i in range(16):
            w[i] = chunk[i * 4:i * 4 + 4]
        for i in range(16, 80):
            w[i] = left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

        a, b, c, d, e = h0, h1, h2, h3, h4

        for i in range(80):
            if i < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (left_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF
            e, d, c, b, a = d, c, left_rotate(b, 30), a, temp

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

        return h0, h1, h2, h3, h4

    # Initialize the hash values (constants)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Pre-processing
    message = bytearray(data)
    original_length_bits = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0x00)
    message += original_length_bits.to_bytes(8, byteorder='big')

    # Process the message in 512-bit chunks
    for i in range(0, len(message), 64):
        chunk = message[i:i + 64]
        h0, h1, h2, h3, h4 = process_chunk(chunk, h0, h1, h2, h3, h4)

    # Produce the final hash
    digest = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    return digest.to_bytes(20, byteorder='big')

# Serial port configuration
ser = serial.Serial('/dev/ttyUSB0', 9600)

try:
    helloagreement = ""                                     # Hello agreement for arduino to avoid serial read not starting properly
    ser.write("helloareyouthere?")
    helloagreement = ser.readline().decode('utf-8').strip()

    if (helloagreement == "yesiamhere"):
        ser.write("ecgHighAlarm: ecgLowAlarm: tempHighAlarm: tempLowAlarm: respiHighAlarm: respiLowAlarm:")
    while True:
        data = ser.readline().strip()
        if data:
            # Calculate SHA-1 hash
            hashed_data = sha1(data)
            print(f"Received: {data.decode('utf-8')}")
            print(f"SHA-1 Hash: {hashed_data.hex()}")
except KeyboardInterrupt:
    ser.close()