import sdes

def file_to_string(name_file):
    valeur = ""
    with open(name_file, encoding='utf-8') as f:
        for line in f.readlines():
            if line is not None and line.strip() != "":
                valeur += line
    return valeur

def encrypt_string_2(string, key_1):
    message_crypter = []
    for block in to_binary(string):
        message_crypte = sdes.encrypt(key_1, int(block,2))
        message_crypter.append(bin(message_crypte))
    return message_crypter


def decrypt_string_2(string_crypte, key_1):
    message_decrypter = []
    for block in string_crypte:
        message_decrypte = sdes.decrypt(key_1, int(block,2))
        message_decrypter.append(bin(message_decrypte))
    return message_decrypter

def to_binary(string):
    valeur_ascii, resultat = [],[]
    for i in string:
        valeur_ascii.append(ord(i))
    for i in valeur_ascii:
        resultat.append(bin(i))
    return resultat