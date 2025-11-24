from mysql.connector import Error
from mysql.connector import pooling

config1 = {
    'pool_name': 'mypool',
    'pool_size': 20,
    'pool_reset_session': True,
    'host': '10.104.16.129', # 10.104.16.129
    'user': 'athena',
    # 'password': 'Ftb181148$', # TODO
    'password': 'WGQKJPL8V/xQ',
    'database': 'depal'
}

config2 = {
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

# TODO: added new database
config3 = {
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

class MysqlDb:
    def __init__(self):
       try:
            self.depal_pool = pooling.MySQLConnectionPool(**config1)
            self.wcs_pool = pooling.MySQLConnectionPool(**config2)
            self.eip_signal_pool = pooling.MySQLConnectionPool(**config3)
            # self.depal_pool = mysql.connector.pooling.MySQLConnectionPool(**config1) #TODO to remove
            # self.wcs_pool = mysql.connector.pooling.MySQLConnectionPool(**config2) # TODO to remove

       except Error as e:
            print(f"Error while connecting to MySQL using Connection pool {e}")

    def get_connection(self,db):
        if db == 'depal':
            return self.depal_pool.get_connection()
        # elif db == 'wcs': TODO
        elif db == 'futaba-chiryu-3building':
            return self.wcs_pool.get_connection()
        elif db == 'eip_signal': #TODO: added
            return self.eip_signal_pool.get_connection()
        else:
            raise ValueError("Invalid database name")
  
