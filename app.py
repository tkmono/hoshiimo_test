# app.py（修正済み！）
import streamlit as st
import pandas as pd

# CSV読み込み
df = pd.read_csv("hoshiimo_data.csv")

# 5段階の選択肢（CSVの1～5に対応！）
options = {
    "種類": ["丸干し", "丸干し寄り", "セット", "平干し寄り", "平干し"],
    "用途": ["贈答用", "贈答寄り", "両方OK", "自分用寄り", "自分用"],
    "予算": ["とても安い", "安め", "普通", "高め", "とても高い"],
    "食感": ["とてもねっとり", "ねっとり寄り", "普通", "しっとり寄り", "とてもしっとり"],
    "量": ["とても少ない(50g)", "少なめ(100g)", "普通(300g)", "多め(1kg)", "とても多い(2kg)"],
    "食べ方": ["そのまま", "少しアレンジ", "両方OK", "アレンジ寄り", "アレンジ料理"],
    "温度": ["冷やして", "少し冷やし", "常温", "少し温め", "温めて"],
    "品質": ["型落ち品", "B級品", "標準", "高級品", "最高級品"],
    "甘さ": ["さっぱり", "少し甘い", "普通", "甘め", "とても甘い"],
    "産地": ["茨城", "茨城寄り", "どっちでも", "鹿児島寄り", "鹿児島"]
}

st.title("干し芋マッチングアプリ")
st.subheader("あなたの好みにぴったりの干し芋を見つけます！")

# フォーム
user = {}
for col, opts in options.items():
    user[col] = st.selectbox(col, opts)

if st.button("おすすめを教えて！"):
    # 修正ポイント：選択肢の「位置」を数字に変換（0～4 → 1～5）
    user_num = {}
    for col, val in user.items():
        opts = options[col]
        user_num[col] = opts.index(val) + 1  # 0から始まる → 1から始まる

    # 一致度計算
    一致数 = pd.Series([0] * len(df))
    for col in user_num.keys():
        一致数 += (df[col] == user_num[col])
    
    df["一致度"] = 一致数 / len(user_num) * 100
    
    # 1位を取得
    best = df.sort_values("一致度", ascending=False).iloc[0]
    
    st.success(f"**{best['商品名']}** がおすすめ！")
    st.write(f"一致度：**{best['一致度']:.0f}%**")
    st.dataframe(df[["商品名", "一致度"]].sort_values("一致度", ascending=False).reset_index(drop=True))
    st.balloons()