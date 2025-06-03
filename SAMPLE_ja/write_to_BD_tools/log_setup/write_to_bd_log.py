"""Write to BD toolsのログ設定

機能:
    - ローテーション形式でデバッグ用にエラーログを記録
    - Nuke のスクリプトエディタにログ情報を表示
    - 重複したログメッセージを防止

ログが適用されている箇所:
    - BackdropノードのPython Scriptボタンに適用

Copyright (c) 2025 Atsu Matsui
"""

# 標準ライブラリをインポート
import logging
from logging.handlers import TimedRotatingFileHandler
import os

# モジュールをインポート
from log_setup.json_formatter import JsonFormatter
from log_setup.remove_duplicates import DuplicateFilter

def create_log_directory():
    """ログのディレクトリが存在することを確認

    戻り値:
        str: ログファイルが保存されているディレクトリのパス
    """

    log_directory = os.path.join(os.path.dirname(__file__), "..", "logs")

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    return log_directory

def get_log_file_path():
    """ログファイルのパスを生成

    戻り値:
        str: ログファイルへのパス
    """

    this_log_directory = create_log_directory()
    log_file = "error.log"
    return os.path.join(this_log_directory, log_file)

def log_errors(error_type, message):
    """エラーメッセージをログに記録し、指定された例外のみ表示させる

    引数:
        error_type (Type[Exception]): 例外の種類
        message (str): 例外で出たメッセージをログに記録する

    例外:
        Exception: 指定された例外とメッセージを表示
    """

    logger = logging.getLogger("write_to_bd_logger")
    logger.error(message)
    raise error_type(message)

def create_file_handler():
    """ログファイルを出力し、時刻を作成

    戻り値:
        TimedRotatingFileHandler: JSON 形式で整形されたファイル
    """

    log_file_path = get_log_file_path()

    # ログファイルを7日分保持
    # PCで設定している時間を使用して、ローテーションを行う
    file_handler = TimedRotatingFileHandler(
        log_file_path,
        when="MIDNIGHT",
        interval=1,
        backupCount=7,
        encoding="utf-8",
        utc=False
    )

    # ログを JSON 形式で整形
    file_handler.setFormatter(JsonFormatter())

    # 重複ログを防止
    file_handler.addFilter(DuplicateFilter())

    # ログレベルを設定
    file_handler.setLevel(logging.ERROR)

    return file_handler

def create_console_handler():
    """Nukeのスクリプトエディタにログを表示

    戻り値:
        logging.StreamHandler: ログレベルとメッセージを表示
    """

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("[%(levelname)s] - %(message)s")
    )

    # ログレベルを設定
    console_handler.setLevel(logging.INFO)

    return console_handler

def get_logger():
    """設定したロガーを作成

    戻り値:
        logging.Logger: ファイルおよびコンソールハンドラ付きのロガーを返す
    """

    logger = logging.getLogger("write_to_bd_logger")

    # ログのディレクトリとファイルパスを確認
    create_log_directory()
    get_log_file_path()

    # ハンドラを追加
    logger.addHandler(create_file_handler())
    logger.addHandler(create_console_handler())

    # ロガーのログレベルを設定
    logger.setLevel(logging.DEBUG)

    return logger

# ロガーを設定
get_logger()
