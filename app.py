# app.py
from pydantic import BaseModel
from transformers import pipeline
import httpx
import io
import streamlit as st
from PIL import Image



class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    translation: str

translator = pipeline("translation_ru_to_en", model="Helsinki-NLP/opus-mt-ru-en")

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    try:
        translation_result = translator(request.text, max_length=50)[0]['translation_text']
        return TranslationResponse(translation=translation_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during translation: {str(e)}")


import streamlit as st

st.title("Translation App")

text_to_translate = st.text_area("Enter text for translation:", "Привет, как дела?")

if st.button("Translate"):
    translation_request = TranslationRequest(text=text_to_translate)
    try:
        with httpx.Client() as client:
            response = client.post("http://127.0.0.1:8000/translate", json=translation_request.dict())
        translation_result = response.json()["translation"]
        st.success(f"Translation: {translation_result}")
    except Exception as e:
        st.error(f"Error during translation: {str(e)}")

# Для запуска АПИ и ВЕБ интерфейса нужно:
# В командной строке запустить апи "uvicorn task3:app --reload --port 8000" - команда разворачивает на адрессе http://127.0.0.1:8000/ АПИ
# В другой командной строке запустить веб "streamlit run task3.py" - команда запускает веб интерфейс
