from pathlib import Path

from bs4 import BeautifulSoup, Tag

HAND = {"*": "左", "+": "両"}   # 印 → 利き手（印がなければ右）

BATTING_COLS = ["選手", "試合", "打席", "打数", "得点", "安打", "二塁打", "三塁打",
                "本塁打", "塁打", "打点", "盗塁", "盗塁刺", "犠打", "犠飛", "四球",
                "故意四", "死球", "三振", "併殺打", "打率", "長打率", "出塁率"]
PITCHING_COLS = ["選手", "登板", "勝利", "敗北", "セーブ", "ホールド", "ＨＰ", "完投",
                 "完封勝", "無四球", "勝率", "打者", "投球回", "安打", "本塁打", "四球",
                 "故意四", "死球", "三振", "暴投", "ボーク", "失点", "自責点", "防御率"]
FIELDING_COLS = ["選手", "試合", "刺殺", "補殺", "失策", "併殺", "捕逸", "守備率"]

def parse_old_row(tr: Tag, columns: list[str], hand_key: str) -> dict:
    """旧形式の 1 行（tr.ststats）を辞書にする"""
    tds = tr.select("td")
    mark = tds[0].get_text(strip=True)                        # ① 印は何列目？
    values = [td.get_text(strip=True) for td in tds[1:]]      # ② 選手名から後ろ
    row = dict(zip(columns, values))
    row[hand_key] = HAND.get(mark, "右")
    return row

def parse_batting_old(html: str) -> list[dict]:
    """2024 年以前の打撃ページを解析する"""
    soup = BeautifulSoup(html, "lxml")
    rows = []
    for tr in soup.select("tr.ststats"):                               # ③ 選手の行
        rows.append(parse_old_row(tr, BATTING_COLS, "打"))
    return rows

def parse_pitching_old(html: str) -> list[dict]:
    """2024 年以前の投球ページを解析する（投球回が 2 マスに分かれている）"""
    soup = BeautifulSoup(html, "lxml")
    rows = []
    for tr in soup.select("tr.ststats"):
        fraction_td = tr.select("td")[14]                      # ④ 端数のマス
        fraction = fraction_td.get_text(strip=True)
        fraction_td.extract()                                       # ⑤ 取り外す
        row = parse_old_row(tr, PITCHING_COLS, "投")
        row["投球回"] = row["投球回"] + fraction                      # ⑥ くっつける
        rows.append(row)
    return rows

def parse_fielding_old(html: str) -> list[dict]:
    """2024 年以前の守備ページを解析する（1 つの表に全守備位置が並んでいる）"""
    soup = BeautifulSoup(html, "lxml")
    rows = []
    position = ""
    for tr in soup.select("tr"):
        th = tr.select_one("th.sthdfplayer")
        if th is not None:                                  # 見出しの行
            position = th.get_text(strip=True).strip("【】")  # ① 【】を取る
        elif "ststats" in tr.get("class", []):              # 選手の行
            row = parse_old_row(tr, FIELDING_COLS, "投")             # ② 列名リスト
            row["守備位置"] = position                          # ③
            rows.append(row)
    return rows

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
    fielding = parse_fielding_old(read_html("data/html/2024/idf1_g.html"))
    print(len(fielding))
    print(fielding[0])
    for row in fielding:
        if row["守備位置"] == "捕手":
            print(row)