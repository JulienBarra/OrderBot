"""OrderBot : API HTTP + interface web."""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from extract import CATALOGUE, extraire

app = FastAPI(title="OrderBot")
STATIC = Path(__file__).parent / "static"


class MailIn(BaseModel):
    texte: str = Field(min_length=1, max_length=10_000)  # borne la taille : un mail, pas un roman


@app.post("/extract")
def extract(mail: MailIn):
    # 'def' et non 'async def' : le client openai est synchrone,
    # FastAPI exécute donc cette fonction dans un thread séparé sans bloquer le serveur.
    try:
        return extraire(mail.texte)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur du moteur LLM : {e}")


@app.get("/catalogue")
def catalogue():
    return [{"sku": s, "designation": r["designation"], "prix_ht": float(r["prix_ht"])}
            for s, r in CATALOGUE.items()]


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")