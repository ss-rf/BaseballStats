import re

from fetch import save_csv
from parse import (parse_batting_old, parse_fielding_new, parse_fielding_old,
                   parse_new, parse_pitching_old, read_html)
from teams import get_team_codes

YEARS = range(2005, 2027)
PREFIX = {"batting": "idb1", "pitching": "idp1", "fielding": "idf1"}

def parse_title(html: str) -> tuple[str, str]:
    """タイトルから（球団名, リーグ）を取り出す"""
    m = re.search(r"<title>\d+年度 (\S+) 個人\S+成績（(\S+)）", html)
    return m.group(1), m.group(2)                    # ③ 何番目の ( ) か

def parse_page(kind: str, year: int, html: str) -> list[dict]:
    """種類と年度に合った解析関数を呼ぶ"""
    if year >= 2025:                                       # 新形式
        if kind == "batting":
            return parse_new(html, "打")
        elif kind == "pitching":
            return parse_new(html, "投")                                    # ④
        else:
            return parse_fielding_new(html)                                    # ⑤
    else:                                                  # 旧形式
        if kind == "batting":
            return parse_batting_old(html)                                    # ⑥
        elif kind == "pitching":
            return parse_pitching_old(html)                                    # ⑦
        else:
            return parse_fielding_old(html)                                    # ⑧

def build(kind: str) -> list[dict]:
    """全年度・全球団のページを解析して、1 つのリストにまとめる"""
    rows = []
    for year in YEARS:
        for code in get_team_codes(year):
            html = read_html(f"data/html/{year}/{PREFIX[kind]}_{code}.html")
            team, league = parse_title(html)
            meta = {"年度": year, "球団コード": code, "球団": team, "リーグ": league}   # ⑨
            for row in parse_page(kind, year, html):
                rows.append({**meta, **row})
    return rows

if __name__ == "__main__":
    for kind in PREFIX:
        rows = build(kind)
        save_csv(rows, f"data/raw/{kind}.csv")
        print(kind, len(rows))