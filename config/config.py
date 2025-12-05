# コンフィグレーション 設定*-

# depalデータベース接続　
MYSQL_DEPAL_DB = {
    'pool_name': 'mypool',
    'pool_size': 20,
    'pool_reset_session': True,
    'host': '10.104.16.129', # 10.104.16.129
    'user': 'athena',
    # 'password': 'Ftb181148$', # TODO
    'password': 'WGQKJPL8V/xQ',
    'database': 'depal'
}

# wcs/futaba-chiryu-3building データベース接続　
MYSQL_WCS_DB = {
    'pool_name': 'mypool',
    'pool_size': 20,
    'pool_reset_session': True,
    'host': '10.104.16.129', # 10.104.16.129
    'user': 'athena',
    # 'password': 'Ftb181148$', # TODO
    'password': 'WGQKJPL8V/xQ',
    # 'database': 'wcs' # TODO
    'database': 'futaba-chiryu-3building'
}

# eip_signal データベース接続
MYSQL_EIP_DB = {
    'pool_name': 'mypool',
    'pool_size': 20,
    'pool_reset_session': True,
    'host': '10.104.16.129', # 10.104.16.129
    'user': 'athena',
    # 'password': 'Ftb181148$', # TODO
    'password': 'WGQKJPL8V/xQ',
    # 'database': 'wcs' # TODO
    'database': 'eip_signal'
}

# LOG
LOG_FOLDER = "../log"
BACKUP_DAYS = 120
LOG_LEVEL = "INFO"  # DEBUG, INFO, NOTSET, WARN, ERORR, CRITICAL
ENCODING = "utf-8"


