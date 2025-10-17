from importlib import resources
from typing import Any, cast

import yaml

# 外部ライブラリの型スタブがないことによるエラーを避けるため、
# yamlの戻り値をAnyとして扱う
YAML_RETURN_TYPE = dict[str, Any]


# 戻り値の型ヒントを追加: yaml.safe_loadの戻り値はAnyを返す辞書構造を想定
def load_yaml(filename: str) -> YAML_RETURN_TYPE:
    """
    データディレクトリから指定されたYAMLファイルを読み込む。
    """
    # resources.files() は Python 3.9+ で推奨
    config_path = resources.files("monorepo") / "data" / filename
    config_path = resources.files("monorepo") / "data" / filename
    with config_path.open("r", encoding="utf-8") as f:  # <- ここを修正
        result = yaml.safe_load(f)
        return cast(YAML_RETURN_TYPE, result)


# 戻り値の型ヒントを追加
def get_yaml() -> Any:
    """
    デモYAMLを読み込み、特定キーの値 (demo) を返す。
    """
    # load_yaml の戻り値が YAML_RETURN_TYPE と型付けされているため、
    # 辞書としてアクセスしても mypy はエラーを出しません。
    demo_yaml = load_yaml("demo.yaml")
    # キーアクセスは Any になるため、厳密には戻り値も Any になります。
    return demo_yaml["demo"]
