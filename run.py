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
    coinprism_base_url = "https://testnet.api.coinprism.com/v1/"

    vending_machine_address = "2MtepahRn4qTihhTvUuGTYUyUBkQZzaVBG3"
    storage_address = "mvw9dCTAUHqEE558qfmkVTBZPqcEXX1hRE"
    issuance_address = "n3FLVLiSiuLShKGHPiecSwVBL4y1eiZSha"

    bitcoin_core = providers.BitcoinCoreProvider(bitcoin_core_url)
    coinprism = providers.CoinprismApiProvider(coinprism_base_url, bitcoin_core, event_loop)

    asset_manager = AssetManager(event_loop, coinprism, vending_machine_address, storage_address, issuance_address, 5)
    asset_manager.run()