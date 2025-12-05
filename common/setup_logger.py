import os
import logging
from logging import Formatter, INFO
from logging.handlers import RotatingFileHandler


# ログレベルの設定
LOG_LEVEL = INFO
ENCODING = "utf-8"

def setup_log(folder_name: str, file_name: str, backup_day: int, max_bytes: int = 10 * 1024 * 1024):
    """
    ログ出力の行う準備を行う関数

    :param folder_name: ログフォルダ名
    :param file_name: ログファイル名
    :param backup_day: 保持するファイル日数
    :param max_bytes: 最大ファイルサイズ（バイト）
    """
    # ログフォルダのパスを作成
    path = os.path.dirname(__file__)
    folder_path = os.path.join(path, folder_name)

    # ログフォルダが無ければ作成
    os.makedirs(folder_path, exist_ok=True)

    # ログファイルのフルパス
    file_fullpath = os.path.join(folder_path, file_name)

    # サイズローテーションを行うハンドラーを設定
    file_handler = RotatingFileHandler(
        file_fullpath, maxBytes=max_bytes, backupCount=backup_day, encoding="utf-8"
    )

    # ログ出力フォーマットを設定
    file_handler.setFormatter(
        Formatter(
            "%(asctime)s.%(msecs)03d,%(levelname)-5s,%(module)s,%(lineno)04d,%(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
    )

    # ルートロガーの設定
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # ログレベルを設定
    file_handler.setLevel(logging.DEBUG)
    # console_handler.setLevel(logging.DEBUG)
    
    # 既存のハンドラを削除
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 新しいハンドラを追加
    logger.addHandler(file_handler)  # ファイル出力用のハンドラを追加
    # logger.addHandler(logging.StreamHandler())  # コンソール出力用のハンドラを追加
