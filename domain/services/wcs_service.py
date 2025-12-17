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
    
    def dispallet(self, depallet_area):
       try:
           if depallet_area is None:
               raise Exception("WCSService >> Depallet Area is None")
           self.wcs_repo.dispallet(depallet_area)
           logging.info("[WCSService >> dispallet() >> 成功]")
       except Exception as e:
           raise Exception(f"WCSService >> Error Dispallet: {e}")


       
