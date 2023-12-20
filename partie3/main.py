from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from PIL import Image


def open_image(path):
    try:
        image = Image.open(path)
        return image
    except Exception as e:
        print(f"An error occurred while opening the image: {e}")
        return None


def to_binary(image):
    try:
        img = Image.eval(image, lambda x: 255 - x)
        data = list(img.getdata())
        data_binary = ''.join(format(255 - pixel, '08b') for pixel in data)
        return data_binary
    except Exception as e:
        print(f"An error occurred while converting to binary: {e}")
        return None


def block_of_8(lst):
    return [lst[i] for i in range(7, len(lst), 8)]


def last_bit(image):
    data_binary = to_binary(image)
    data_bits = block_of_8(data_binary[:512])  # 8 * 64 = 512
    return data_bits
