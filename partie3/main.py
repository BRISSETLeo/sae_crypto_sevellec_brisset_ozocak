from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from PIL import Image


def open_image(path):
    """ fonction qui permet d'ouvrir une image

    Args:
        path (str): le chemin de l'image

    Returns:
        Image: l'image ouverte 
    """
    try:
        image = Image.open(path)
        return image
    except Exception as e:
        print(f"An error occurred while opening the image: {e}")
        return None


def to_binary(image):
    """ fonction qui permet de convertir une image en binaire

    Args:
        image (Image): l'image à convertir 

    Returns:
        Bytes: l'image convertie en binaire 
    """
    try:
        img = Image.eval(image, lambda x: 255 - x)
        data = list(img.getdata())
        data_binary = ''.join(format(255 - pixel, '08b') for pixel in data)
        return data_binary
    except Exception as e:
        print(f"An error occurred while converting to binary: {e}")
        return None


def block_of_8(lst):
    """ fonction qui permet de séparer une liste en bloc de 8

    Args:
        lst (list): la liste à séparer 

    Returns:
        list: la liste séparée en bloc de 8 
    """
    return [lst[i] for i in range(7, len(lst), 8)]


def last_bit(image):
    """ fonction qui permet de récupérer le dernier bit de chaque block de 8

    Args:
        image (Image): l'image à traiter 

    Returns:
        bytes: les 512 derniers bits de chaque block de 8 de l'image 
    """
    data_binary = to_binary(image)
    data_bits = block_of_8(data_binary[:512])  # 8 * 64 = 512
    return data_bits
