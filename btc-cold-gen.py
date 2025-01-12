from mnemonic import Mnemonic
import hashlib
import hmac
import ecdsa
from base58 import b58encode, b58decode
import os
import qrcode_terminal
import secrets


def generate_entropy(bits=256):
    """Generate cryptographically secure entropy."""
    if bits not in [128, 160, 192, 224, 256]:
        raise ValueError("Entropy bits must be one of 128, 160, 192, 224, or 256.")
    return os.urandom(bits // 8)


def validate_mnemonic(mnemonic):
    """Validate a BIP-39 mnemonic phrase."""
    mnemo = Mnemonic("english")
    if not mnemo.check(mnemonic):
        raise ValueError("Invalid mnemonic phrase.")
    return mnemonic


def derive_master_keys(seed):
    """Derive BIP-32 master private key and chain code from the seed."""
    hmac_result = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    master_private_key = hmac_result[:32]
    master_chain_code = hmac_result[32:]
    return master_private_key, master_chain_code


def derive_child_key(parent_key, parent_chain_code, index):
    """Derive a child private key using BIP-32 hardened derivation."""
    index_bytes = (index + 0x80000000).to_bytes(4, "big")  # Hardened key
    data = b"\x00" + parent_key + index_bytes
    hmac_result = hmac.new(parent_chain_code, data, hashlib.sha512).digest()
    child_private_key = hmac_result[:32]
    child_chain_code = hmac_result[32:]
    return child_private_key, child_chain_code


def private_to_public(private_key):
    """Convert a private key to a public key using secp256k1."""
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    return b"\x04" + vk.to_string()  # Prefix 0x04 indicates uncompressed key


def public_key_to_address(public_key):
    """Convert a public key to a Bitcoin address."""
    # Step 1: Perform SHA-256 hashing on the public key
    sha256_hash = hashlib.sha256(public_key).digest()

    # Step 2: Perform RIPEMD-160 hashing on the result
    ripemd160_hash = hashlib.new("ripemd160", sha256_hash).digest()

    # Step 3: Add version byte (0x00 for mainnet Bitcoin)
    versioned_payload = b"\x00" + ripemd160_hash

    # Step 4: Create checksum (first 4 bytes of double SHA-256)
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]

    # Step 5: Append checksum to payload
    full_payload = versioned_payload + checksum

    # Step 6: Encode in Base58
    return b58encode(full_payload).decode()


def validate_bitcoin_address(address):
    """Validate the checksum of a Bitcoin address."""
    try:
        decoded = b58decode(address)
        if len(decoded) != 25:
            return False
        payload, checksum = decoded[:-4], decoded[-4:]
        valid_checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        return checksum == valid_checksum
    except ValueError:
        return False


def secure_erase(variable):
    """Overwrite a variable with random bytes before deleting it."""
    if isinstance(variable, bytes):
        overwritten = secrets.token_bytes(len(variable))
    elif isinstance(variable, str):
        overwritten = ''.join(chr(secrets.randbelow(256)) for _ in range(len(variable)))
    variable = overwritten  # Overwrite in memory
    del variable  # Delete reference


# Step 1: Generate Mnemonic and Validate
mnemo = Mnemonic("english")
entropy = generate_entropy(256)
mnemonic = mnemo.to_mnemonic(entropy)

print("\n==== Your Mnemonic Phrase ====")
print(mnemonic)
print("\nWrite this down and store it safely. You will be asked to re-enter it to verify.")
print("================================\n")

# Step 2: User Confirmation (Re-enter Mnemonic)
user_mnemonic = input("Re-enter your mnemonic phrase to confirm: ").strip()
if user_mnemonic != mnemonic:
    print("\nError: Mnemonic does not match! Restart the process and ensure you write it down correctly.")
    exit(1)

print("\nMnemonic successfully verified!\n")

# Step 3: Convert Mnemonic to Seed
passphrase = input("Enter an optional passphrase (press Enter to skip): ")
seed = mnemo.to_seed(mnemonic, passphrase=passphrase.strip())

# Step 4: Derive Master Private Key and Chain Code
master_private_key, master_chain_code = derive_master_keys(seed)

# Step 5: Derive First Hardened Child Key (No printing of private keys)
child_private_key, child_chain_code = derive_child_key(master_private_key, master_chain_code, index=0)

# Step 6: Generate Public Key and Bitcoin Address
public_key = private_to_public(child_private_key)
bitcoin_address = public_key_to_address(public_key)

if validate_bitcoin_address(bitcoin_address):
    print("\n==== Your Bitcoin Address ====")
    print(bitcoin_address)
    print("\n================================\n")
    qrcode_terminal.draw(bitcoin_address)
else:
    print("Failed - Invalid address")

# Step 7: Securely Erase Sensitive Data
secure_erase(entropy)
secure_erase(mnemonic)
secure_erase(seed)
secure_erase(master_private_key)
secure_erase(master_chain_code)
secure_erase(child_private_key)