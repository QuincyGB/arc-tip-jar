"""Send a real test tip through ArcTipJar on Arc mainnet."""
import json
from web3 import Web3

RPC = "https://rpc.mainnet.arc.io"
CHAIN_ID = 5042

w3 = Web3(Web3.HTTPProvider(RPC, request_kwargs={"timeout": 30}))
key = open("/home/hatch/.evm-wallet/key").read().strip()
acct = w3.eth.account.from_key(key)

dep = json.load(open("deployment.json"))
compiled = json.load(open("ArcTipJar.json"))
jar = w3.eth.contract(address=dep["address"], abi=compiled["abi"])

tip_amount = w3.to_wei(0.01, "ether")  # 0.01 native USDC (18 decimals on Arc)
recipient = acct.address  # test tip to self

fn = jar.functions.tip(recipient, "first tip on Arc — gas is USDC!")
gas_est = fn.estimate_gas({"from": acct.address, "value": tip_amount})
tx = fn.build_transaction({
    "from": acct.address,
    "value": tip_amount,
    "nonce": w3.eth.get_transaction_count(acct.address),
    "gas": int(gas_est * 1.2),
    "gasPrice": w3.eth.gas_price,
    "chainId": CHAIN_ID,
})
signed = w3.eth.account.sign_transaction(tx, key)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print("tip tx:", tx_hash.hex())
receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
print("status:", receipt.status, "| gas used:", receipt.gasUsed)

# Verify on-chain state + event
print("totalReceived:", jar.functions.totalReceived(recipient).call())
print("tipCount:", jar.functions.tipCount(recipient).call())
print("totalTips:", jar.functions.totalTips().call())
logs = jar.events.Tip().process_receipt(receipt)
for l in logs:
    print("event Tip:", l.args["from"], "->", l.args["to"],
          w3.from_wei(l.args["amount"], "ether"), "USDC |", l.args["memo"])
json.dump({"tipTx": tx_hash.hex(), "gasUsed": receipt.gasUsed},
          open("test-tip.json", "w"), indent=1)
