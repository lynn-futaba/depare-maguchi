import os
import logging
from logging import Formatter, INFO
# 変更: RotatingFileHandler を TimedRotatingFileHandler に変更
from logging.handlers import TimedRotatingFileHandler


# ログレベルの設定
LOG_LEVEL = INFO
ENCODING = "utf-8"

def setup_log(folder_name: str, file_name: str, backup_day: int):
    """
    ログ出力の行う準備を行う関数 (日付ローテーション対応)

    :param folder_name: ログフォルダ名
    :param file_name: ログファイル名 (ベース名となり、日付が追記される)
    :param backup_day: 保持するファイルの世代数 (日数)
    """
    # ログフォルダのパスを作成
    path = os.path.dirname(__file__)
    folder_path = os.path.join(path, folder_name)

    # ログフォルダが無ければ作成
    os.makedirs(folder_path, exist_ok=True)

    # ログファイルのフルパス
    file_fullpath = os.path.join(folder_path, file_name)

    # 変更: サイズローテーションを TimedRotatingFileHandler (日付ローテーション) に変更
    # when='midnight' または when='D' (daily) は、毎日午前0時にローテーションを行います。
    file_handler = TimedRotatingFileHandler(
        file_fullpath, 
        when='midnight',             # 毎日午前0時にローテーション
        interval=1,                  # 1日ごとに実行
        backupCount=backup_day,      # 保持するファイルの世代数 (日数)
        encoding=ENCODING,           # エンコーディング
        atTime=None                  # 0時ちょうどにローテーション
    )

    # ログ出力フォーマットを設定 (日付フォーマットはそのまま)
    file_handler.setFormatter(
        Formatter(
            "%(asctime)s.%(msecs)03d,%(levelname)-5s,%(module)s,%(lineno)04d,%(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
    )

    # ルートロガーの設定
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG) 
    file_handler.setLevel(logging.DEBUG)
    
    # 既存のハンドラを削除 (Good practice)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 新しいハンドラを追加
    logger.addHandler(file_handler) 
    
    # ログローテーションの仕組みのイメージ