from domain.models.line import Line, LineFrontage
from domain.models.part import Part, Inventory
from domain.models.shelf import FlowRack

from domain.infrastructure.line_repository import ILineRepository
from common.setup_logger import setup_log  # ログ用
from config.config import BACKUP_DAYS  # ログ用

import logging

# ログ出力開始
LOG_FOLDER = "../log"
LOG_FILE = "line_repository.py_logging.log"
setup_log(LOG_FOLDER, LOG_FILE, BACKUP_DAYS)

#mysql実装
class LineRepository(ILineRepository):
    def __init__(self,db):
         self.db =db

    # def get_lines(self, line_id_list: list) -> list[Line]:
    #     lines = []
    #     conn = None
    #     cur = None

    #     try:
    #         # Get DB connection
    #         conn = self.db.depal_pool.get_connection()
    #         cur = conn.cursor(dictionary=True)

    #         # 1. Fetch lines TODO: check CONSTRAINT in application layer if line_id exists or not
    #         sql = f"SELECT * FROM depal.line WHERE line_id IN ({','.join(['%s'] * len(line_id_list))})"
    #         cur.execute(sql, line_id_list)
    #         result = cur.fetchall()
    #         # print(f"[Line Table >>] Query Result: {result}")

    #         for row in result:
    #             line = Line(row["line_id"], row["name"], row["process"])
    #             lines.append(line)

    #         # 2. Fetch frontages for each line
    #         for line in lines:
    #             sql =f"SELECT * FROM depal.line_frontage where line_id = {line.id};"
    #             cur.execute(sql)
    #             frontages_result = cur.fetchall()
    #             # print(f"[Line Frontage >> Query Result] : {frontages_result}")

    #             for row in frontages_result:
    #                 frontage_obj = LineFrontage(row["cell_code"], row["name"], row["frontage_id"], row["car_model_id"])
    #                 line.register_frontage(frontage_obj)
                
    #             # 3. Fetch inventories for each frontage
    #             for frontage in line.frontages.values():
    #                 # print(f"[Frontage >> ID] : {frontage.id}")

    #                 sql = f"SELECT * FROM depal.line_inventory inner join depal.m_product using(part_number) where depal.line_inventory.frontage_id = {frontage.id};"
    #                 cur.execute(sql)

    #                 inv_result = cur.fetchall()
    #                 # print(f"[Line Inventory >> Query Result] : {inv_result}")

    #                 inventories = []
    #                 for row in inv_result:
    #                     # part = Part(row["part_number"], row["kanban_no"], row["name"], row["car_model_id"]) TODO: comment out
    #                     part = Part(row["part_number"], row["kanban_no"], row["supplier_name"], row["car_model_id"])
    #                     inventory = Inventory(row["inventory_id"], part, row["case_quantity"])
    #                     inventories.append(inventory)

    #                 frontage.set_inventories(inventories)

    #     except Exception as e:
    #         print(f"[LineRepository >> Error] : {e}")

    #     finally:
    #         if cur:
    #             cur.close()
    #         if conn:
    #             conn.close()

    #     return lines
    
    # TODO➞リン: Handle DB CONSTRAINTS in the application layer because there is no root or DB admin permission in the dababase
    def validate_line_ids(self, line_id_list: list) -> set[int]:
        """
        EN: Validate that the given line_id_list exists in depal.line table.
        JP: 指定された line_id_list が depal.line テーブルに存在するか確認します。
        Returns a set of valid line IDs.
        JP: 有効な line_id のセットを返します。
        """
        conn = None
        cur = None
        valid_ids = set()

        try:
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            # EN: If no IDs provided, return empty set
            # JP: ID が指定されていない場合、空のセットを返す
            if not line_id_list:
                logging.error(f"[LineRepository >> validate_line_ids() >> No valid IDs found] : {e}")
                return valid_ids

            # EN: Check if line_id exists in depal.line
            # JP: depal.line テーブルで line_id が存在するか確認
            sql = f"SELECT line_id FROM depal.line WHERE line_id IN ({','.join(['%s'] * len(line_id_list))})"
            cur.execute(sql, line_id_list)
            rows = cur.fetchall()
            valid_ids = {row["line_id"] for row in rows}

        except Exception as e:
            logging.error(f"[LineRepository >> validate_line_ids() >> Validation エラー] : {e}")

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

        return valid_ids


    def get_lines(self, line_id_list: list) -> list[Line]:
        """
        EN: Fetch lines and their related frontages and inventories.
        JP: ラインと関連するフロンテージおよび在庫情報を取得します。
        Uses application-layer validation for line_id.
        JP: line_id の検証をアプリケーション層で実施します。
        """
        lines = []
        conn = None
        cur = None

        try:
            # EN: Step 1 - Validate line IDs
            # JP: ステップ1 - line_id を検証
            valid_ids = self.validate_line_ids(line_id_list)

            # EN: If no valid IDs, return empty list
            # JP: 有効な ID がない場合、空のリストを返す
            if not valid_ids:
                logging.error("LineRepository >> get_lines() >> No valid line_id found. / 有効な line_id が見つかりません。")
                return []

            # EN: Warn about invalid IDs
            # JP: 無効な ID について警告を表示
            invalid_ids = [lid for lid in line_id_list if lid not in valid_ids]
            if invalid_ids:
                logging.error(f"LineRepository >> get_lines() >> Invalid line_id(s) skipped: {invalid_ids} / 無効な line_id はスキップされました: {invalid_ids}")

            # EN: Step 2 - Fetch lines
            # JP: ステップ2 - ライン情報を取得
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            sql_lines = f"SELECT * FROM depal.line WHERE line_id IN ({','.join(['%s'] * len(valid_ids))})"
            cur.execute(sql_lines, list(valid_ids))
            result = cur.fetchall()

            for row in result:
                # EN: Create Line object
                # JP: Line オブジェクトを作成
                line = Line(row["line_id"], row["name"], row["process"])
                lines.append(line)

            # EN: Step 3 - Fetch frontages for each line
            # JP: ステップ3 - 各ラインのフロンテージを取得
            for line in lines:
                sql_frontage = "SELECT * FROM depal.line_frontage WHERE line_id = %s"
                cur.execute(sql_frontage, (line.id,))
                frontages_result = cur.fetchall()

                for row in frontages_result:
                    # EN: Create LineFrontage object and register to line
                    # JP: LineFrontage オブジェクトを作成し、ラインに登録
                    frontage_obj = LineFrontage(row["cell_code"], row["name"], row["frontage_id"], row["car_model_id"])
                    line.register_frontage(frontage_obj)

                # EN: Step 4 - Fetch inventories for each frontage
                # JP: ステップ4 - 各フロンテージの在庫情報を取得
                for frontage in line.frontages.values():
                    sql_inventory = """
                        SELECT * FROM depal.line_inventory
                        INNER JOIN depal.m_product USING(part_number)
                        WHERE depal.line_inventory.frontage_id = %s
                    """
                    cur.execute(sql_inventory, (frontage.id,))
                    inv_result = cur.fetchall()

                    inventories = []
                    for row in inv_result:
                        # EN: Create Part and Inventory objects
                        # JP: Part と Inventory オブジェクトを作成
                        part = Part(row["part_number"], row["kanban_no"], row["supplier_name"], row["car_model_id"])
                        inventory = Inventory(row["inventory_id"], part, row["case_quantity"])
                        inventories.append(inventory)

                    frontage.set_inventories(inventories)

        except Exception as e:
            logging.error(f"LineRepository >> get_lines() >> エラー]: {e}")

        finally:
            # EN: Close cursor and connection
            # JP: カーソルと接続を閉じる
            if cur:
                cur.close()
            if conn:
                conn.close()

        return lines
    
    def validate_inventory_ids(self, inventory_id_list: list) -> set[int]:
        """
        EN: Validate that the given inventory_id_list exists in depal.line_inventory table.
        JP: 指定された inventory_id_list が depal.line_inventory テーブルに存在するか確認します。
        Returns a set of valid inventory IDs.
        JP: 有効な inventory_id のセットを返します。
        """
        conn = None
        cur = None
        valid_ids = set()

        try:
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            # EN: If no IDs provided, return empty set
            # JP: ID が指定されていない場合、空のセットを返す
            if not inventory_id_list:
                logging.error(f"LineRepository >> validate_inventory_ids() >> No valid inventory_id_list found")
                return valid_ids

            # EN: Check if line_id exists in depal.line
            # JP: depal.line テーブルで line_id が存在するか確認
            sql = f"SELECT inventory_id FROM depal.line_inventory WHERE line_id IN ({','.join(['%s'] * len(inventory_id_list))})"
            cur.execute(sql, inventory_id_list)
            rows = cur.fetchall()
            valid_ids = {row["inventory_id"] for row in rows}

        except Exception as e:
            logging.error(f"[LineRepository >> validate_inventory_ids() >> Validation エラー] : {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

        return valid_ids

    def supply_parts(self, flow_rack:FlowRack):

        if flow_rack.is_empty():
            logging.error(f"[LineRepository >> supply_parts() >> FlowRack is empty]")
            raise Exception("FlowRack is empty")
        
        values = []
        for inventory in flow_rack.rack:
            if inventory is None or inventory.is_empty():
                continue
            values.append([inventory.id, inventory.case_quantity])

        try:
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor()
            sql = "INSERT INTO depal.parts_supply (inventory_id,case_quantity) VALUES (%s,%s);"
            cur.executemany(sql, values)
            conn.commit()

        except Exception as e:
            logging.error(f"[LineRepository >> supply_parts() >> エラー]: {e}")
        
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        

if __name__ == "__main__":
    
    repo = LineRepository()
    lines = repo.get_lines((1,2))
    for line in lines: 
        print(line.name)
        for f in line.frontages.values():
            print(f.id)
            for i in f.inventories:
                print(i)
    
    # flow_rack = FlowRack(1)
    # inventory = Inventory(1, Part(1, "A", "partA"), 5)
    # flow_rack.set_inventories([inventory])
    # repo.supply_line_area(flow_rack)


