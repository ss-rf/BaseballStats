import io

import pandas as pd

from fetch import fetch_html   # ステップ 3 で作った関数を再利用する

html = fetch_html("https://npb.jp/bis/2025/stats/bat_c.html")
dfs = pd.read_html(io.StringIO(html))

print(type(dfs), len(dfs))   # ① 何が返ってきた？
df = dfs[0]                # ② 表はどこにある？

print(df.shape)              # ③ (行数, 列数)
print(df.head())             # ④ 先頭5行
print(df.dtypes)             # ⑤ 各列の型