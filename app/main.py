from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from .crypto_utils import load_private_key, decrypt_seed
from .totp_utils import generate_totp_code, verify_totp_code, seconds_until_period_end

DATA_PATH = Path("/data")
SEED_FILE = DATA_PATH / "seed.txt"
PRIVATE_KEY_PATH = Path("/app/student_private.pem")

app = FastAPI()

class SeedPayload(BaseModel):
    encrypted_seed: str

class CodePayload(BaseModel):
    code: str

@app.post("/decrypt-seed")
def decrypt_seed_api(payload: SeedPayload):
    try:
        private_key = load_private_key(str(PRIVATE_KEY_PATH))
        seed = decrypt_seed(payload.encrypted_seed, private_key)

        DATA_PATH.mkdir(parents=True, exist_ok=True)
        SEED_FILE.write_text(seed)

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not found")

    seed = SEED_FILE.read_text().strip()
    code = generate_totp_code(seed)
    valid_for = seconds_until_period_end()

    return {"code": code, "valid_for": valid_for}

@app.post("/verify-2fa")
def verify_2fa(payload: CodePayload):
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not found")

    seed = SEED_FILE.read_text().strip()
    is_valid = verify_totp_code(seed, payload.code)

    return {"valid": is_valid}

@app.get("/health")
def health():
    return {"status": "ok"}
