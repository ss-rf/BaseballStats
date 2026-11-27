from download import download
from teams import get_team_codes

PREFIXES = ["idb1", "idp1", "idf1"]   # 打撃・投球・守備

def download_year(year: int) -> None:
    """その年の全球団 × 3 種類の HTML を保存する"""
    codes = get_team_codes(year)                           # ① 球団コードの一覧
    for team in codes:
        for prefix in PREFIXES:                      # ② 3 種類を回す
            name = f"{prefix}_{team}.html"
            url = f"https://npb.jp/bis/{year}/stats/{name}"
            path = f"data/html/{year}/{name}"     # ③ 保存先
            try:                                # ④
                download(url, path)
                print("OK", year, name)
            except Exception as e:                 # ⑤
                print("NG", url, e)

if __name__ == "__main__":
    for year in range(2005, 2027):
        download_year(year)