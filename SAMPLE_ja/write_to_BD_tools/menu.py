"""ノードメニューにカスタムノードを追加し、ノードを読み込む

属性:
    icon_directory (str): アイコンが格納されているパスを指定
    nuke_file_directory (str): Nukeスクリプトがあるパスを指定

実行する処理:
    - "Write to BD with TCL": Nukeスクリプトからノードを読み込む

Copyright (c) 2025 Atsu Matsui
"""

# 標準ライブラリをインポート
import os

# 外部ライブラリをインポート
import nuke

# Nukeスクリプトとアイコンのあるフォルダを読み込む
nuke.pluginAddPath("./icons")
nuke.pluginAddPath("./nk_files")

# Nukeスクリプトとアイコンが格納されているパスを指定
icon_directory = os.path.join(os.path.dirname(__file__), "icons")
nuke_file_directory = os.path.join(os.path.dirname(__file__), "nk_files")

# ツールバーにツールを追加
write_to_bd_menu = nuke.menu("Nodes").addMenu(
    "Write to BD tools",
    icon = os.path.join(icon_directory, "WBD_icon_v01.png")
)

write_to_bd_menu.addCommand(
    "Write to BD with TCL",
    "nuke.nodePaste(os.path.join(nuke_file_directory, \"Write_to_BD_TCL.nk\"))",
    icon=""
)
