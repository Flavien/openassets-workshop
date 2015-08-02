import asyncio

class AssetManager:
    def __init__(self, bitcoin_core_url):
        self.bitcoin_core_url = bitcoin_core_url

    def run(self):
        print("Running the AssetManager...")
        asyncio.new_event_loop().run_until_complete(self.run_loop())
        print("AssetManager terminating")

    @asyncio.coroutine
    def run_loop(self):
        pass