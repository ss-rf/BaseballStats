from pathlib import Path

from bs4 import BeautifulSoup

def parse_batting_new(html: str) -> list[dict]:
    """2025 年以降の球団別打撃ページを解析する"""
    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one("table.tablefix2")                      # ① 表
    headers = [th.get_text(strip=True) for th in table.select("thead th")]
    rows = []
    for tr in table.select("tbody tr"):
        tds = tr.select("td")
        name_td = tds[0]                              # ② 選手名は何列目？
        sup = name_td.select_one("sup")                 # ③ 左打ちの印
        if sup is not None:
            sup.extract()                                   # ④ 取り除く
        values = [td.get_text(strip=True) for td in tds]
        row = dict(zip(headers, values))
        row["左打"] = sup is not None                               # ⑤ True / False
        rows.append(row)
    return rows

if __name__ == "__main__":
    html = Path("data/html/2025/idb1_g.html").read_text(encoding="utf-8")
    rows = parse_batting_new(html)
    print(len(rows))
    print(rows[-3])
    print(rows[-2])