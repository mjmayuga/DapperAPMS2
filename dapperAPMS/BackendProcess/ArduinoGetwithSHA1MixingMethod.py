import serial

# Function to perform circular left shift
def circular_left_shift(word, n):           #n is the number of positions to shift
    return ((word << n) | (word >> (32 - n))) & 0xFFFFFFFF

# Function to perform the SHA-1 mixing operation
def sha1_mixing(a, b, c, d, e, word, k):
    f = (b & c) | ((~b) & d)  # Mixing function based on bitwise operations (mixing of b and c)
    temp = (circular_left_shift(a, 5) + f + e + word + k) & 0xFFFFFFFF
    return ((temp + b) & 0xFFFFFFFF, a, circular_left_shift(b, 30), c, d)

# Function to compute the SHA-1 hash of a message
def sha1(message):
    # Initialize constants (5 32-bit words)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Pre-processing
    original_length_bits = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
    message += b'\x80'  # Append a '1' bit followed by zeros

    while len(message) % 64 != 56:
        message += b'\x00'  # Pad with zeros until 448 bits are reached

    message += original_length_bits.to_bytes(8, byteorder='big')  # Append the original message length in bits as an 8-byte value

    # Process the message in 512-bit chunks
    for i in range(0, len(message), 64):
        chunk = message[i:i + 64]

        # Break chunk into 32-bit words
        words = [int.from_bytes(chunk[j:j + 4], 'big') for j in range(0, 64, 4)]

        a, b, c, d, e = h0, h1, h2, h3, h4

        # Main loop
        for i in range(80):
            if i < 20:
                k = 0x5A827999
            elif i < 40:
                k = 0x6ED9EBA1
            elif i < 60:
                k = 0x8F1BBCDC
            else:
                k = 0xCA62C1D6

            # Update hash values using the mixing method
            a, b, c, d, e = sha1_mixing(a, b, c, d, e, words[i], k)

        # Update hash values after processing the chunk
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # Produce the final hash (160 bits)
    return (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4

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

                #calculate SHA-1 hash
                hashed_data = sha1(data)
                print(f"Received: {data.decode('utf-8')}")      #modification needed for transmiting to django and mysql database
                print(f"SHA-1 Hash: {hashed_data:040x}")
except KeyboardInterrupt:
    ser.close()
