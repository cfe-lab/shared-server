import os
import secrets

from django.conf import settings

settings.DATASUBMISSION_PATH


def gen_filename():
    return secrets.token_hex(16)
    

def save_file(uploaded_file, filename):
    new_path = os.path.join(
        settings.DATASUBMISSION_PATH,
        filename,
    )
    with open(new_path, 'wb') as outfile:
        for chunk in uploaded_file.chunks():
            outfile.write(chunk)

            

    
    
