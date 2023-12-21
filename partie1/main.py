import sdes

def to_binary(string):
    """ fonction qui permet de convertir un string en binaire

    Args:
        string (str): le string à convertir

    Returns:
        list: le string converti en binaire
    """
    valeur_ascii, resultat = [],[]
    for i in string:
        valeur_ascii.append(ord(i))
    for i in valeur_ascii:
        resultat.append(bin(i))
    return resultat


def to_string(binary):
    """ fonction qui permet de convertir un binaire en string

    Args:
        binary (list): le binaire à convertir

    Returns:
        str: le binaire converti en string
    """
    return ''.join(chr(int(chunk, 2)) for chunk in binary)
    

def file_to_string(name_file):
    """ fonction qui permet de lire un fichier et de le convertir en string

    Args:
        name_file (str): le nom du fichier

    Returns:
        str: le contenu du fichier
    """
    valeur = ""
    with open(name_file, encoding='utf-8') as f:
        for line in f.readlines():
            if line is not None and line.strip() != "":
                valeur += line
    return valeur

def encrypt_string_2(string, key_1):
    """ fonction qui permet de crypter un string

    Args:
        string (str): le string à crypter
        key_1 (int): la clé de cryptage

    Returns:
        list: le string crypté
    """
    message_crypter = []
    for block in to_binary(string):
        message_crypte = sdes.encrypt(key_1, int(block,2))
        message_crypter.append(bin(message_crypte))
    return message_crypter


def decrypt_string_2(string_crypte, key_1):
    """ fonction qui permet de décrypter un string

    Args:
        string_crypte (str): le string à décrypter
        key_1 (int): la clé de décryptage

    Returns:
        list: le string décrypté
    """
    message_decrypter = []
    for block in string_crypte:
        message_decrypte = sdes.decrypt(key_1, int(block,2))
        message_decrypter.append(bin(message_decrypte))
    return message_decrypter


def encrypt_string(string, key_1, key_2):
    """Fonction qui permet de crypter un string avec deux clés

    Args:
        string (str): le string à crypter
        key_1 (int): La première clé
        key_2 (int): La deuxième clé

    Returns:
        list: le string crypté
    """
    message_crypter = []
    for block in to_binary(string):
        message_crypte = sdes.encrypt(key_2, sdes.encrypt(key_1, int(block,2)))
        message_crypter.append(bin(message_crypte))
    return message_crypter


def decrypt_string(string_crypte, key_1, key_2):
    """Fonction qui permet de décrypter un string avec deux clés

    Args:
        string_crypte (str): le string à décrypter
        key_1 (int): La première clé
        key_2 (int): La deuxième clé

    Returns:
        list: le string décrypté
    """
    message_decrypter = []
    for block in string_crypte:
        message_decrypte = sdes.decrypt(key_1, sdes.decrypt(key_2, int(block,2)))
        message_decrypter.append(bin(message_decrypte))
    return message_decrypter


#print(encryptage("arsene_lupin_extrait.txt",10,10))

if __name__ == '__main__':
    message_crypter = encrypt_string("Ceci est un t'èeste", 4, 1)
    print(message_crypter)
    message_decrypter = decrypt_string(message_crypter,4,1)

    print(to_string(message_decrypter))
    