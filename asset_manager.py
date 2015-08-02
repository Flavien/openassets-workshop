import asyncio
import bitcoin
import providers
from pprint import pprint

class AssetManager:
    def __init__(self, bitcoin_core_url):
        self.blockchain = providers.BitcoinCoreProvider(bitcoin_core_url)
        bitcoin.params = bitcoin.TestNetParams

    def run(self):
        print("Running the AssetManager...")
        asyncio.new_event_loop().run_until_complete(self.run_loop())
        print("AssetManager terminating")

    @asyncio.coroutine
    def run_loop(self):
        unspent = yield from self.blockchain.list_unspent(addresses=None, min_confirmations=0)
        pprint(unspent)
        pass