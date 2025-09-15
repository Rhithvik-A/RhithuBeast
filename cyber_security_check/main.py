from fastapi import FastAPI, File, UploadFile, Form
from cryptography.fernet import Fernet
import shutil, os
import easyocr
import re

app = FastAPI()
UPLOAD_FOLDER = r"C:\Users\Ashok\Desktop\student_details\plain"
DATA_FOLDER = r"C:\Users\Ashok\Desktop\student_details\data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
def upload_file(
    name: str = Form("Rhithvik"),
    grade: int = Form("10"),
    email: str = Form("rhithvik@gmail.com"),
    adm_num: int = Form("16206344"),
    file: UploadFile = File(...)

    ):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    reader = easyocr.Reader(['en'])  # loads English model
    
    results = reader.readtext(DATA_FOLDER + "\\" + file.filename, detail=0)  # returns list of text strings

    text = ' '.join(results)
    emirates_ids = re.findall(r'784[\-\s]?\d{4}[\-\s]?\d{7}[\-\s]?\d', text)
    print(emirates_ids[0])


    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    details_file = os.path.join(UPLOAD_FOLDER, "details.txt")
    with open(details_file, "w") as f:  # write mode overwrites the file
        f.write(f"Name: {name}, Grade: {grade}, Email: {email}, File: {file.filename}, Admition Number: {adm_num}, EmiratesID: {emirates_ids[0]}\n")

    return {"message": f"Student details have been saved successfully!"}

#now the encrypted version

with open("secret.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

UPLOAD_ENCRYPTED_FOLDER = r"C:\Users\Ashok\Desktop\student_details\encrypted"
os.makedirs(UPLOAD_ENCRYPTED_FOLDER, exist_ok=True)

@app.post("/encrypt_and_upload/")
def upload_and_encrypt(
    name: str = Form("Rhithvik"),
    grade: int = Form("10"),
    email: str = Form("rhithvik@gmail.com"),
    adm_num: int = Form("16206344"),
    file: UploadFile = File(...)
    ):
    # read file content
    file_bytes = file.file.read()

    # encrypt content
    encrypted = fernet.encrypt(file_bytes)

    # save encrypted file
    enc_file_path = os.path.join(UPLOAD_ENCRYPTED_FOLDER, f"{adm_num}_{file.filename}")
    with open(enc_file_path, "wb") as f:
        f.write(encrypted)


    encrypted_email = fernet.encrypt(email.encode()).decode()

    # Read EID
    reader = easyocr.Reader(['en'])  # loads English model
    results = reader.readtext(DATA_FOLDER + "\\" + file.filename, detail=0)  # returns list of text strings
    text = ' '.join(results)
    emirates_ids = re.findall(r'784[\-\s]?\d{4}[\-\s]?\d{7}[\-\s]?\d', text)
    print(emirates_ids[0])
    encrypted_eid = fernet.encrypt(emirates_ids[0].encode()).decode()


    details_file = os.path.join(UPLOAD_ENCRYPTED_FOLDER, "encrypted_details.txt")
    with open(details_file, "w") as f:  # write mode overwrites the file
        f.write(f"Name: {name}, Grade: {grade}, Email: {encrypted_email}, File: {file.filename}, Admition Number: {adm_num}, EmiratesID: {encrypted_eid}\n")

    return {"message": f"Student details have been encrypted & saved successfully!"}

@app.get("/")
def my_root():
    return "Welcome to my API!"


@app.post("/decrypt/")
def decrypt_file(encrypted_id_file: UploadFile = File(...), 
                 encrypted_details_file: UploadFile = File(...)):
    details_file_path = os.path.join(UPLOAD_ENCRYPTED_FOLDER, encrypted_details_file.filename)
    id_file_path = os.path.join(UPLOAD_ENCRYPTED_FOLDER, encrypted_id_file.filename)

    print(details_file_path)
    print(id_file_path)
     

    if not os.path.exists(id_file_path):
        return {"error": "ID File not found"}

    with open(id_file_path, "rb") as f:
        encrypted_id_file_data = f.read()

    # decrypt data
    decrypted_id_file_data = fernet.decrypt(encrypted_id_file_data)

    # save decrypted file temporarily
    dec_id_file_path = os.path.join(UPLOAD_ENCRYPTED_FOLDER, "decrypted_" + encrypted_id_file.filename.replace("encrypted_",""))
    with open(dec_id_file_path, "wb") as f:
        f.write(decrypted_id_file_data)

    # Reading Details File
    details_file_path = os.path.join(UPLOAD_ENCRYPTED_FOLDER, encrypted_details_file.filename)
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

    output_path = os.path.join(UPLOAD_ENCRYPTED_FOLDER, "decrypted_details.txt")
    with open(output_path, "w") as f:
        f.write(decrypted_content)

    return {"message": f"Data and file have been decrypted & saved successfully!"}
