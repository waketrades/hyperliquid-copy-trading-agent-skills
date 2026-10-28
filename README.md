# Hyperliquid copy trading - agent skills by WakeTrades

Two [Agent Skills](https://agentskills.io) and an MCP server that let an AI agent **open its own Hyperliquid wallet** and **copy Hyperliquid traders onto it, end to end** (traders you choose, or from our monthly report), with [WakeTrades](https://waketrades.com).

> **Risk first.** Copying leveraged trades can lose the whole balance. Start with a small amount, use the exposure level WakeTrades recommends for your balance, and only act for a wallet owner who gave you that mandate.
>
> **Not for Restricted Persons** ([Terms](https://waketrades.com/terms), section 3): people from the United States, Canada, the United Kingdom, China, Ukraine, Venezuela or sanctioned countries, and anyone acting for them.

| Skill | What it does | Human steps |
|---|---|---|
| [`hyperliquid-agent-wallet`](skills/hyperliquid-agent-wallet/SKILL.md) | Create the agent's wallet (local key by default, or MetaMask Agent Wallet with guardrails), get it funded, practice on testnet, check the account | **One**: the owner sends USDC |
| [`waketrades-copy-trading`](skills/waketrades-copy-trading/SKILL.md) | Sign in, pick a level and traders, alerts by webhook, trade-only key, pay, monitor, pause, exit | **None** with a local key |

## Why WakeTrades

- **Your funds stay on your account.** WakeTrades gets a trading key that can place and close orders and can never withdraw.
- **24/7.** The copy keeps running while your agent is offline.
- **Any trader**, not only vault owners, scaled to your balance, with four exposure levels.
- **No profit share.** One flat plan price, and you can stop or leave at any moment.

## Install

**Any agent that supports skills** ([skills CLI](https://github.com/vercel-labs/skills)):

```bash
npx skills add waketrades/hyperliquid-copy-trading-agent-skills
```

**Claude Code** (skills and the MCP server in one plugin):

```
/plugin marketplace add waketrades/hyperliquid-copy-trading-agent-skills
/plugin install waketrades-hyperliquid@waketrades
```

**MCP only**, in any MCP client (streamable HTTP, no OAuth):

```json
{ "mcpServers": { "waketrades": { "type": "http", "url": "https://waketrades.com/mcp" } } }
```

After sign-in, add `"headers": { "Authorization": "Bearer <session_token>" }` to that entry: the token stays out of tool arguments and transcripts (a `session_token` tool argument is refused).

## Learn more

- Agent API guide: https://waketrades.com/docs/api/
- OpenAPI: https://waketrades.com/openapi.json
- For agents: https://waketrades.com/llms.txt
- Terms: https://waketrades.com/terms

## Versions

Each release is a git tag (`v1.1.0`, …) and the plugin's `version`. Read the changes between two tags before you update: these skills tell an agent what to sign.

## Official sources only

The only official WakeTrades skills are in this repository, linked from https://waketrades.com/docs/api/. WakeTrades never asks for a private key or a seed phrase, and only ever talks to `https://waketrades.com` and Hyperliquid's own API. A copy that sends you elsewhere is not ours.

## Security

Found a vulnerability? See [SECURITY.md](SECURITY.md).

## License

Code and text: [MIT](LICENSE). The WakeTrades name and logo are not covered by this license.

WakeTrades is independent: it is not affiliated with, endorsed by or operated by Hyperliquid. "Hyperliquid" is used only to say which network these skills work with.
