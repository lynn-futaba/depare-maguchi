from domain.infrastructure.wcs_repository import IWCSRepository

from common.setup_logger import setup_log  # ログ用
from config.config import BACKUP_DAYS  # ログ用

import logging

# ログ出力開始
LOG_FOLDER = "../log"
LOG_FILE = "debug_logging.log"
setup_log(LOG_FOLDER, LOG_FILE, BACKUP_DAYS)

class WCSService:

    def __init__(self, wcs_repo: IWCSRepository):
        self.wcs_repo = wcs_repo

    # update maguchi signal 1
    def insert_target_ids(self, button_id):
        try:
            logging.info("[WCSService >> insert_target_ids() >> 成功]")
            self.wcs_repo.insert_target_ids(button_id)
        except Exception as e:
            logging.error(f"[WCSService >> insert_target_ids() >> エラー]: {e}")
            raise Exception(f"[WCSService >> insert_target_ids >> エラー]: {e}")
        
    # update maguchi signal 2
    def call_target_ids(self, button_id):
        try:
            logging.info("[WCSService >> call_target_ids() >> 成功]")
            self.wcs_repo.call_target_ids(button_id)
        except Exception as e:
            logging.error(f"[WCSService >> call_target_ids() >> エラー]: {e}")
            raise Exception(f"[WCSService >> call_target_ids() >> エラー]: {e}")
    
    def dispallet(self, depallet_area):
       try:
           if depallet_area is None:
               raise Exception("WCS Service >> Depallet Area is None")
           self.wcs_repo.dispallet(depallet_area)
           logging.info("[WCS Service >> dispallet() >> 成功]")
       except Exception as e:
           raise Exception(f"WCS Service >> Error Dispallet: {e}")
       
    def get_empty_kotatsu_status(self):
       try:
           supplier_names = self.wcs_repo.get_empty_kotatsu_status()
           logging.info("[WCS Service >> get_empty_kotatsu_status() >> 成功]")
           return supplier_names
       except Exception as e:
           raise Exception(f"[WCS Service >> get_empty_kotatsu_status() >> エラー]: {e}")
       
    


       
