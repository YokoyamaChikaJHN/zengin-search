import json
import streamlit as st

# 全角カナ → 半角カナ変換テーブル
# 濁音・半濁音は 清音＋濁点(ﾞ/ﾟ) の2文字に分解、拗音は通常文字に統一
_HANKAKU_TABLE = str.maketrans({
    'ガ': 'ｶﾞ', 'ギ': 'ｷﾞ', 'グ': 'ｸﾞ', 'ゲ': 'ｹﾞ', 'ゴ': 'ｺﾞ',
    'ザ': 'ｻﾞ', 'ジ': 'ｼﾞ', 'ズ': 'ｽﾞ', 'ゼ': 'ｾﾞ', 'ゾ': 'ｿﾞ',
    'ダ': 'ﾀﾞ', 'ヂ': 'ﾁﾞ', 'ヅ': 'ﾂﾞ', 'デ': 'ﾃﾞ', 'ド': 'ﾄﾞ',
    'バ': 'ﾊﾞ', 'ビ': 'ﾋﾞ', 'ブ': 'ﾌﾞ', 'ベ': 'ﾍﾞ', 'ボ': 'ﾎﾞ',
    'パ': 'ﾊﾟ', 'ピ': 'ﾋﾟ', 'プ': 'ﾌﾟ', 'ペ': 'ﾍﾟ', 'ポ': 'ﾎﾟ',
    'ヴ': 'ｳﾞ',
    'ア': 'ｱ', 'イ': 'ｲ', 'ウ': 'ｳ', 'エ': 'ｴ', 'オ': 'ｵ',
    'カ': 'ｶ', 'キ': 'ｷ', 'ク': 'ｸ', 'ケ': 'ｹ', 'コ': 'ｺ',
    'サ': 'ｻ', 'シ': 'ｼ', 'ス': 'ｽ', 'セ': 'ｾ', 'ソ': 'ｿ',
    'タ': 'ﾀ', 'チ': 'ﾁ', 'ツ': 'ﾂ', 'テ': 'ﾃ', 'ト': 'ﾄ',
    'ナ': 'ﾅ', 'ニ': 'ﾆ', 'ヌ': 'ﾇ', 'ネ': 'ﾈ', 'ノ': 'ﾉ',
    'ハ': 'ﾊ', 'ヒ': 'ﾋ', 'フ': 'ﾌ', 'ヘ': 'ﾍ', 'ホ': 'ﾎ',
    'マ': 'ﾏ', 'ミ': 'ﾐ', 'ム': 'ﾑ', 'メ': 'ﾒ', 'モ': 'ﾓ',
    'ヤ': 'ﾔ', 'ユ': 'ﾕ', 'ヨ': 'ﾖ',
    'ラ': 'ﾗ', 'リ': 'ﾘ', 'ル': 'ﾙ', 'レ': 'ﾚ', 'ロ': 'ﾛ',
    'ワ': 'ﾜ', 'ヲ': 'ｦ', 'ン': 'ﾝ',
    # 拗音（小さい仮名）→ 通常の仮名（半角）
    'ァ': 'ｱ', 'ィ': 'ｲ', 'ゥ': 'ｳ', 'ェ': 'ｴ', 'ォ': 'ｵ',
    'ャ': 'ﾔ', 'ュ': 'ﾕ', 'ョ': 'ﾖ', 'ッ': 'ﾂ',
    'ー': 'ｰ', '・': '･',
})

def to_hankaku(text: str) -> str:
    return text.translate(_HANKAKU_TABLE)

_BRANCH_SUFFIXES = ('出張所', '営業部', '本店', 'センター', 'ローンプラザ',
                    'ローンセンター', '事務センター', 'サービスセンター')

def with_suffix(name: str) -> str:
    if any(name.endswith(s) for s in _BRANCH_SUFFIXES):
        return name
    return name + '支店'

_BANK_SUFFIXES = ('農協', '信金', '労金', '金庫')

def bank_fullname(name: str) -> str:
    if any(name.endswith(s) for s in _BANK_SUFFIXES):
        return name
    return name + '銀行'

st.set_page_config(page_title="全銀コード検索", page_icon="🏦", layout="wide")

st.markdown("""
<style>
/* disabled テキスト欄を通常のテキスト欄と同じ見た目に */
input[disabled] {
    cursor: text !important;
    -webkit-text-fill-color: inherit !important;
    opacity: 1 !important;
    color: inherit !important;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_banks():
    with open("banks.json", encoding="utf-8") as f:
        return json.load(f)


banks = load_banks()

st.title("🏦 全銀コード検索")

# ── 銀行検索 ──────────────────────────────────────────────────────────────────
st.header("銀行を選ぶ")

bank_query = st.text_input("銀行名・コードで絞り込み（部分一致）", placeholder="例: 住友 / みずほ / 0001")

q = bank_query.lower()
filtered_banks = {
    code: b
    for code, b in banks.items()
    if not q
    or q in b["name"]
    or q in b["kana"].lower()
    or q in b["hira"].lower()
    or q in b["roma"].lower()
    or q in code
}

if not filtered_banks:
    st.warning("該当する銀行が見つかりません。")
    st.stop()

bank_options = {f"{b['code']} ｜ {bank_fullname(b['name'])}": code for code, b in filtered_banks.items()}
selected_label = st.selectbox("銀行", list(bank_options.keys()))
selected_code = bank_options[selected_label]
selected_bank = banks[selected_code]

col1, col2, col3 = st.columns(3)
col1.metric("銀行コード", selected_bank["code"])
col2.text_input("銀行名（編集不可）", value=bank_fullname(selected_bank["name"]), disabled=True)
col3.metric("支店数", len(selected_bank["branches"]))

st.divider()

# ── 支店検索 ──────────────────────────────────────────────────────────────────
st.header("支店を絞り込む")

branch_query = st.text_input("支店名・コードで絞り込み（部分一致）", placeholder="例: 新宿 / shinjuku / 001")

branches = selected_bank["branches"]
if isinstance(branches, list):
    branches = branches[0] if branches else {}

bq = branch_query.lower()
filtered_branches = {
    code: br
    for code, br in branches.items()
    if not bq
    or bq in br["name"]
    or bq in br["kana"].lower()
    or bq in br["hira"].lower()
    or bq in br["roma"].lower()
    or bq in code
}

st.caption(f"{len(filtered_branches)} 支店表示中（全 {len(branches)} 支店）")

if filtered_branches:
    rows = [
        {"支店コード": br["code"], "支店名": with_suffix(br["name"]), "カナ": to_hankaku(br["kana"]), "ローマ字": br["roma"]}
        for br in filtered_branches.values()
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.warning("該当する支店が見つかりません。")
