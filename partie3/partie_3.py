import dpkt
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import main


def encrypt_messages(trace_path):
    encrypted_messages = []

    with open(trace_path, 'rb') as file:
        pcap = dpkt.pcap.Reader(file)

        for _, packet in pcap:
            eth = dpkt.ethernet.Ethernet(packet)

            if isinstance(eth.data, dpkt.ip.IP) and isinstance(
                    eth.data.data, dpkt.udp.UDP):
                udp = eth.data.data
                if udp.dport == 9999:
                    iv_and_message = udp.data
                    iv = iv_and_message[:16]
                    encrypted_message = iv_and_message[16:]

                    encrypted_messages.append((iv, encrypted_message))

    return encrypted_messages


def decrypt_messages(key, encrypted_messages):
    decrypted_messages = []

    for iv, encrypted_message in encrypted_messages:
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        padded_message = cipher.decrypt(encrypted_message)
        message = unpad(padded_message, AES.block_size)

        decrypted_messages.append(message)

    return decrypted_messages


if __name__ == "__main__":

    rossignol2 = main.open_image("./docs/rossignol2.bmp")

    original_key = ""

    if rossignol2:
        original_key = main.last_bit(rossignol2)
        original_key = "".join(original_key)

    for i in range(2):
        original_key += original_key

    key = int(original_key, 2).to_bytes(len(original_key) // 8,
                                        byteorder='big')

    encrypted_messages = encrypt_messages("./docs/trace_sae.cap")
    print(encrypted_messages)

    decrypted_messages = decrypt_messages(key, encrypted_messages)

    for message in decrypted_messages:
        print(message.decode('utf-8'))
