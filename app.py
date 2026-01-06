import os
import json
import time
import logging
import threading
import asyncio

from flask import Flask, render_template, request, jsonify, abort
from config.config_loader import AppConfig
from common.setup_logger import setup_log  # ログ用
from config.config import BACKUP_DAYS, LOG_FOLDER, LOG_FILE   # ログ用
from datetime import datetime
from application.depallet_app import DepalletApplication

# ログ出力開始
setup_log(LOG_FOLDER, LOG_FILE, BACKUP_DAYS)

CONFIG_PATH = "/app/config/app_config.json" if os.path.exists("/app/config/app_config.json") else "config/app_config.json"

class DepalletWebServer:
    def __init__(self, depallet_app):
        self._depallet_app = depallet_app
        self.app = Flask(__name__, static_folder='static')
        self.setup_routes()
        self.server_thread = None
        self.app.secret_key = 'secret_key'
        self.config_loader = AppConfig()

    def start(self, host='0.0.0.0', port=5000):

            if self.server_thread is not None and self.server_thread.is_alive():
                logging.info("Web server is already running")
                return self

            def run_server():
                self.app.run(host=host, port=port, debug=False, threaded=True, use_reloader=False)

            self.server_thread = threading.Thread(target=run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            logging.info(f"Web server started at http://{host}:{port}")
            return self
    
    

    def setup_routes(self):
        """ルート設定"""
        app = self.app
        
        @app.route("/", methods=["GET"])
        def index():
            return render_template('index.html')
        
        @app.route("/ui/b_line/maguchi_r1", methods=["GET"])
        def ui_b_line_maguchi_r1():
            return render_template('b-line-maguchi-r1.html')
        
        @app.route("/ui/b_line/maguchi_r2", methods=["GET"])
        def ui_b_line_maguchi_r2():
            return render_template('b-line-maguchi-r2.html')
        
        @app.route("/api/get_b_ui_config", methods=["GET"])
        def get_b_ui_config():
            # Use a try-except block so that even if this fails, 
            # the rest of the server stays alive.
            try:
                data = self.config_loader.data
                return jsonify({
                    "buttonIdMap": data.get("b_button_id_map", {}),
                    "shelfMap": data.get("b_shelf_map", {})
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            
        @app.route("/api/get_a_ui_config", methods=["GET"])
        def get_a_ui_config():
            # Use a try-except block so that even if this fails, 
            # the rest of the server stays alive.
            try:
                data = self.config_loader.data
                return jsonify({
                    "buttonIdMap": data.get("a_button_id_map", {}),
                    "shelfMap": data.get("a_shelf_map", {})
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # @app.route("/return_index")
        # def returns():
        #     return render_template('index.html')

        # @app.route("/maguchi")
        # def maguchi_page():
        #     return render_template('depallet/maguchi.html')

        # @app.route("/flow_rack")
        # def flow_rack_page():
        #     return render_template('depallet/flowrack.html') 

        @app.route("/b_line_depallet_maguchi", methods=["GET"])
        def b_line_depallet_maguchi():
            try:
                id_value = request.args.get("id")
                name_value = request.args.get("name")
                logging.info("[app.py >> b_line_depallet_maguchi() >> 成功]")
                return render_template('b-line-depallet-maguchi.html', id=id_value, name=name_value)
            except Exception as e:
                logging.info(f"[app.py >> b_line_depallet_maguchi() >> エラー] : {e}")
                return abort(400, 'Invalid request')

        @app.route("/a_line_depallet_maguchi", methods=["GET"])
        def a_line_depallet_maguchi():
            try:
                id_value = request.args.get("id")
                name_value = request.args.get("name")
                logging.info("[app.py >> a_line_depallet_maguchi() >> 成功]")
                return render_template('a-line-depallet-maguchi.html', id = id_value, name = name_value)
            except Exception as e:
                logging.info(f"[app.py >> a_line_depallet_maguchi() >> エラー] : {e}")
                return abort(400, 'Invalid request')

        @app.route("/api/get_product_infos", methods=["GET"])
        def get_product_infos():
            try:
                self._depallet_app.update_line_data()
                a_product_r, a_product_l, b_product_r, b_product_l = self._depallet_app.get_product_infos_json() # TODO➞リン: l,r to product_r, product_l
                line_area_json = self._depallet_app.get_lines_json()
                return [a_product_r, a_product_l, b_product_r, b_product_l, line_area_json] # TODO➞リン: l,r to product_r, product_l
            except Exception as e:
                return str(e), 500

        @app.route("/api/insert_kanban_nuki", methods=["GET"])
        def insert_kanban_nuki():
            try:
                logging.info("[app.py >> insert_kanban_nuki() >> 成功]")
                self._depallet_app.insert_kanban_nuki()
                return jsonify({"status": "success"})
            except Exception as e:
                logging.info(f"[app.py >> insert_kanban_nuki() >> エラー] : {e}")
                return abort(400, str(e))

        @app.route("/api/insert_kanban_sashi", methods=["GET"])
        def insert_kanban_sashi():
            try:
                logging.info("[app.py >> insert_kanban_sashi() >> 成功]")
                self._depallet_app.insert_kanban_sashi()
                return jsonify({"status": "success"})
            except Exception as e:
                logging.info(f"[app.py >> insert_kanban_sashi() >> エラー] : {e}")
                return abort(400, str(e))
            
        @app.route("/api/insert_kanban_yobi_dashi", methods=["GET"])
        def insert_kanban_yobi_dashi():
            try:
                logging.info("[app.py >> insert_kanban_yobi_dashi() >> 成功]")
                self._depallet_app.insert_kanban_yobi_dashi()
                return jsonify({"status": "success"})
            except Exception as e:
                logging.info(f"[app.py >> insert_kanban_yobi_dashi() >> エラー] : {e}")
                return abort(400, str(e))

        @app.route("/api/line_frontage_click", methods=["POST"])
        def line_frontage_click():
            # クリックしたら部品とフローラックを呼ぶ
            id = request.json.get('frontage_id')
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_in_executor(None, self._depallet_app.depallet_start, id)
                return jsonify({"status": "success"})

            except Exception as e:
                logging.error(f"{e}")
                return abort(400, 'Invalid request')

        @app.route("/api/insert_target_ids", methods=["POST"])
        def insert_target_ids():
            try:
                button_id = request.json.get('button_id')
                logging.info("[app.py >> [insert_target_ids() >> 成功]")
                self._depallet_app.insert_target_ids(button_id)
                return jsonify({"status": "success"})
            except Exception as e:
                logging.error(f"[app.py >> insert_target_ids() >> エラー] : {e}")
                return abort(400, str(e))

        @app.route("/api/call_target_ids", methods=["POST"])
        def call_target_ids():
            try:
                button_id = request.json.get('button_id')
                logging.info("[app.py >> call_target_ids() >> 成功]")
                self._depallet_app.call_target_ids(button_id)
                return jsonify({"status": "success"})
            except Exception as e:
                logging.error(f"[app.py >> call_target_ids() >> エラー] : {e}")
                return abort(400, str(e))

        @app.route("/api/get_depallet_area")  # TODO➞リン: changed 
        def get_depallet_area():
            try:
                depallet_area = self._depallet_app.get_depallet_area_json()
                logging.info(f"[app.py >> get_depallet_area_by_plat() >> depallet_area] : {depallet_area}")
                return jsonify(depallet_area)
            except Exception as e:
                logging.error(f"[app.py >> get_depallet_area() >> エラー] : {e}")
                return abort(400, str(e))

        @app.route("/api/update_flow_rack")
        def update_flow_rack():
            try:
                flow_rack = self._depallet_app.get_flow_rack_json()
                return jsonify(flow_rack)
            except Exception as e:
                return abort(400, str(e))

        @app.route("/api/to_flow_rack", methods=["POST"])
        def to_flow_rack():
            try:
                frontage_id = request.json.get('frontage_id')
                part_id = request.json.get('part_id')
                self._depallet_app.fetch_part(int(frontage_id), str(part_id))
                # self._depallet_app.fetch_part(int(frontage_id), int(part_id))  # TODO➞リン: testing
                return jsonify({"status": "success"})
            except Exception as e:
                return abort(400, str(e))

        @app.route("/api/to_kotatsu", methods=["POST"])
        def to_kotatsu():
            try:
                frontage_id = request.json.get('frontage_id')
                part_id = request.json.get('part_id')
                self._depallet_app.return_part(int(frontage_id), str(part_id))
                # self._depallet_app.return_part(int(frontage_id), int(part_id)) # TODO➞リン: modified
                return jsonify({"status": "success"})
            except Exception as e:
                return abort(400, str(e))

        @app.route("/api/return_kotatsu", methods=["POST"])
        def return_kotatsu():
            try:
                frontage = request.json.get('frontage_id')
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_in_executor(
                   None, self._depallet_app.return_kotatsu, int(frontage))

                return jsonify({"status": "success"})
            except Exception as e:
                return abort(400, str(e))

        @app.route("/api/complete", methods=["POST"])
        def complete():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_in_executor(None, self._depallet_app.complete)
                return jsonify({"status": "success"})
            except Exception as e:
                return abort(400, str(e))

        @app.route("/api/get_depallet_area_by_plat", methods=["POST"])  # TODO➞リン: added 
        def get_depallet_area_by_plat():
            try:
                # button_id = request.json.get("button_id")
                fetch_depallet_area = self._depallet_app.get_depallet_area_by_plat_json()
                logging.info(f"[app.py >> get_depallet_area_by_plat() >> fetch_depallet_area] : {fetch_depallet_area}")
                return fetch_depallet_area
            except Exception as e:
                logging.error(f"[app.py >> get_depallet_area_by_plat() >> エラー]: {e}")
                return abort(400, str(e))


        # 取出数量 更新
        file_lock = threading.Lock()
        
        @app.route('/api/update_take_count', methods=['POST'])
        def update_take_count():
            kanban_no = str(request.json.get('kanban_no'))
            new_take_count = str(request.json.get('new_take_count'))

            response = {}

            try:
                # Basic validation
                if not kanban_no or new_take_count is None:
                    response = jsonify({"status": "error", "message": "kanban_no and new_take_count are required"}), 400
                    return response

                with file_lock:
                    # Load current config
                    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                        config = json.load(f)

                    # Ensure the "take_count" section exists
                    take_count = config.get("take_count")
                    if not isinstance(take_count, dict):
                        response = jsonify({"status": "error", "message": "'take_count' section missing in app_config.json"}), 500
                        return response

                    # Check if the kanban exists; if you want to allow new keys, remove this check
                    if kanban_no not in take_count:
                        response = jsonify({
                            "status": "error",
                            "message": f"背番号 '{kanban_no}' が app_config.jsonの中で有りません"
                        }), 404 
                        return response

                    # Update nested value
                    take_count[kanban_no] = new_take_count
                    config["take_count"] = take_count  # (not strictly necessary but explicit)

                    # Atomic save: write to temp then replace
                    tmp_path = CONFIG_PATH + ".tmp"
                    with open(tmp_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, ensure_ascii=False, indent=2)
                    os.replace(tmp_path, CONFIG_PATH)

                    # ✅ Refresh one time
                    get_depallet_area_by_plat()

                    response = jsonify({"status": "success", "message": f"背番号 '{kanban_no}' を '{new_take_count}' に更新しました。", "updated": {kanban_no: new_take_count}})
                    return response
                
            except Exception as e:
                logging.error(f"[app.py >> update_take_count() >> ERROR] : {e}", exc_info=True)
                response = jsonify({"status": "error", "message": str(e)}), 500
                return response

        @app.route("/api/call_AMR_return", methods=["POST"])
        def call_AMR_return():
            try:
                # ✅ Refresh one time
                get_depallet_area_by_plat()
                button_id = request.json.get('button_id') 
                self._depallet_app.call_AMR_return(button_id) 
                logging.info(f"[app.py >> call_AMR_return() >> success]")
                return jsonify({"status": "success", "message": "call AMR return successfully"})
            except Exception as e:
                logging.error(f"[app.py >> call_AMR_return() >> エラー] : {e}")
                return abort(400, str(e))
            
        
        @app.route("/api/call_AMR_flowrack_only", methods=["POST"])
        def call_AMR_flowrack_only():
            try:
                button_id = request.json.get('button_id') 
                self._depallet_app.call_AMR_flowrack_only(button_id) 
                logging.info(f"[app.py >> call_AMR_flowrack_only() >> success]")
                return jsonify({"status": "success", "message": "call AMR flowrack only return successfully"})
            except Exception as e:
                logging.error(f"[app.py >> call_AMR_flowrack_only() >> エラー] : {e}")
                return abort(400, str(e))
            
        @app.route("/api/get_empty_kotatsu_status", methods=["GET"])
        def get_empty_kotatsu_status():
            try:
                # 1. Call the application layer (ensure the middle layers also 'return' the result!)
                supplier_list = self._depallet_app.get_empty_kotatsu_status()
                
                # 2. Check if the list has content
                if supplier_list and len(supplier_list) > 0:
                    logging.info(f"[app.py >> get_empty_kotatsu_status() >> 成功] Found: {supplier_list}")
                    return jsonify({
                        "status": "success", 
                        "suppliers": supplier_list,
                        "message": f"{len(supplier_list)}件の空き仕入先が見つかりました。"
                    }), 200
                else:
                    return jsonify({
                        "status": "empty", 
                        "suppliers": [],
                        "message": "現在、対象の空き棚はありません。"
                    }), 200

            except Exception as e:
                logging.error(f"[app.py >> get_empty_kotatsu_status() >> エラー] : {e}")
                # Return 400 or 500 error for AJAX 'error' block to catch
                return jsonify({"status": "error", "message": str(e)}), 400
        
if __name__ == "__main__":
    depallet_app = None # TODO➞リン
    try:
        depallet_app = DepalletApplication()
        logging.info(f"[app.py >> DepalletApplication >> __main__] : {depallet_app}")
        depallet_app.start()
        web_server = DepalletWebServer(depallet_app)
        web_server.start(host='0.0.0.0', port=5000)
        while True:
            time.sleep(1)

    except KeyboardInterrupt as e:
        logging.error(f"app.py >> Shutting down...:{e}")
    finally:
        if depallet_app:
            depallet_app.stop()

