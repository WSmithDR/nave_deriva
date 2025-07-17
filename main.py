from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse, HTMLResponse

import random

app = FastAPI()

SYSTEMS = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

# Guardar el sistema averiado en memoria (simple para demo)
damaged_system = random.choice(list(SYSTEMS.keys()))

@app.get("/status")
def get_status():
    # Devuelve el sistema averiado
    return {"damaged_system": damaged_system}

@app.get("/repair-bay")
def repair_bay():
    # Devuelve el código único en HTML
    code = SYSTEMS[damaged_system]
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
    <div class="anchor-point">{code}</div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/teapot")
def teapot():
    # Retorna HTTP 418
    return Response(status_code=418)