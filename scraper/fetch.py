import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path

def fetch_html(url: str) -> str:
    """URL の HTML を文字列で返す"""
    headers = {"User-Agent": "BaseballStats-learning"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text

def parse_batting(html: str) -> list[dict]:
    """HTML から打撃成績を取り出し、1 選手 = 1 つの dict のリストで返す"""
    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one("table.tablefix2")

    # ===== 作業A: 見出しを集める（for の外で1回だけ） =====
    headers = [th.get_text(strip=True) for th in table.select("thead th")]

    # ===== 作業B: 選手を1人ずつ処理する =====
    rows = []
    for tr in table.select("tbody tr"):
        tds = tr.select("td")

        name_td = tds[1]
        team_span = name_td.select_one("span.stteam")
        team = team_span.get_text(strip=True).strip("()")
        team_span.extract()

        values = [td.get_text(strip=True) for td in tds]
        row = dict(zip(headers,values))
        row["球団"] = team
        rows.append(row)

    return rows



def save_csv(rows: list[dict], path: str) -> None:
    """リストを CSV に保存する"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8-sig") as f:

        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()    # 1行目に見出しを書く
        writer.writerows(rows)  # 全員分をまとめて書く

if __name__ == "__main__":
    html = fetch_html("https://npb.jp/bis/2025/stats/bat_c.html")
    rows = parse_batting(html)
    print(len(rows))
    save_csv(rows, "data/raw/batting_2025_c.csv")
    for row in rows:
        print(row["順位"], row["選手"], row["球団"])