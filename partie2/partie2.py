from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time
import main
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


def encrypt_message(key, plain_messages):
    encrypted_messages = []

    for plain_message in plain_messages:
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        padded_message = pad(plain_message.encode('utf-8'), AES.block_size)
        encrypted_message = cipher.encrypt(padded_message)

        encrypted_messages.append((iv, encrypted_message))

    return encrypted_messages


def decrypt_message(key, encrypted_messages):
    decrypted_messages = []

    for iv, encrypted_message in encrypted_messages:
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        padded_message = cipher.decrypt(encrypted_message)
        message = unpad(padded_message, AES.block_size)

        decrypted_messages.append(message)

    return decrypted_messages


if __name__ == "__main__":

    rossignol2 = open_image("./docs/rossignol2.bmp")

    original_key = ""

    if rossignol2:
        original_key = last_bit(rossignol2)
        original_key = "".join(original_key)
        print(original_key)

    for i in range(2):
        original_key += original_key

    sdes_key = 1023
    aes_key = get_random_bytes(32)

    plain_messages_sdes = main.file_to_string("./docs/arsene_lupin_extrait.txt")
    plain_messages_aes = "# Texte extrait du livre Arsène Lupin, gentleman-cambrioleur de Maurice Leblanc # Source: le projet Gutenberg https://www.gutenberg.org/ebooks/32854 Arsène Lupin parmi nous! l'insaisissable cambrioleur dont on racontait les prouesses dans tous les journaux depuis des mois! l'énigmatique personnage avec qui le vieux Ganimard, notre meilleur policier, avait engagé ce duel à mort dont les péripéties se déroulaient de façon si pittoresque! Arsène Lupin, le fantaisiste gentleman qui n'opère que dans les châteaux et les salons, et qui, une nuit, où il avait pénétré chez le baron Schormann, en était parti les mains vides et avait laissé sa carte, ornée de cette formule: «Arsène Lupin, gentleman-cambrioleur, reviendra quand les meubles seront authentiques». Arsène Lupin, l'homme aux mille déguisements: tour à tour chauffeur, ténor, bookmaker, fils de famille, adolescent, vieillard, commis-voyageur marseillais, médecin russe, torero espagnol!"

    start_sdes = time.time()
    encrypted_text_sdes = main.encrypt_string_2(plain_messages_sdes, sdes_key)
    encryption_time_sdes = time.time() - start_sdes

    start_decrypt_sdes = time.time()
    decrypted_text_sdes = main.decrypt_string_2(encrypted_text_sdes, sdes_key)
    decryption_time_sdes = time.time() - start_decrypt_sdes

    start_aes = time.time()
    encrypted_messages_aes = encrypt_message(aes_key, plain_messages_aes)
    encryption_time_aes = time.time() - start_aes

    start_decrypt_aes = time.time()
    decrypted_text_aes = decrypt_message(aes_key, encrypted_messages_aes)
    decryption_time_aes = time.time() - start_decrypt_aes

    print(
        f"Temps cryptage SDES: {encryption_time_sdes / len(plain_messages_sdes):.8f} seconds"
    )
    print(
        f"Temps décryptage SDES: {decryption_time_sdes / len(plain_messages_sdes):.8f} seconds"
    )

    print(
        f"Temps cryptage AES: {encryption_time_aes / len(plain_messages_aes):.8f} seconds"
    )
    print(
        f"Temps décryptage AES: {decryption_time_aes / len(plain_messages_aes):.8f} seconds"
    )

    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit. Ut velit mauris, egestas sed, gravida nec, ornare ut, mi. Aenean ut orci vel massa suscipit pulvinar. Nulla sollicitudin. Fusce varius, ligula non tempus aliquam, nunc turpis ullamcorper nibh, in tempus sapien eros vitae ligula. Pellentesque rhoncus nunc et augue. Integer id felis. Curabitur aliquet pellentesque diam. Integer quis metus vitae elit lobortis egestas. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Morbi vel erat non mauris convallis vehicula. Nulla et sapien. Integer tortor tellus, aliquam faucibus, convallis id, congue eu, quam. Mauris ullamcorper felis vitae erat. Proin feugiat, augue non elementum posuere, metus purus iaculis lectus, et tristique ligula justo vitae magna. Aliquam convallis sollicitudin purus. Praesent aliquam, enim at fermentum mollis, ligula massa adipiscing nisl, ac euismod nibh nisl eu lectus. Fusce vulputate sem at sapien. Vivamus leo. Aliquam euismod libero eu enim. Nulla nec felis sed leo placerat imperdiet. Aenean suscipit nulla in justo. Suspendisse cursus rutrum augue. Nulla tincidunt tincidunt mi. Curabitur iaculis, lorem vel rhoncus faucibus, felis magna fermentum augue, et ultricies lacus lorem varius purus. Curabitur eu amet."

    key = int(original_key, 2).to_bytes(len(original_key) // 8,
                                        byteorder='big')

    encrypted_text = encrypt_message(key, text)

    decrypted_text = decrypt_message(key, encrypted_text)

    final_text = ""
    for letter in decrypted_text:
        final_text += letter.decode('utf-8')

    print(text)
