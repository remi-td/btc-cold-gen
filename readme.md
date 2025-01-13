# **Bitcoin Cold Wallet Generator**

## **Overview**
A **secure, offline Bitcoin cold wallet generator**. It creates a **BIP-39 mnemonic seed phrase**, derives a **BIP-32 hierarchical deterministic (HD) wallet**, and generates a **Bitcoin address** without exposing private keys. This is a minimal implementation, can be used in an air-gapped way to generate Bitcoin wallets without relying on third-party software. 

## **Disclaimer**
This tool is provided as-is and primarily intended for education purposes. The authors are not responsible for any loss of funds or security breaches. Use it at your own risk, and always follow best practices for cold storage.

## **Features**
- **Generates a secure Bitcoin wallet offline**
- **Displays a mnemonic phrase (BIP-39) for manual backup**
- **Validates mnemonic input to ensure correct storage**
- **Generates a Bitcoin address (Base58Check encoded)**
- **Displays a QR code for easy address sharing**
- **Does NOT display private keys on-screen**
- **Securely erases sensitive data from memory**

## **Requirements**
- Python 3.x
- Dependencies listed in requirements.txt:
  ```sh
  pip install mnemonic ecdsa qrcode-terminal base58
  ```

## **Usage**
### **1. Run the Script**
```sh
python btc-cold-gen.py
```

### **2. Follow the On-Screen Instructions**
- The script will generate and display a **12/24-word mnemonic phrase**.
- You **must** write it down and store it safely.
- You will be required to **re-enter the mnemonic** to confirm you’ve stored it correctly.
- A **Bitcoin address** will be generated and displayed along with a **QR code**.

### **3. Secure Your Mnemonic**
- The **mnemonic phrase is your wallet**. Losing it means losing access to your Bitcoin.
- **Do not store the mnemonic digitally** (e.g., no screenshots, no text files).
- Consider storing it on **paper, metal backup, or another durable medium**.

## **Security Best Practices**
- **Run this script on an air-gapped machine** (a computer that is never connected to the internet).
- **Use a clean operating system** (e.g., boot a fresh Linux Live USB).
- **Never share your mnemonic phrase with anyone**.
- **Ensure your environment is free from malware or keyloggers**.

## **FAQ**
### **Q: Can I use this script to restore a wallet?**
A: No. This script only generates new wallets. To restore a wallet, use a Bitcoin wallet that supports **BIP-39 recovery**.

### **Q: Where is my private key?**
A: The private key is **derived from the mnemonic**. As long as you have your mnemonic, you can restore your wallet and access your funds.

### **Q: Can I use this script for other cryptocurrencies?**
A: No. This script is **Bitcoin-specific** and does not support Ethereum, Monero, or other coins.

## **Contributing**
Contributions are welcome! If you’d like to improve this script, submit a pull request or open an issue.

## **License**
MIT License – Free to use, modify, and distribute.