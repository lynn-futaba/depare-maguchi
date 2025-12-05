import os
import logging
from logging import Formatter, basicConfig, INFO
from logging.handlers import RotatingFileHandler

class LoggerSetup:
    # ログレベルの設定
    LOG_LEVEL = INFO    
    ENCODING = "utf-8"

    def __init__(self, folder_name: str, file_name: str, backup_day: int, max_bytes: int = 5 * 1024 * 1024):
        """
        ログ出力の準備を行うクラス

        :param folder_name: ログフォルダ名
        :param file_name: ログファイル名
        :param backup_day: 保持するファイル日数
        :param max_bytes: 最大ファイルサイズ（バイト）
        """
        self.folder_name = folder_name
        self.file_name = file_name
        self.backup_day = backup_day
        self.max_bytes = max_bytes

    def setup_log(self):
        """
        ログ出力の行う準備を行う関数

        :param folder_name: ログフォルダ名
        :param file_name: ログファイル名
        :param backup_day: 保持するファイル日数
        :param max_bytes: 最大ファイルサイズ（バイト）
        """

        path = os.path.dirname(__file__)
        folder_path = f"{path}/{self.folder_name}"

        # ログフォルダが無ければ作る
        os.makedirs(folder_path, exist_ok=True)

        file_fullpath = f"{folder_path}/{self.file_name}"

        # サイズローテーションを行うハンドラーを設定
        file_handler = RotatingFileHandler(
            file_fullpath, maxBytes=self.max_bytes,
            backupCount=self.backup_day,
            encoding=self.ENCODING
        )

        # ログ出力フォーマットを設定
        file_handler.setFormatter(
            Formatter(
                "%(asctime)s.%(msecs)03d,%(levelname)-5s,%(module)s,%(lineno)04d,%(message)s",
                datefmt="%Y/%m/%d %H:%M:%S",
            )
        )

        # ルートロガーの設定
        basicConfig(level=self.LOG_LEVEL, handlers=[file_handler])

        # 既存のすべてのハンドラーを削除して、コンソール出力を無効化
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                root_logger.removeHandler(handler)