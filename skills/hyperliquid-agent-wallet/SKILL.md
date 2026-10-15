---
name: hyperliquid-agent-wallet
description: Give an AI agent its own Hyperliquid wallet - create it (local key by default, or MetaMask Agent Wallet with guardrails), get it funded with one human step (the owner sends USDC), claim testnet USDC to practice, then check balance and account mode. Use before trading or copy trading on Hyperliquid when the agent has no funded wallet yet.
---

# Your own Hyperliquid wallet, as an agent

> **Risk first.** This wallet will hold real money. Keep its key secret, ask the owner for a small amount to start, and never let anyone else sign with it. Trading on Hyperliquid, leveraged or copied, can lose the whole balance.

A Hyperliquid account is just an Ethereum address. You create the key; Hyperliquid creates the account the first time USDC arrives. The **only human step** is the owner sending you USDC.

## 1. Create the wallet - pick one way

**A. Local key (default, fully autonomous).** No account anywhere, every signature is yours.

Run the scripts from this skill's folder, in a virtual environment (many Pythons refuse a system-wide `pip install`):

```bash
cd <this skill's folder>
python3 -m venv .venv && .venv/bin/pip install eth-account
.venv/bin/python scripts/create_wallet.py ~/.hyperliquid-agent/wallet.key
```

It writes a new private key to that file (permissions `600`) and prints the address. Keep the file outside any repository, never print or send the key, and give the owner a backup if they ask for one.

**B. MetaMask Agent Wallet (guardrails).** The key stays in MetaMask's secure enclave; daily outflow limits and an allowlist apply. The owner approves **each signature by e-mail**, so this way is not hands-free.

```bash
npm install -g @metamask/agent-wallet     # or install in a local folder
mm login browser                          # the owner signs in once (Google, e-mail, or QR with MetaMask Mobile)
mm init --wallet server-wallet --mode guard
mm wallet address
```

Sign later with `mm wallet sign-message ... --wait` and `mm wallet sign-typed-data ... --wait`. Docs: `https://docs.metamask.io/agent-wallet/`.

## 2. Get funded - the one human step

**How much to ask for.** Only what the owner can afford to lose. To copy traders with WakeTrades, plan for **at least 300 USDC** (the Risky level's minimum; 550 for Balanced, 1,100 for Prudent): below that, copies still open but at Hyperliquid's 11 USDC minimum order, bigger than your level's share. The WakeTrades plan is paid in USDC from this wallet after the 14-day free trial.

Send the owner this, with your address and the amount:

> Please send **<amount> USDC** to my Hyperliquid address `0x...`: on app.hyperliquid.xyz, **Send** (a free internal transfer). Hyperliquid charges **you, the sender, a one-time 1 USDC** when an address receives its first transfer. Start small.

Other way for the owner: deposit native USDC from Arbitrum through Hyperliquid's bridge (minimum 5 USDC; less is lost).

Then wait and check (step 4) until the USDC shows up. A transfer can land in **spot** (`spotUsdc`) on a new account in `default` mode: that is fine for WakeTrades, which switches the account to unified, where spot USDC backs perps margin.

## 3. Practice on testnet (optional, no human step)

Once your address exists on mainnet (step 2 done), claim mock USDC with the same address:

```bash
curl -s -X POST https://api.hyperliquid-testnet.xyz/info -H 'content-type: application/json' \
  -d '{"type":"claimDrip","user":"0xYOUR_ADDRESS"}'
```

It answers HTTP 200 even when it refuses: read the body. `"Cannot claim drip because user ... does not exist on mainnet."` means step 2 is not done yet; a claim works once per address.

Testnet API: `https://api.hyperliquid-testnet.xyz` · app: `https://app.hyperliquid-testnet.xyz`. Practice signing and placing orders there; testnet funds have no value.

## 4. Check the account

```bash
.venv/bin/python scripts/check_account.py 0xYOUR_ADDRESS            # mainnet
.venv/bin/python scripts/check_account.py 0xYOUR_ADDRESS --testnet
```

It prints the perps balance, the spot USDC and the account mode (`userAbstraction`). On a **unified** account, spot USDC backs perps margin. On a `default` (standard) account, perps only use the perps balance: USDC that landed in spot must be moved to perps, or the account switched to unified (WakeTrades does the switch for you).

## Next: copy trade with WakeTrades

Your wallet is funded. To have top Hyperliquid traders copied onto it 24/7, while your funds stay on your account and only you can withdraw, use the **`waketrades-copy-trading`** skill: `https://waketrades.com/docs/api/`.

## Never

- Never paste the private key into a chat, a log, a URL or a request.
- Never sign a message or typed data you did not build or check.
- Never move the owner's funds anywhere they did not ask for.
