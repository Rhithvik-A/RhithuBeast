from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from cryptography.fernet import Fernet
import shutil
import os
import easyocr
import re
from pathlib import Path
from fastapi.responses import StreamingResponse
import io
import zipfile

app = FastAPI()

# ----------------- Enable CORS -----------------
origins = [
    "*",  # allow all origins, you can restrict to your frontend URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)

# ----------------- Folders -----------------
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / "files/plain"
DATA_FOLDER = BASE_DIR / "files/data"
UPLOAD_ENCRYPTED_FOLDER = BASE_DIR / "files/encrypted"

for folder in [UPLOAD_FOLDER, DATA_FOLDER, UPLOAD_ENCRYPTED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# ----------------- Load encryption key -----------------
with open("secret.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

# ----------------- EasyOCR Reader -----------------
ocr_reader = easyocr.Reader(['en'], gpu=False)  # Use GPU if available

# ----------------- Upload Plain File -----------------
@app.post("/upload/")
def upload_file(
    name: str = Form("Rhithvik"),
    grade: int = Form(10),
    email: str = Form("rhithvik@gmail.com"),
    adm_num: int = Form(16206344),
    file: UploadFile = File(...)
):
    file_path = UPLOAD_FOLDER / Path(file.filename).name
    data_path = DATA_FOLDER / Path(file.filename).name

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    with open(data_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR to extract Emirates ID
    results = ocr_reader.readtext(str(file_path), detail=0)
    text = ' '.join(results)
    emirates_ids = re.findall(r'784[\-\s]?\d{4}[\-\s]?\d{7}[\-\s]?\d', text)
    eid = emirates_ids[0] if emirates_ids else "Not Found"

    # Save details
    details_file = UPLOAD_FOLDER / "details.txt"
    with open(details_file, "w") as f:
        f.write(
            f"Name: {name}, Grade: {grade}, Email: {email}, "
            f"File: {file.filename}, Admission Number: {adm_num}, EmiratesID: {eid}\n"
        )

    return {"message": "Student details have been saved successfully!"}


# ----------------- Encrypt and Upload -----------------
@app.post("/encrypt_and_upload/")
def upload_and_encrypt(
    name: str = Form("Rhithvik"),
    grade: int = Form(10),
    email: str = Form("rhithvik@gmail.com"),
    adm_num: int = Form(16206344),
    file: UploadFile = File(...)
):
    original_path = DATA_FOLDER / Path(file.filename).name
    enc_filename = f"{adm_num}_{Path(file.filename).name}"
    enc_file_path = UPLOAD_ENCRYPTED_FOLDER / enc_filename
    details_file = UPLOAD_ENCRYPTED_FOLDER / "encrypted_details.txt"

    # Save original file
    with open(original_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Encrypt file
    with open(original_path, "rb") as src:
        encrypted = fernet.encrypt(src.read())
    with open(enc_file_path, "wb") as f:
        f.write(encrypted)

    # Encrypt email
    encrypted_email = fernet.encrypt(email.encode()).decode()

    # OCR for Emirates ID
    results = ocr_reader.readtext(str(original_path), detail=0)
    text = ' '.join(results)
    emirates_ids = re.findall(r'784[\-\s]?\d{4}[\-\s]?\d{7}[\-\s]?\d', text)
    eid = emirates_ids[0] if emirates_ids else "Not Found"
    encrypted_eid = fernet.encrypt(eid.encode()).decode()

    # Write encrypted details
    with open(details_file, "w") as f:
        f.write(
            f"Name: {name}, Grade: {grade}, Email: {encrypted_email}, "
            f"File: {file.filename}, Admission Number: {adm_num}, EmiratesID: {encrypted_eid}\n"
        )

    # Create ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(enc_file_path, arcname=enc_filename)
        zipf.write(details_file, arcname="encrypted_details.txt")
    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={adm_num}_encrypted_package.zip"}
    )


# ----------------- Decrypt -----------------
@app.post("/decrypt/")
def decrypt_file(
    encrypted_id_file: UploadFile = File(...),
    encrypted_details_file: UploadFile = File(...),
):
    id_file_path = UPLOAD_ENCRYPTED_FOLDER / Path(encrypted_id_file.filename).name
    details_file_path = UPLOAD_ENCRYPTED_FOLDER / Path(encrypted_details_file.filename).name

    with open(id_file_path, "wb") as f:
        shutil.copyfileobj(encrypted_id_file.file, f)
    with open(details_file_path, "wb") as f:
        shutil.copyfileobj(encrypted_details_file.file, f)

    # Decrypt ID file
    with open(id_file_path, "rb") as f:
        decrypted_id_file_data = fernet.decrypt(f.read())
    dec_id_filename = "decrypted_" + Path(encrypted_id_file.filename).name.replace("encrypted_", "")
    dec_id_file_path = UPLOAD_ENCRYPTED_FOLDER / dec_id_filename
    with open(dec_id_file_path, "wb") as f:
        f.write(decrypted_id_file_data)

    # Decrypt details file
    with open(details_file_path, "r") as f:
        content = f.read().strip()
    parts = [p.strip() for p in content.split(",")]
    email_part = [p for p in parts if p.startswith("Email:")][0]
    eid_part = [p for p in parts if p.startswith("EmiratesID:")][0]

    decrypted_email = fernet.decrypt(email_part.replace("Email:", "").strip().encode()).decode()
    decrypted_eid = fernet.decrypt(eid_part.replace("EmiratesID:", "").strip().encode()).decode()

    new_parts = [
        f"Email: {decrypted_email}" if p.startswith("Email:") else
        f"EmiratesID: {decrypted_eid}" if p.startswith("EmiratesID:") else p
        for p in parts
    ]
    decrypted_content = ", ".join(new_parts)

    dec_details_filename = "decrypted_details.txt"
    dec_details_path = UPLOAD_ENCRYPTED_FOLDER / dec_details_filename
    with open(dec_details_path, "w") as f:
        f.write(decrypted_content)

    # Create ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(dec_id_file_path, arcname=dec_id_filename)
        zipf.write(dec_details_path, arcname=dec_details_filename)
    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="decrypted_package.zip"'}
    )


# ----------------- Root -----------------
@app.get("/")
def root():
    return {"message": "Welcome to the Student Encryption API!"}
