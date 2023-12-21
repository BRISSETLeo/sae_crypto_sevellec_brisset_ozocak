import main
import time

def brute_force_attack(plaintext_message, encrypted_message):
    """Fonction qui permet de casser un message chiffré avec une attaque brute force

    Args:
        plaintext_message (str): Le message en clair
        encrypted_message (str): Le message chiffré

    Returns:
        tuple: Les clés utilisées pour chiffrer le message
    """
    for key_1 in range(1024):
        for key_2 in range(1024):
            encrypted = main.encrypt_string(plaintext_message, key_1, key_2)
            if encrypted == encrypted_message:
                return key_1, key_2
    return None, None

def clever_attack(plaintext_message, encrypted_message):
    """Fonction qui permet de casser un message chiffré avec une attaque astucieuse

    Args:
        plaintext_message (str): Le message en clair
        encrypted_message (str): Le message chiffré

    Returns:
        tuple: Les clés utilisées pour chiffrer le message
    """
    keys = range(2 ** 10)
    results = {}
    for key_1 in keys:
        encrypted = main.encrypt_string_2(plaintext_message[:20], key_1)
        results[key_1] = encrypted
    for key_2 in keys:
        encrypted = main.decrypt_string_2(encrypted_message[:20], key_2)
        if encrypted in results.values():
            for key_1, encrypter in results.items():
                if encrypted == encrypter:
                    return key_1, key_2
    return None, None

def brute_force_attack_evaluation(plaintext_message, encrypted_message):
    """Fonction qui permet de compter le nombre de tentative pour casser un message chiffré avec une attaque brute force

    Args:
        plaintext_message (str): Le message en clair
        encrypted_message (str): Le message chiffré

    Returns:
        tuple: Les clés utilisées pour chiffrer le message et le nombre de tentatives
    """
    attempts = 0
    for key_1 in range(1024):
        for key_2 in range(1024):
            attempts += 1
            encrypted = main.encrypt_string(plaintext_message, key_1, key_2)
            if encrypted == encrypted_message:
                return key_1, key_2, attempts
    return None, None, attempts

def clever_attack_evaluation(plaintext_message, encrypted_message):
    """Fonction qui permet de compter le nombre de tentative pour casser un message chiffré avec une attaque astucieuse

    Args:
        plaintext_message (str): Le message en clair
        encrypted_message (str): Le message chiffré

    Returns:
        tuple: Les clés utilisées pour chiffrer le message et le nombre de tentatives
    """
    keys = range(2 ** 10)
    results = {}
    attempts = 0
    for key_1 in keys:
        encrypted = main.encrypt_string_2(plaintext_message[:20], key_1)
        results[key_1] = encrypted
    for key_2 in keys:
        attempts += 1
        encrypted = main.decrypt_string_2(encrypted_message[:20], key_2)
        if encrypted in results.values():
            for key_1, encrypter in results.items():
                if encrypted == encrypter:
                    return key_1, key_2, attempts
    return None, None, attempts

def evaluate_attack(plaintext_message, encrypted_message, attack_method, number_of_iterations=5):
    """Fonction qui permet d'évaluer le temps et les essaie d'une attaque

    Args:
        plaintext_message (str): Le message en clair
        encrypted_message (str): Le message chiffré
        attack_method (str): La méthode d'attaque utilisée
        number_of_iterations (int, optional): Le nombre d'iteration. Defaults to 5.

    Returns:
        _type_: _description_
    """
    total_attempts = 0
    total_execution_time = 0

    for _ in range(number_of_iterations):
        start = time.time()
        key1, key2, attempts = attack_method(plaintext_message, encrypted_message)
        execution_time = time.time() - start

        total_attempts += attempts
        total_execution_time += execution_time

    average_attempts = total_attempts / number_of_iterations
    average_execution_time = total_execution_time / number_of_iterations

    return average_attempts, average_execution_time

if __name__ == "__main__":
    plaintext_message = main.file_to_string("./docs/arsene_lupin_extrait.txt")
    encrypted_message = main.encrypt_string(plaintext_message, 3, 2)

    time_start = time.time()
    print(brute_force_attack(plaintext_message, encrypted_message))
    print("Temps pour cassage brute:", time.time() - time_start)

    time_start = time.time()
    key1, key2 = clever_attack(plaintext_message, encrypted_message)
    print("Temps pour cassage astucieux:", time.time() - time_start)
    print(main.toString(main.decrypt_string(encrypted_message, key1, key2)))

    plaintext_message = main.file_to_string("./docs/lettres_persanes.txt")
    encrypted_message = main.encrypt_string(plaintext_message, 1000, 997)

    clever_attempts, clever_execution_time = evaluate_attack(plaintext_message, encrypted_message, clever_attack_evaluation)
    print(f"Cassage astucieux - Nombre moyen de tentatives: {clever_attempts}, Temps d'exécution moyen: {clever_execution_time:.6f} seconds")

    brute_attempts, brute_execution_time = evaluate_attack(plaintext_message, encrypted_message, brute_force_attack_evaluation)
    print(f"Cassage brute - Nombre moyen de tentatives: {brute_attempts}, Temps d'exécution moyen: {brute_execution_time:.6f} seconds")
