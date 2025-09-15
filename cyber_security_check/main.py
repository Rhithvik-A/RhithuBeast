from fastapi import FastAPI, File, UploadFile, Form
from cryptography.fernet import Fernet
import shutil, os
import easyocr
import re
from pathlib import Path

from fastapi.responses import FileResponse

app = FastAPI()
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / "files/plain"
DATA_FOLDER = BASE_DIR / "files/data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

@app.post("/upload/")
def upload_file(
    name: str = Form("Rhithvik"),
    grade: int = Form("10"),
    email: str = Form("rhithvik@gmail.com"),
    adm_num: int = Form("16206344"),
    file: UploadFile = File(...)

    ):
    file_path = UPLOAD_FOLDER / file.filename  # Path object
    data_path = DATA_FOLDER / file.filename    # Path object (if you need it)

    # 1️⃣ Save the uploaded file FIRST
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2️⃣ Now run OCR on the saved file
    reader = easyocr.Reader(['en'])
    results = reader.readtext(str(file_path), detail=0)  # ✅ convert to str

    # 3️⃣ Extract Emirates ID
    text = ' '.join(results)
    emirates_ids = re.findall(r'784[\-\s]?\d{4}[\-\s]?\d{7}[\-\s]?\d', text)
    eid = emirates_ids[0] if emirates_ids else "Not Found"
    print(eid)

    # 4️⃣ Save details
    details_file = UPLOAD_FOLDER / "details.txt"
    with open(details_file, "w") as f:
        f.write(
            f"Name: {name}, Grade: {grade}, Email: {email}, "
            f"File: {file.filename}, Admition Number: {adm_num}, EmiratesID: {eid}\n"
        )

    return {"message": "Student details have been saved successfully!"}

#now the encrypted version

with open("secret.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

UPLOAD_ENCRYPTED_FOLDER = BASE_DIR / "files/encrypted"
os.makedirs(UPLOAD_ENCRYPTED_FOLDER, exist_ok=True)

from fastapi.responses import StreamingResponse
import io, zipfile, shutil, re
from pathlib import Path

@app.post("/encrypt_and_upload/")
def upload_and_encrypt(
    name: str = Form("Rhithvik"),
    grade: int = Form("10"),
    email: str = Form("rhithvik@gmail.com"),
    adm_num: int = Form("16206344"),
    file: UploadFile = File(...)
):
    # ----------------- Paths -----------------
    original_path = DATA_FOLDER / file.filename
    enc_filename = f"{adm_num}_{file.filename}"
    enc_file_path = UPLOAD_ENCRYPTED_FOLDER / enc_filename
    details_file = UPLOAD_ENCRYPTED_FOLDER / "encrypted_details.txt"

    # ----------------- Save original -----------------
    with open(original_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ----------------- Encrypt content -----------------
    with open(original_path, "rb") as src:
        file_bytes = src.read()
    encrypted = fernet.encrypt(file_bytes)
    with open(enc_file_path, "wb") as f:
        f.write(encrypted)

    # ----------------- Encrypt Email -----------------
    encrypted_email = fernet.encrypt(email.encode()).decode()

    # ----------------- OCR Emirates ID -----------------
    reader = easyocr.Reader(['en'])
    results = reader.readtext(str(original_path), detail=0)
    text = ' '.join(results)
    emirates_ids = re.findall(r'784[\-\s]?\d{4}[\-\s]?\d{7}[\-\s]?\d', text)
    eid = emirates_ids[0] if emirates_ids else "Not Found"
    encrypted_eid = fernet.encrypt(eid.encode()).decode()

    # ----------------- Write details -----------------
    with open(details_file, "w") as f:
        f.write(
            f"Name: {name}, Grade: {grade}, Email: {encrypted_email}, "
            f"File: {file.filename}, Admission Number: {adm_num}, EmiratesID: {encrypted_eid}\n"
        )

    # ----------------- Create in-memory ZIP -----------------
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(enc_file_path, arcname=enc_filename)          # encrypted file
        zipf.write(details_file, arcname="encrypted_details.txt") # details file
    zip_buffer.seek(0)

    # ----------------- Return ZIP -----------------
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={adm_num}_encrypted_package.zip"
        }
    )

@app.get("/")
def my_root():
    return "Welcome to my API!"


@app.post("/decrypt/")
def decrypt_file(
    encrypted_id_file: UploadFile = File(...),
    encrypted_details_file: UploadFile = File(...)
):
    # -------- Paths --------
    id_file_path = os.path.join(UPLOAD_ENCRYPTED_FOLDER, encrypted_id_file.filename)
    details_file_path = os.path.join(UPLOAD_ENCRYPTED_FOLDER, encrypted_details_file.filename)

    if not os.path.exists(id_file_path):
        return {"error": "ID File not found"}
    if not os.path.exists(details_file_path):
        return {"error": "Details File not found"}

    # -------- Decrypt ID File --------
    with open(id_file_path, "rb") as f:
        encrypted_id_file_data = f.read()
    decrypted_id_file_data = fernet.decrypt(encrypted_id_file_data)

    dec_id_filename = "decrypted_" + encrypted_id_file.filename.replace("encrypted_", "")
    dec_id_file_path = os.path.join(UPLOAD_ENCRYPTED_FOLDER, dec_id_filename)
    with open(dec_id_file_path, "wb") as f:
        f.write(decrypted_id_file_data)

    # -------- Decrypt Details --------
    with open(details_file_path, "r") as f:
        content = f.read().strip()

    parts = [p.strip() for p in content.split(",")]
    email_part = [p for p in parts if p.startswith("Email:")][0]
    encrypted_email = email_part.replace("Email:", "").strip()

    eid_part = [p for p in parts if p.startswith("EmiratesID:")][0]
    encrypted_eid = eid_part.replace("EmiratesID:", "").strip()

    decrypted_email = fernet.decrypt(encrypted_email.encode()).decode()
    decrypted_eid = fernet.decrypt(encrypted_eid.encode()).decode()

    new_parts = []
    for p in parts:
        if p.startswith("Email:"):
            new_parts.append(f"Email: {decrypted_email}")
        elif p.startswith("EmiratesID:"):
            new_parts.append(f"EmiratesID: {decrypted_eid}")
        else:
            new_parts.append(p)

    decrypted_content = ", ".join(new_parts)
    dec_details_filename = "decrypted_details.txt"
    dec_details_path = os.path.join(UPLOAD_ENCRYPTED_FOLDER, dec_details_filename)
    with open(dec_details_path, "w") as f:
        f.write(decrypted_content)

    # -------- Create in-memory ZIP --------
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(dec_id_file_path, arcname=dec_id_filename)
        zipf.write(dec_details_path, arcname=dec_details_filename)
    zip_buffer.seek(0)

    # -------- Return ZIP --------
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="decrypted_package.zip"'
        }
    )
