from Crypto.Cipher import AES
from scapy.all import IP, UDP, Raw, rdpcap
import main

def pkcs7_unpad(data):
    """ fonction qui permet de supprimer le padding

    Args:
        data (bytes): les données à traiter

    Returns:
        bytes: les données sans le padding
    """
    padding_size = data[-1]

    if all(i == padding_size for i in data[-padding_size:]):
        return data[:-padding_size]
    else:
        return data

def encrypt_messages(trace_path):
    """ fonction qui permet de crypter les messages

    Args:
        trace_path (str): le chemin du fichier trace a crypter

    Returns:
        list: les messages cryptés
    """
    encrypted_messages = []
    packets = rdpcap(trace_path)

    for packet in packets:
        if IP in packet and UDP in packet[IP] and packet[IP].dport == 9999:
            iv_and_message = bytes(packet[Raw].load)
            iv = iv_and_message[:16]
            encrypted_message = iv_and_message[16:]

            encrypted_messages.append((iv, encrypted_message))

    return encrypted_messages

def decrypt_messages(key, encrypted_messages):
    """ fonction qui permet de décrypter les messages

    Args:
        key (int): la clé de décryptage
        encrypted_messages (str): les messages à décrypter

    Returns:
        list: les messages décryptés 
    """
    decrypted_messages = []

    for iv, encrypted_message in encrypted_messages:
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        padded_message = cipher.decrypt(encrypted_message)
        message = pkcs7_unpad(padded_message)

        decrypted_messages.append(message)

    return decrypted_messages

if __name__ == "__main__":
    """ fonction qui permet de tester les fonctions de ce fichier """
    
    rossignol2 = main.open_image("./docs/rossignol2.bmp")

    original_key = ""

    if rossignol2:
        original_key = main.last_bit(rossignol2)
        original_key = "".join(original_key)

    for i in range(2):
        original_key += original_key

    key = int(original_key, 2).to_bytes(len(original_key) // 8, byteorder='big')

    encrypted_messages = encrypt_messages("./docs/trace_sae.cap")
    print(encrypted_messages)

    decrypted_messages = decrypt_messages(key, encrypted_messages)

    for message in decrypted_messages:
        print(message.decode('utf-8'))
