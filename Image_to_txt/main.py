from fastapi import FastAPI
import easyocr
import re

app = FastAPI()   # ✅ Correct way

@app.get("/get-title")
def get_title(): 
    reader = easyocr.Reader(['en'])  # loads English model
    results = reader.readtext(
        r"C:\Users\vidhyadevig\Desktop\Rhithvik\Screenshot 2025-09-16 192449.png",
        detail=0
    )  # returns list of text strings
    text = ' '.join(results)
    print(text)
    return {"extracted_text": text}  # ✅ Return JSON instead of just printing
