import time
from pathlib import Path

from fetch import fetch_html


def download(url: str, path: str) -> str:
    """URL の HTML を返す。path に保存済みならそれを読み、なければ取得して保存する"""
    file = Path(path)

    # 1. 保存済みなら、ファイルを読んで返す
    if file.exists():
        return file.read_text(encoding="utf-8")

    # 2. NPB から取得する
    html = fetch_html(url)

    # 3. 保存する（フォルダがなければ作る）
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(html, encoding="utf-8")

    # 4. 待つ
    time.sleep(3)

    # 5. 返す
    return html


if __name__ == "__main__":
    html = download("https://npb.jp/bis/2025/stats/", "data/html/2025/index.html")
    print(len(html))