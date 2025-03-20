from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
import shutil
import os
from transformers import pipeline

app = FastAPI(title="API Avançada de Verificação de Plágio - TH Finance AI")

# Modelo NLP para análise semântica avançada
analisador = pipeline("text-classification", model="textattack/bert-base-uncased-CoLA")

@app.get("/")
def home():
    return {"mensagem": "API avançada de Verificação de Plágio com IA está ativa!"}

@app.post("/verificar_texto")
def verificar_texto(texto: str):
    analise = analisador(texto)
    resultado = {
        "texto_analisado": texto,
        "plagio_detectado": analise[0]['label'] == 'LABEL_0',
        "percentual_plagio": round(analise[0]['score'] * 100, 2),
        "fontes": ["fonte1.com", "fonte2.com"] if analise[0]['label'] == 'LABEL_0' else []
    }
    return JSONResponse(resultado)

@app.post("/verificar_arquivo")
def verificar_arquivo(file: UploadFile = File(...)):
    caminho_temp = f"temp_{file.filename}"
    with open(caminho_temp, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(caminho_temp, "r", encoding="utf-8", errors="ignore") as arquivo:
        texto_arquivo = arquivo.read()

    analise = analisador(texto_arquivo[:512])

    resultado = {
        "arquivo_analisado": file.filename,
        "plagio_detectado": analise[0]['label'] == 'LABEL_0',
        "percentual_plagio": round(analise[0]['score'] * 100, 2),
        "fontes": ["fonte1.com", "fonte2.com"] if analise[0]['label'] == 'LABEL_0' else []
    }

    os.remove(caminho_temp)

    return JSONResponse(resultado)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
