# ArcTipJar 🫙

A tiny tipping dApp built for **Arc mainnet** — where the gas token *is* USDC.

Tip anyone in native USDC with an on-chain memo. No custody, no vaults, no
middlemen: value flows straight from tipper to recipient, and the memo lives
on-chain forever.

**Live on Arc mainnet:** [`0xBD437E3378eae16a082580e26157575523Ba852f`](https://explorer.arc.io/address/0xBD437E3378eae16a082580e26157575523Ba852f)

## Why Arc?

On most chains, tipping means: hold ETH for gas + hold the token you want to
tip. On Arc, gas *is* USDC — one balance does everything. ArcTipJar is built
around that: `tip()` is `payable`, the tip amount *is* the native value, and
there's nothing else to manage.

## Contract

`contracts/ArcTipJar.sol` (Solidity 0.8.20, MIT)

```solidity
function tip(address payable to, string calldata memo) external payable
```

- `msg.value` (native USDC, 18 decimals) is forwarded directly to `to`
- Memo (≤280 chars) recorded on-chain, `Tip(from, to, amount, memo)` emitted
- Tracks `totalReceived` / `tipCount` per recipient

## Try it

```bash
pip install web3
# scripts/test_tip.py sends a 0.01 USDC tip with a memo (edit recipient first)
python scripts/test_tip.py
```

Needs an Arc RPC (`https://rpc.mainnet.arc.io`, chain ID 5042) and a funded key.

## Deployed

| | |
|---|---|
| Contract | `0xBD437E3378eae16a082580e26157575523Ba852f` |
| Network | Arc mainnet (chain ID 5042) |
| Deploy tx | `0x090d02ca7bc17965f541e91d425469c013cbf1224c0b99e097021c48ef91da72` |
| Test tip tx | `0x875b5ef21ffa8c9a6f2fba3598f8633eefe0698bf036277a5035925daf135341` |
| Explorer | https://explorer.arc.io/address/0xBD437E3378eae16a082580e26157575523Ba852f |

Built for the Circle Arc Microgrants on DoraHacks.
