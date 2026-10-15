"""Create a new Hyperliquid (Ethereum) wallet for an agent.

Usage: python create_wallet.py PATH_TO_KEY_FILE
Writes the private key to PATH (permissions 600, refuses to overwrite) and prints only the address.
"""
import os
import sys

from eth_account import Account


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python create_wallet.py PATH_TO_KEY_FILE")
    path = os.path.expanduser(sys.argv[1])
    if os.path.exists(path):
        sys.exit(f"{path} already exists: refusing to overwrite a key")
    os.makedirs(os.path.dirname(path) or ".", mode=0o700, exist_ok=True)
    acct = Account.create()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(acct.key.hex() + "\n")
    print(acct.address)


if __name__ == "__main__":
    main()
