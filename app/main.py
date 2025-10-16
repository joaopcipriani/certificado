from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess, os, tempfile, shutil, zipfile, datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="/app/static"), name="static")
templates = Jinja2Templates(directory="/app/templates")

OUTPUT_DIR = "/data/certs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_csr(
    request: Request,
    C: str = Form(...),
    O: str = Form(...),
    CN: str = Form(...),
    ST: str = Form(...),
    L: str = Form(...),
    serialNumber: str = Form(...),
    prefix: str = Form("server")
):
    """Gera KEY e CSR via OpenSSL"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    key_file = f"{prefix}_{timestamp}.key"
    csr_file = f"{prefix}_{timestamp}.csr"

    key_path = os.path.join(OUTPUT_DIR, key_file)
    csr_path = os.path.join(OUTPUT_DIR, csr_file)

    subj = f"/C={C}/O={O}/CN={CN}/ST={ST}/L={L}/serialNumber={serialNumber}/jurisdictionCountryName=BR"

    cmd = [
        "openssl", "req", "-newkey", "rsa:2048",
        "-keyout", key_path, "-sha256", "-out", csr_path,
        "-subj", subj, "-nodes"
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr.decode()}

    # zip para download
    zip_path = os.path.join(OUTPUT_DIR, f"{prefix}_{timestamp}.zip")
    with zipfile.ZipFile(zip_path, "w") as z:
        z.write(key_path, arcname=key_file)
        z.write(csr_path, arcname=csr_file)

    return FileResponse(zip_path, filename=os.path.basename(zip_path))

@app.post("/combine")
async def combine_cert(
    cer_file: str = Form(...),
    key_file: str = Form(...),
    chain_file: str = Form("cadeia.cer"),
    pfx_name: str = Form("certificado_final.pfx"),
    password: str = Form("senha123")
):
    """Gera PFX a partir de CER + KEY + CA intermediária"""
    pfx_path = os.path.join(OUTPUT_DIR, pfx_name)
    cmd = [
        "openssl", "pkcs12", "-export",
        "-in", cer_file,
        "-inkey", key_file,
        "-certfile", chain_file,
        "-out", pfx_path,
        "-password", f"pass:{password}"
    ]
    subprocess.run(cmd, check=True)
    return FileResponse(pfx_path, filename=pfx_name)
