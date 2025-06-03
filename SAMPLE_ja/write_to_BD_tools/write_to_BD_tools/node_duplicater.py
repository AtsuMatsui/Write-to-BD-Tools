"""ノードを複製し、Backdropに表示されているWriteノード名（Write_to_BD1）の数を１増やす

機能一覧:
    - ノードを複製
    - Backdropに表示されているWriteノード名（Write_to_BD1）の末尾番号を1増やす
    - 複製したノードの位置をずらす
    - ノードの接続を解除

関数:
    get_current_number(base_name): Writeノードの最大値を取得
    duplicate_nodes(node_names): 指定されたノードを選択し、複製
    apply_position_offset(nodes, x_offset, y_offset): x軸とy軸の値を変更
    update_backdrop_label(duplicated_backdrop, original_write): Backdropの表示を更新
    disconnect_nodes(nodes): 複数のノードの接続を解除
    disconnect_node(node): 各ノードの接続を解除

Copyright (c) 2025 Atsu Matsui
"""

# 外部ライブラリをインポート
import nuke

# モジュールをインポート
from log_setup import write_to_bd_log

def get_current_number(base_name):
    """Writeノードの最大値を取得

    引数:
        base_name (str): Writeノード名を検索

    戻り値:
        int: Writeノードの最大値を返す、存在しない場合は0を返す
    """

    write_nodes = [node for node in nuke.allNodes("Write")
                   if base_name in node.name()]
    current_number = 0
    for node in write_nodes:
        number_str = node.name().split("_")[-1][2:]
        if number_str.isdigit():
            number = int(number_str)
            current_number = max(current_number, number)

    return current_number

def duplicate_nodes(node_names):
    """指定されたノードを選択し、複製

    引数:
        node_names (list[str]): 複製するノード名のリスト

    戻り値:
        list[nuke.Node]: 複製したノードのリスト、エラーが発生した場合は空のリスト

    例外:
        ValueError: 指定されたノードがNukeスクリプトに存在しない場合
    """

    # エラーをログファイルに記録
    catch_errors = write_to_bd_log.log_errors

    # ノードが存在することを確認
    original_nodes = [nuke.toNode(node_name) for node_name in node_names]
    missing = [name for name, node in zip(node_names, original_nodes) if node is None]

    if missing:
        error_message = f"Node \"{', '.join(missing)}\" not found"
        catch_errors(ValueError, error_message)

    # すべてのノードの選択を解除
    for node in nuke.allNodes():
        node["selected"].setValue(False)

    # 複製するノードを選択
    for node in original_nodes:
        node["selected"].setValue(True)

    # ノードを複製
    nuke.nodeCopy("%clipboard%")
    nuke.nodePaste("%clipboard%")

    duplicated_nodes = nuke.selectedNodes()
    return duplicated_nodes

def apply_position_offset(nodes, x_offset, y_offset):
    """指定されたノードのX軸、Y軸を調整

    引数:
        nodes (list[nuke.Node]): 調整するノードのリスト
        x_offset (int): X軸の値
        y_offset (int): Y軸の値
    """

    for node in nodes:
        new_xpos = node["xpos"].value() + x_offset
        new_ypos = node["ypos"].value() + y_offset

        node["xpos"].setValue(new_xpos)
        node["ypos"].setValue(new_ypos)

def update_backdrop_label(duplicated_backdrop, original_write):
    """Backdropの表示を更新

    例: "Write_to_BD1" を "Write_to_BD2"のように末尾番号を1増やして更新

    引数:
        duplicated_backdrop (nuke.Node): 複製したBackdropノード
        original_write (str): 複製前のWriteノード名

    例外:
        KeyError: Backdropにlabelノブが存在しない場合
    """

    current_number = get_current_number("Write_to_BD")
    next_number = current_number

    # エラーをログファイルに記録
    catch_errors = write_to_bd_log.log_errors

    if "label" not in duplicated_backdrop.knobs():
        error_message = "The \"label\" knob is missing in the BackdropNode."
        catch_errors(KeyError,error_message)

    current_label = duplicated_backdrop["label"].value()
    new_label = current_label.replace(original_write, f"Write_to_BD{next_number}")
    duplicated_backdrop["label"].setValue(new_label)

def disconnect_nodes(nodes):
    """複数のノードの接続を解除

    引数:
        nodes (list[nuke.Node]): 接続を解除したい複数のノード
    """

    for node in nodes:
        disconnect_node(node)

def disconnect_node(node):
    """各ノードの接続を解除

    引数:
        node (nuke.Node): 接続を解除するノード
    """

    for i in range(node.inputs()):
        node.setInput(i, None)

    for dep_node in node.dependent():
        for i in range(dep_node.inputs()):
            if dep_node.input(i) == node:
                dep_node.setInput(i, None)
