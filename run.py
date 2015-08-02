import asyncio
import providers
from asset_manager import AssetManager

#
# Prerequisites on Windows:
# - Install OpenSSL: http://slproweb.com/products/Win32OpenSSL.html
#   e.g. http://slproweb.com/download/Win64OpenSSL_Light-1_0_1p.exe
#

if __name__ == '__main__':
    event_loop = asyncio.new_event_loop()

    bitcoin_core_url = "http://<username>:<password>@localhost:18332"
    chain_base_url = "https://api.chain.com/v1/testnet3/"
    chain_api = "<apikey>"
    chain_secret = "<apisecret>"

    vending_machine_address = ""
    storage_address = ""
    issuance_address = ""

    bitcoin_core = providers.BitcoinCoreProvider(bitcoin_core_url)
    # chain = providers.ChainApiProvider(chain_base_url, chain_api, chain_secret, bitcoin_core, event_loop)

    asset_manager = AssetManager(event_loop, bitcoin_core, vending_machine_address, storage_address, issuance_address, 5)
    asset_manager.run()