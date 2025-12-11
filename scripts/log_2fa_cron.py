#!/usr/bin/env python3
import os
from datetime import datetime, timezone
from app.totp_utils import generate_totp_code

SEED_PATH = '/data/seed.txt'

if __name__ == '__main__':
    try:
        if not os.path.exists(SEED_PATH):
            print("Seed file not found", flush=True)
            raise SystemExit(1)

        with open(SEED_PATH, 'r') as f:
            hex_seed = f.read().strip()

        code = generate_totp_code(hex_seed)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        print(f"{timestamp} - 2FA Code: {code}", flush=True)

    except Exception as e:
        import sys
        print(f"ERROR: {e}", file=sys.stderr, flush=True)
        raise SystemExit(1)
