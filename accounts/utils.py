from cryptography.fernet import Fernet
from django.conf import settings
from .models import Code


def decrypt_message(encrypted_message):
    key = settings.CRYPTO_KEY
    cipher = Fernet(key)
    decrypted_message = cipher.decrypt(encrypted_message.encode()).decode()
    split_pattern = decrypted_message.split('-')
    if len(split_pattern) == 6:
        id_physical_location = split_pattern[0]
        consecutive = split_pattern[1]
        try:
            code = Code.objects.get(id_physical_location=id_physical_location, consecutive=consecutive)
            raise Exception()
        except Code.DoesNotExist:
            code = Code()
            code.id_physical_location = id_physical_location
            code.consecutive = consecutive
            code.id_container = split_pattern[2]
            code.id_model = split_pattern[3]
            code.material = split_pattern[4]
            code.success = split_pattern[5]
            return code
    else:
        raise Exception()
