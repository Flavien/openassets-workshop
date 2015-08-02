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
        # List unspent transaction outputs

        # Color them using the coloring engine
        engine = self.create_engine()

        # Process every uncolored output
