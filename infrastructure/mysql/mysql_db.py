from mysql.connector import Error
from mysql.connector import pooling
from config.config import MYSQL_DEPAL_DB, MYSQL_WCS_DB, MYSQL_EIP_DB  # "database":は都度設定する


class MysqlDb:
    def __init__(self):
        try:
            self.depal_pool = pooling.MySQLConnectionPool(**MYSQL_DEPAL_DB)
            self.wcs_pool = pooling.MySQLConnectionPool(**MYSQL_WCS_DB)
            self.eip_signal_pool = pooling.MySQLConnectionPool(**MYSQL_EIP_DB)

        except Error as e:
            print(f"Error while connecting to MySQL using Connection pool {e}")

    def get_connection(self, db):
        if db == 'depal':
            return self.depal_pool.get_connection()
        # elif db == 'wcs': # TODO➞リン
        elif db == 'futaba-chiryu-3building':
            return self.wcs_pool.get_connection()
        elif db == 'eip_signal':  # TODO➞リン: added
            return self.eip_signal_pool.get_connection()
        else:
            raise ValueError("Invalid database name")
