import asyncio
import bitcoin
import openassets.protocol
import providers
from pprint import pprint

class AssetManager:
    def __init__(self, bitcoin_core_url):
        self.event_loop = asyncio.new_event_loop()
        self.blockchain = providers.BitcoinCoreProvider(bitcoin_core_url)
        bitcoin.params = bitcoin.TestNetParams

    def create_engine(self):
        cache = openassets.protocol.OutputCache()
        return openassets.protocol.ColoringEngine(self.blockchain.get_transaction, cache, self.event_loop)

    def run(self):
        print("Running the AssetManager...")
        self.event_loop.run_until_complete(self.run_loop())
        print("AssetManager terminating")

    @asyncio.coroutine
    def run_loop(self):
        unspent = yield from self.blockchain.list_unspent(addresses=None, min_confirmations=0)
        pprint(unspent)
        pass