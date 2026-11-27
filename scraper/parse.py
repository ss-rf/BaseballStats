from pathlib import Path

from bs4 import BeautifulSoup, Tag

HAND = {"*": "左", "+": "両"}   # 印 → 利き手（印がなければ右）

def parse_table(table: Tag, hand_key: str) -> list[dict]:
    """tablefix2 の表 1 つを解析する"""
    headers = [th.get_text(strip=True) for th in table.select("thead th")]
    rows = []
    for tr in table.select("tbody tr"):
        tds = tr.select("td")
        name_td = tds[0]
        sup = name_td.select_one("sup")
        mark = ""
        if sup is not None:
            mark = sup.get_text(strip=True)                  # ① 印の文字を取り出す
            sup.extract()
        values = [td.get_text(strip=True) for td in tds]
        row = dict(zip(headers, values))
        row[hand_key] = HAND.get(mark, "右")             # ② 印 → 右・左・両
        rows.append(row)
    return rows

def parse_new(html: str, hand_key: str) -> list[dict]:
    """2025 年以降の打撃・投球ページを解析する"""
    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one("table.tablefix2")
    return parse_table(table, hand_key)                         # ① 上の関数に任せる

def parse_fielding_new(html: str) -> list[dict]:
    """2025 年以降の守備ページを解析する（守備位置ごとに表がある）"""
    soup = BeautifulSoup(html, "lxml")
    rows = []
    for table in soup.select("table.tablefix2"):           # ② 表を全部
        position = table.find_previous_sibling("h5").get_text(strip=True)   # ③ 見出し
        for row in parse_table(table, "投"):
            row["守備位置"] = position                        # ④
            rows.append(row)
    return rows

def read_html(path: str) -> str:
    """保存済みの HTML を読む"""
    return Path(path).read_text(encoding="utf-8")

if __name__ == "__main__":
    batting = parse_new(read_html("data/html/2025/idb1_g.html"), "打")
    pitching = parse_new(read_html("data/html/2025/idp1_g.html"), "投")
    fielding = parse_fielding_new(read_html("data/html/2025/idf1_g.html"))
    print(len(batting), len(pitching), len(fielding))
    print(fielding[0])
    for row in fielding:
        if row["守備位置"] == "捕手":
            print(row)
    rakuten = parse_new(read_html("data/html/2025/idb1_e.html"), "打")
    for row in rakuten:
        if row["打"] == "両":
            print(row["選手"], row["打"])