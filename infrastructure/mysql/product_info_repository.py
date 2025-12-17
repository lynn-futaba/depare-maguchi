from datetime import datetime, date, time

from domain.models.product import ProductInfo, Product
from domain.infrastructure.product_info_repository import IProductInfoRepository


# mysql実装
class ProductInfoRepository(IProductInfoRepository):

    def __init__(self, db):
        self.db = db

    def get_product(self, line_id: int) -> Product:
        try:
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            sql = f"SELECT product_id, kanban_no, name FROM depal.futaba_product inner join depal.line_product using(product_id) WHERE line_id={line_id};"
            cur.execute(sql)
            result = cur.fetchall()

            # print(f"[ProductInfoRepository >> Get_product >> Query Result] : {result}")

            for row in result:
                product = Product(row["product_id"], row["kanban_no"], line_id, row["name"])

        except Exception as e:
            print(f"ProductInfoRepository >> Get_product >> Error] : {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        return product

    def get_product_info(self, line_id: int) -> ProductInfo:
        try:
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            product = self.get_product(line_id)
            
            start = datetime.combine(date.today(), time.min)
            end = datetime.combine(date.today(), time.max)

            sql = f"SELECT count(*) as count FROM depal.production WHERE product_id='{product.id}' AND time_stamp between '{start}' AND '{end}' group by product_id;"
            cur.execute(sql)
            result = cur.fetchall()

            # print(f"[ProductInfoRepository >> Get_product_info >> Query Result] : {result}")

            #resultが０
            if len(result) == 0:
                product_info = ProductInfo(product, 0, 0)
                return product_info

            for row in result:
                product_info = ProductInfo(product, row["count"], row["count"])
  
        except Exception as e:
            print(f"[ProductInfoRepository >> Get_product_info >> Error] : {e}")

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

        return product_info 


if __name__ == "__main__":

    from mysql_db import MysqlDb
    db = MysqlDb()
    repo = ProductInfoRepository(db)
    product_info = repo.get_product_info(1)
    print(product_info)




   

   




