import json
import streamlit as st

st.set_page_config(page_title="全銀コード検索", page_icon="🏦", layout="wide")


@st.cache_data
def load_banks():
    with open("banks.json", encoding="utf-8") as f:
        return json.load(f)


banks = load_banks()

st.title("🏦 全銀コード検索")

# ── 銀行検索 ──────────────────────────────────────────────────────────────────
st.header("銀行を選ぶ")

bank_query = st.text_input("銀行名・コードで絞り込み", placeholder="例: みずほ / 0001")

filtered_banks = {
    code: b
    for code, b in banks.items()
    if not bank_query
    or bank_query in b["name"]
    or bank_query in b["kana"]
    or bank_query in b["hira"]
    or bank_query in code
}

if not filtered_banks:
    st.warning("該当する銀行が見つかりません。")
    st.stop()

bank_options = {f"{b['code']} ｜ {b['name']}": code for code, b in filtered_banks.items()}
selected_label = st.selectbox("銀行", list(bank_options.keys()))
selected_code = bank_options[selected_label]
selected_bank = banks[selected_code]

col1, col2, col3 = st.columns(3)
col1.metric("銀行コード", selected_bank["code"])
col2.metric("銀行名（カナ）", selected_bank["kana"])
col3.metric("支店数", len(selected_bank["branches"]))

st.divider()

# ── 支店検索 ──────────────────────────────────────────────────────────────────
st.header("支店を絞り込む")

branch_query = st.text_input("支店名・コードで絞り込み", placeholder="例: 新宿 / 001")

branches = selected_bank["branches"]
if isinstance(branches, list):
    # to_dict() がリストを返す場合の互換対応
    branches = branches[0] if branches else {}

filtered_branches = {
    code: br
    for code, br in branches.items()
    if not branch_query
    or branch_query in br["name"]
    or branch_query in br["kana"]
    or branch_query in br["hira"]
    or branch_query in code
}

st.caption(f"{len(filtered_branches)} 支店表示中（全 {len(branches)} 支店）")

if filtered_branches:
    rows = [
        {"支店コード": br["code"], "支店名": br["name"], "カナ": br["kana"], "ローマ字": br["roma"]}
        for br in filtered_branches.values()
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.warning("該当する支店が見つかりません。")
