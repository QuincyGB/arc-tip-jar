"""Deploy ArcTipJar to Arc mainnet. Key is read from ~/.evm-wallet/key (600), never logged."""
import json
from web3 import Web3

RPC = "https://rpc.mainnet.arc.io"
CHAIN_ID = 5042

w3 = Web3(Web3.HTTPProvider(RPC, request_kwargs={"timeout": 30}))
assert w3.is_connected(), "RPC not reachable"

key = open("/home/hatch/.evm-wallet/key").read().strip()
acct = w3.eth.account.from_key(key)
print("deployer:", acct.address)

compiled = json.load(open("ArcTipJar.json"))
contract = w3.eth.contract(abi=compiled["abi"], bytecode=compiled["bytecode"])

# Estimate gas, then add a small buffer
gas_est = contract.constructor().estimate_gas({"from": acct.address})
gas_price = w3.eth.gas_price
print("gas estimate:", gas_est, "| gas price (wei):", gas_price)

tx = contract.constructor().build_transaction({
    "from": acct.address,
    "nonce": w3.eth.get_transaction_count(acct.address),
    "gas": int(gas_est * 1.2),
    "gasPrice": gas_price,
    "chainId": CHAIN_ID,
})
signed = w3.eth.account.sign_transaction(tx, key)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print("tx hash:", tx_hash.hex())

receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
print("status:", receipt.status)
print("contract:", receipt.contractAddress)
print("gas used:", receipt.gasUsed)
json.dump({"address": receipt.contractAddress, "tx": tx_hash.hex(),
           "gasUsed": receipt.gasUsed, "gasPrice": str(gas_price)},
          open("deployment.json", "w"), indent=1)
