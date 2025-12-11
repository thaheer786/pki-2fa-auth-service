#!/usr/bin/env python3
import sys
import base64
from app.crypto_utils import (
    load_private_key,
    load_public_key,
    sign_message,
    encrypt_with_public_key
)

if len(sys.argv) < 2:
    print("Usage: sign_commit.py <commit-hash>")
    sys.exit(2)

commit_hash = sys.argv[1].strip()

if len(commit_hash) != 40:
    print("Commit hash must be 40 hex characters.")
    sys.exit(2)

# Load student private key
priv_key = load_private_key("student_private.pem")

# Step 1: Sign commit hash using RSA-PSS-SHA256
signature = sign_message(commit_hash, priv_key)

# Step 2: Load instructor public key
instr_pub = load_public_key("instructor_public.pem")

# Step 3: Encrypt signature using RSA-OAEP-SHA256
encrypted = encrypt_with_public_key(signature, instr_pub)

# Step 4: Output as base64 (single line)
print(base64.b64encode(encrypted).decode("utf-8"))
