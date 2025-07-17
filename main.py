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

# --- PARTE 2: Endpoint para el diagrama de cambio de fase ---
from fastapi import Query

P_CRIT = 10.0  # MPa
VC = 0.0035     # m3/kg (punto crítico)
P_MIN = 0.05    # MPa (presión mínima del diagrama)
V_LIQ_MIN = 0.00105  # m3/kg (aprox. del diagrama)
V_VAP_MIN = 30.0     # m3/kg (aprox. del diagrama)

def interpolate(x, x0, y0, x1, y1):
    """Interpolación lineal simple"""
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

@app.get("/phase-change-diagram")
def phase_change_diagram(pressure: float = Query(..., gt=0)):
    if pressure >= P_CRIT:
        return {
            "specific_volume_liquid": VC,
            "specific_volume_vapor": VC
        }
    elif pressure <= P_MIN:
        return {
            "specific_volume_liquid": V_LIQ_MIN,
            "specific_volume_vapor": V_VAP_MIN
        }
    else:
        v_liq = interpolate(pressure, P_MIN, V_LIQ_MIN, P_CRIT, VC)
        v_vap = interpolate(pressure, P_MIN, V_VAP_MIN, P_CRIT, VC)
        return {
            "specific_volume_liquid": round(v_liq, 5),
            "specific_volume_vapor": round(v_vap, 5)
        }