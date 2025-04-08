from fastapi import APIRouter
from .endpoints import translate_text

app_router = APIRouter()

# Route for /translate
app_router.post("/translate")(translate_text)