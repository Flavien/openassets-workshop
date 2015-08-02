from asset_manager import AssetManager

if __name__ == '__main__':
    bitcoin_core_url = "http://generated_by_armory:G17aGhX5wsGjZeY3vQXRLEXHAq1ont3Wso6yPAHS3HHH@localhost:18332"
    asset_manager = AssetManager(bitcoin_core_url)
    asset_manager.run()