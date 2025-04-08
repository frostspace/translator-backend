from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq

# Load env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

# response schema
class TranslationRequest(BaseModel):
    text: str

# endpoint for translation
@app.post("/translate")
async def translate_text(request: TranslationRequest):
    try:
        completion = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=[
                {"role": "system", "content": "You are a professional translator. Your task is to translate English text to Hindi. Provide only the Hindi translation without any additional explanations or notes."},
                {"role": "user", "content": f"Translate the following English text to Hindi: {request.text}"}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        translation = completion.choices[0].message.content if completion.choices else None
        if translation:
            return {"translation": translation}
        else:
            raise HTTPException(status_code=500, detail="Translation failed, please try again")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during translation: {e}")
