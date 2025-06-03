"""JSON形式のロギング設定

特徴:
    - タイムスタンプ、ログレベル、ファイル名、行番号、メッセージを含んだログを出力
    - ログ管理システムと連携できるようにJSON形式で出力

Copyright (c) 2025 Atsu Matsui
"""

# 標準ライブラリをインポート
import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """ログをJSON形式で出力するためのカスタム設定"""

    def __init__(self):
        """インスタンスを初期化し、ログをJSON形式で出力"""

        super().__init__()

    def format(self, record):
        """ログの内容をJSON文字列として整形

        引数:
            record (logging.LogRecord): ログ情報をまとめたデータ

        戻り値:
            str: JSON文字列を返す
        """

        log_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "location": f"{record.filename}:L{record.lineno}",
            "message": record.getMessage()
        }
        return json.dumps(log_record, ensure_ascii=False)
