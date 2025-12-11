import pyotp
import base64

def hex_to_base32(hex_seed: str) -> str:
    b = bytes.fromhex(hex_seed)
    b32 = base64.b32encode(b).decode("utf-8")
    return b32.rstrip("=")

def generate_totp_code(hex_seed: str) -> str:
    b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32, digits=6, interval=30, digest="sha1")
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, window: int = 1) -> bool:
    b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32, digits=6, interval=30, digest="sha1")
    return totp.verify(code, valid_window=window)

def seconds_until_period_end():
    import time
    period = 30
    return period - (int(time.time()) % period)
