# Signing without surprises

You sign three things: the sign-in message (EIP-191), Hyperliquid's `approveAgent` (EIP-712) and each payment (EIP-712, `typedData` returned by `GET /pay/prepare`, signed as is).

- No wallet library? A dependency-light example with `@noble/curves` and `@noble/hashes` (tested against the server): `https://waketrades.com/docs/api/authentication`.
- MetaMask Agent Wallet: `mm wallet sign-message --message "<message>" --chain-id 42161 --wait` and `mm wallet sign-typed-data --chain-id 42161 --payload '<JSON>' --wait`. Each signature waits for the owner's approval by e-mail.
- Split EIP-712 signatures into `{r, s, v}` with **64 hex digits** for `r` and `s` (keep leading zeros) and `v` = 27 or 28.

## Python (eth-account)

```python
from eth_account import Account
from eth_account.messages import encode_defunct

acct = Account.from_key(PRIVATE_KEY)
sig_text = "0x" + bytes(acct.sign_message(encode_defunct(text=message)).signature).hex()   # step 1

typed = {
  "types": {
    "EIP712Domain": [{"name": "name", "type": "string"}, {"name": "version", "type": "string"},
                     {"name": "chainId", "type": "uint256"}, {"name": "verifyingContract", "type": "address"}],
    "HyperliquidTransaction:ApproveAgent": [{"name": "hyperliquidChain", "type": "string"}, {"name": "agentAddress", "type": "address"},
                                            {"name": "agentName", "type": "string"}, {"name": "nonce", "type": "uint64"}],
  },
  "primaryType": "HyperliquidTransaction:ApproveAgent",
  "domain": {"name": "HyperliquidSignTransaction", "version": "1", "chainId": 42161, "verifyingContract": "0x0000000000000000000000000000000000000000"},
  "message": {"hyperliquidChain": "Mainnet", "agentAddress": agent_address, "agentName": agent_name, "nonce": now_ms},
}
signed = Account.sign_typed_data(PRIVATE_KEY, full_message=typed)                          # step 4
signature = {"r": f"0x{signed.r:064x}", "s": f"0x{signed.s:064x}", "v": signed.v}   # 64 hex digits each: hex() drops leading zeros
```

The action sent with it: `{"type": "approveAgent", "hyperliquidChain": "Mainnet", "signatureChainId": "0xa4b1", "agentAddress", "agentName", "nonce"}` (same values).
