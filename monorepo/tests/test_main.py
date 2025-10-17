# 修正前: from monorepo import main
# monorepo パッケージ直下ではなく、monorepo.main モジュールからインポートする
# 必要があります。

# 修正後: main.py モジュールから main 関数と get_demo 関数をインポート
# 実行時の PYTHONPATH=. が効いているので、絶対インポート形式を使います。

import monorepo.main as main


# mypyのエラー: Function is missing a return type annotation
# テスト関数は通常何も返さないため、-> None を追加します。
def test_main_demo() -> None:
    # main.py の get_demo 関数を直接呼び出します
    # get_demo() は yamlから取得した値を返すため、その値が 10 であることを想定
    assert main.get_demo() == 10
