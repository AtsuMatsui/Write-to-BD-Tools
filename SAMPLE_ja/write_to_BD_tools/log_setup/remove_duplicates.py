"""重複したログメッセージをすべて削除

ログメッセージが繰り返し出力されるのを防ぎ、重要な情報のみ残す

Copyright (c) 2025 Atsu Matsui
"""

# 標準ライブラリをインポート
import logging

class DuplicateFilter(logging.Filter):
    """重複したログメッセージを削除するフィルター

    属性:
        last_log (tuple): 最後に記録された (モジュール名, レベル, メッセージ) を保持
    """

    last_log = None

    def filter(self, record):
        """最後のログメッセージと異なる場合のみ記録する

        引数:
            record (logging.LogRecord): 確認する対象のログ情報

        戻り値:
            bool: メッセージが異なる場合は記録する、それ以外は記録しない
        """

        current_log = (record.module, record.levelno, record.msg)

        if current_log != DuplicateFilter.last_log:
            DuplicateFilter.last_log = current_log  # 最後のログメッセージを更新
            return True
        return False
