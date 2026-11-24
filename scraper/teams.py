import re

from download import download

def get_team_codes(year: int) -> list[str]:
    """その年の球団コードの一覧を返す（例: ["b", "c", ...]）"""
    url = f"https://npb.jp/bis/{year}/stats/"
    path = f"data/html/{year}/index.html"          # ① ステップ 1 で保存したファイル名
    html = download(url, path)
    codes = re.findall(r"idb1_([a-z]+)\.html", html)       # ② パターンを考える
    return sorted(set(codes))              # ③ 重複を消す

if __name__ == "__main__":
    print(get_team_codes(2025))
    print(get_team_codes(2005))