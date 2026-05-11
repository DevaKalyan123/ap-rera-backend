# app/utils/file_upload.py

import os
from werkzeug.utils import secure_filename

BASE_UPLOAD_DIR = "uploads"

def save_file(file, sub_folder):
    upload_dir = os.path.join(BASE_UPLOAD_DIR, sub_folder)
    os.makedirs(upload_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_dir, filename)

    file.save(file_path)
    return file_path