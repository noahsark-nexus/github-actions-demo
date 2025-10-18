from typing import Any  # yamlの戻り値の型としてAnyを使用

from .utils import demo


# 戻り値の型ヒントを追加: 文字列またはAny (yamlの内容に依存)
def get_demo() -> Any:
    # utils.demo モジュール全体が型付けされている前提であれば、
    # demo.get_yaml() の戻り値の型をそのまま返します。
    # 現在はAnyが戻り値なのでAnyとします。
    return demo.get_yaml()

def main() -> None:
    """エントリポイント関数"""
    print(f"YAML content: {get_demo()}")

if __name__ == "__main__":
    main()
