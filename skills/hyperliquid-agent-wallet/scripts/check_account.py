"""Show a Hyperliquid account's balances and mode. Read-only, no key needed.

Usage: python check_account.py 0xADDRESS [--testnet]
"""
import json
import os
import ssl
import sys
import urllib.request

def _ssl_context() -> ssl.SSLContext:
    """Default CA store, else the first CA bundle found (some Python installs ship without one)."""
    ctx = ssl.create_default_context()
    if ctx.get_ca_certs() or ssl.get_default_verify_paths().cafile:
        return ctx
    candidates = ["/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt"]
    try:
        import certifi
        candidates.insert(0, certifi.where())
    except ImportError:
        pass
    for path in candidates:
        if os.path.exists(path):
            return ssl.create_default_context(cafile=path)
    return ctx


_CTX = _ssl_context()


def info(base: str, body: dict):
    req = urllib.request.Request(base + "/info", data=json.dumps(body).encode(), headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=15, context=_CTX) as r:
        return json.load(r)


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit("usage: python check_account.py 0xADDRESS [--testnet]")
    user = args[0].lower()
    base = "https://api.hyperliquid-testnet.xyz" if "--testnet" in sys.argv else "https://api.hyperliquid.xyz"
    perps = info(base, {"type": "clearinghouseState", "user": user})
    spot = info(base, {"type": "spotClearinghouseState", "user": user})
    mode = info(base, {"type": "userAbstraction", "user": user})
    usdc_spot = next((b["total"] for b in spot.get("balances", []) if b["coin"] == "USDC"), "0")
    print(json.dumps({
        "network": "testnet" if "testnet" in base else "mainnet",
        "address": user,
        "perpsAccountValue": perps["marginSummary"]["accountValue"],
        "perpsWithdrawable": perps["withdrawable"],
        "spotUsdc": usdc_spot,
        "openPositions": len(perps.get("assetPositions", [])),
        "accountMode": mode,
    }, indent=2))


if __name__ == "__main__":
    main()
