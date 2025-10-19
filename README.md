# 🐍 Pythonの環境構築チートシート

## 🐍 Miniconda

ライブラリ（パッケージ）の依存関係と、プロジェクトごとの実行環境を管理するための非常に便利なツール

| コマンド | 解説 |
| ---- | ---- |
| `conda env list` | 環境の一覧を表示す |
| `conda create -n myenv python=3.10 -y` | `myenv`という名前で、Python 3.10の環境を作成する |
| `conda activate myenv` | 作成した環境に入る |
| `conda deactivate` | 現在の環境から出る| 
| `conda env remove -n myenv -y` | 環境を削除する |
| `conda create -n newenv --clone myenv` | 環境を複製する |

---

## 📦 Poetry

`pip` ではサブ依存関係のバージョンが固定されず、時間が立つにつれて依存ライブラリが更新され動かなくなるので、プロジェクトが誕生した瞬間の依存関係の完全なスナップショットを保持するツール


### 初期設定

Conda環境でPoetryを使う場合、Poetryが独自の仮想環境を作らないように設定します。

| コマンド | 解説 |
| ---- | ---- |
| `conda activate <あなたの環境名>` | 使用するConda環境をアクティベートする。 |
| `pip install poetry` | そのConda環境の中にPoetryをインストールする。 |
| `poetry config virtualenvs.create false` | Poetryが独自の仮想環境を作る機能を無効化し、アクティブなConda環境を使うように指示する。 |
| `poetry config --list` | 全てのグローバル設定を表示 |

`poetry config` はグローバル設定ファイルに保存されるので、ユーザーアカウント全体に適応されるので１度設定すれば永続的に適応される。

### よく使うコマンド

| コマンド | 解説 |
| ---- | ---- |
| `poetry init` | `pyproject.toml` ファイルを作成する。プロジェクト名、バージョン、ライセンスなどを対話形式で設定する。 |
| `poetry show` | インストールされているパッケージとバージョンをすべて表示 |
| `poetry add <パッケージ名>` | 実行時に必要なコアなライブラリ（例: `numpy`, `pandas`）を追加する。 |
| `poetry add pytest mypy ruff --group dev` | `pytest`, `mypy`, `ruff` などの開発・テスト用ツールを **`dev` グループ**として追加する。 |
| `poetry add <パッケージ名> -C <ディレクトリ名>` | **`-C`** オプションで、追加対象のサブプロジェクトの `pyproject.toml` を指定します。 |
| `poetry remove <パッケージ名>` | ライブラリを削除 |
| `poetry update` | 全てのパッケージを更新 |
| `poetry lock` | `poetry install` したら ‘pyproject.toml changed’ の警告が出る」場合、 `pyproject.toml` に合致させた最新の `poetry.lock` を生成または更新する。 |
| `poetry install` | `poetry.lock` に基づいて、全依存関係（`dev` 含む）をインストールする。 |
| `poetry install --without dev` | 実行時依存関係のみをインストールする（CIでのデプロイステップなどで使う）。 |
| `poetry run python main.py` | コマンドの前に `poetry run` を付けて、Poetryが管理する環境で実行する。 |

### ポリレポ開発でのパッケージ管理

**pyproject.toml**
```toml
[tool.poetry]
name = "demo"
version = "0.1.0"
packages = [{ include = "demo", from = "src" }]

[tool.poetry.dependencies]
python = ">=3.10"

[tool.poetry.group.dev.dependencies]
pytest = ">=8.4.2,<9.0.0"
mypy = ">=1.18.2,<2.0.0"
ruff = ">=0.14.1,<0.15.0"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

**src/demo/main.py**

```python
def get_demo():
    return 30

if __name__ == "__main__":
    print(f"Demo content: {get_demo()}")
```

**実行**

```bash
poetry lock
poetry install
poetry show # packages = [{ include = "demo", from = "src" }] が追加されてる確認
poetry run python -m demo.main
```

### モノレポ開発でのパッケージ管理

**pyproject.toml**

```toml
[tool.poetry]
name = "github-actions-demo"
version = "0.1.0"
# パッケージモードを明示的に無効化
package-mode = false

[tool.poetry.dependencies]
python = ">=3.10"
monorepo = { path = "monorepo", develop = true }

[tool.poetry.group.dev.dependencies]
pytest = ">=8.4.2,<9.0.0"
mypy = ">=1.18.2,<2.0.0"
ruff = ">=0.14.1,<0.15.0"
types-pyyaml = "^6.0.12.20250915"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

`package-mode` を `false` にして、 `[tool.poetry.dependencies]` に `monorepo = { path = "monorepo", develop = true }` を記述すると `pip install -e monorepo` と同じ編集可能パッケージになる。


**monorepo/pyproject.toml**

```toml
# monorepo/pyproject.toml
[tool.poetry]
name = "monorepo" # パッケージ名
version = "0.1.0"
# 「monorepo」パッケージをインクルードし、そのソースは「src」ディレクトリ内にあることを指定
packages = [{ include = "monorepo", from = "src" }] 

[tool.poetry.dependencies]
python = ">=3.10"
pyyaml = "^6.0.3"
```

**実行**

```bash
poetry lock
poetry install
poetry show # packages = [{ include = "demo", from = "src" }] が追加されてる確認
poetry run python -m monorepo.main
poetry run ruff check . 
poetry run mypy .
poetry run pytest
```

---

## 🧹 Ruff

ruffは「リンティング（構文やスタイルのチェック）」と「フォーマット（自動整形）」の2つの機能があります。

| コマンド | 解説 |
| ---- | ---- |
| `poetry run ruff check .` | スタイル違反や潜在的なバグを指摘する（ファイルは変更しない）。これをCIで使います。 |
| `poetry run ruff check . --fix` | 指摘されたエラーのうち、安全に自動修正できるものを直す。 |
| `poetry run ruff format .` | Black互換のスタイルに整形し、コードを美しく統一する。 |
| `poetry run ruff format . --check` | フォーマットが必要なファイルがないか確認する（CIで使うことがあります）。 |

**使い方**:
1.  **開発中**は `poetry run ruff format .` を頻繁に実行し、コードを常に整形された状態に保ちます。
2.  **コミット前**に `poetry run ruff check .` を実行し、修正可能なものは `--fix` で直します。
3.  **CI**では `poetry run ruff check .` を実行し、エラーがあればマージを禁止します。

---

## 🧠 Mypy

mypyは「型チェック」のみを行います。

| コマンド | 解説 |
| ---- | ---- |
| `poetry run mypy .` | コード全体をスキャンし、型ヒントの不整合やエラーを指摘する。これをCIで使います。 |
| `poetry run mypy path/to/file.py` | 特定のファイルだけをチェックし、結果を早く確認したいときに便利です。 |

**使い方**:
1.  **開発中**は `poetry run mypy .` を実行し、指摘された型エラーを一つずつ解決していきます。
2.  `poetry run mypy` はコードを自動修正しないため、エラーが出た場合は開発者が型ヒントを修正する必要があります。
3.  **CI**では `poetry run mypy .` を実行し、型エラーがあればマージを禁止します。

---

## 🧪 Pytest

pytestは「ロジックのテスト」を行います。

| コマンド | 解説 |
| ---- | ---- |
| `poetry run pytest` | コード全体をスキャンし、テストを実行します |
| `poetry run pytest path/to/file.py` | 特定のファイルのテストだけを実行します |
