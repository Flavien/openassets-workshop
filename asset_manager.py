import asyncio
import bitcoin
import bitcoin.wallet
import openassets.protocol
import openassets.transactions
from pprint import pprint

class AssetManager:
    def __init__(self, event_loop, blockchain,
                 vending_machine_address, storage_address, issuance_address,  satoshis_per_unit):
        self.event_loop = event_loop
        self.blockchain = blockchain
        self.vending_machine_address = vending_machine_address
        self.storage_address = storage_address
        self.issuance_address = issuance_address
        self.satoshis_per_unit = satoshis_per_unit
        bitcoin.params = bitcoin.TestNetParams

    def create_engine(self):
        cache = openassets.protocol.OutputCache()
        return openassets.protocol.ColoringEngine(self.blockchain.get_transaction, cache, self.event_loop)

    def run(self):
        print("Running the asset manager...")
        self.event_loop.run_until_complete(self.run_loop())
        print("Asset manager terminating")

    @asyncio.coroutine
    def run_loop(self):
        unspent = yield from self.blockchain.list_unspent(addresses=[self.vending_machine_address])
        pprint(unspent)

        engine = self.create_engine()

        for item in unspent:
            output_result = yield from engine.get_output(item['outpoint'].hash, item['outpoint'].n)
            output = openassets.transactions.SpendableOutput(
                bitcoin.core.COutPoint(item['outpoint'].hash, item['outpoint'].n), output_result)
            if output.output.asset_id is None:
                print("\nProcessing inboud transaction " + str(output.out_point) + "\n\t" + str(output.output))

                transaction = yield from self.process_output(output)
                print(transaction)

                signed_transaction = yield from self.blockchain.sign_transaction(transaction)

                result = yield from self.blockchain.send_transaction(signed_transaction["tx"])
                print("Transaction hash: " + bitcoin.core.b2lx(result))


    @asyncio.coroutine
    def process_output(self, output):

        issuance_unspent = yield from self.blockchain.list_unspent(addresses=[self.issuance_address])
        engine = self.create_engine()
        colored_issuance_unspent = yield from engine.get_output(
            issuance_unspent[0]['outpoint'].hash, issuance_unspent[0]['outpoint'].n)
        issuance_output = openassets.transactions.SpendableOutput(
            bitcoin.core.COutPoint(issuance_unspent[0]['outpoint'].hash, issuance_unspent[0]['outpoint'].n),
            colored_issuance_unspent)

        print("Using " + str(issuance_output.out_point) + " for issuance\n\t" + str(issuance_output.output))

        inputs = [
            bitcoin.core.CTxIn(issuance_output.out_point),
            bitcoin.core.CTxIn(output.out_point)
        ]

        buyer_script = yield from self.get_buyer_script(output.out_point.hash)
        print("Buyer's script: " + str(buyer_script))

        output_quantity_list = [int(output.output.value / self.satoshis_per_unit)]
        payload = openassets.protocol.MarkerOutput(output_quantity_list, b'').serialize_payload()
        marker_output_script = openassets.protocol.MarkerOutput.build_script(payload)
        storage_script = bitcoin.wallet.CBitcoinAddress(self.storage_address).to_scriptPubKey()

        outputs = [
            bitcoin.core.CTxOut(600, bitcoin.core.CScript(buyer_script)),
            bitcoin.core.CTxOut(0, marker_output_script),
            bitcoin.core.CTxOut(output.output.value - 10000, storage_script),
            bitcoin.core.CTxOut(issuance_output.output.value - 600, issuance_output.output.script)
        ]

        return bitcoin.core.CTransaction(
            vin=inputs,
            vout=outputs)

    @asyncio.coroutine
    def get_buyer_script(self, transaction_hash):
        inbound_transaction = yield from self.blockchain.get_transaction(transaction_hash)
        out_point = inbound_transaction.vin[0].prevout
        funding_transaction = yield from self.blockchain.get_transaction(out_point.hash)
        return funding_transaction.vout[out_point.n].scriptPubKey