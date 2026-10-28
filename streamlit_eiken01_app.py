import json
import random
import streamlit as st

# ページの設定
st.set_page_config(
    page_title="英検1級 単語＆例文ジェネレーター", page_icon="📚", layout="wide"
)

st.title("📚 英検1級 トレンド単語・例文ジェネレーター")
st.markdown(
    "JSONファイル (`eiken04.json`) から英検1級レベルの高度な単語を抽出し、実用的な例文とともに対話形式で表示するアプリです。"
)


# JSONファイルからデータを読み込む関数（キャッシュ付き）
@st.cache_data
def load_eiken_word_pool():
    """eiken04.jsonから英検1級関連の語彙データを読み込む関数。"""
    try:
        with open("eiken04.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # ファイル読み込みエラー時のフォールバック
        st.error(f"JSONファイルの読み込みに失敗しました: {e}")
        return [
            {
                "word": "Ubiquitous",
                "meaning": "至る所にある、遍在する",
                "sentence": (
                    "Smartphones have become ubiquitous in modern daily life."
                ),
                "translation": (
                    "スマートフォンは現代の日常生活において至る所に見られるようになった。"
                ),
            }
        ]


# セッション状態の初期化（キャッシュによる重複を防ぎ、毎回確実にシャッフルするため）
if "word_list" not in st.session_state:
    all_pool = load_eiken_word_pool()
    st.session_state.word_list = random.sample(
        all_pool, min(10, len(all_pool))
    )

# メイン処理の更新ボタン
if st.button("🔄 最新の英検1級単語を10件シャッフル・読み込む", type="primary"):
    all_pool = load_eiken_word_pool()
    st.session_state.word_list = random.sample(
        all_pool, min(10, len(all_pool))
    )
    st.rerun()

st.success(
    f"📂 JSONファイルから抽出された英検1級単語"
    f" {len(st.session_state.word_list)}件 を取得しました！"
)

# 1つずつカード形式で表示
for i, item in enumerate(st.session_state.word_list, 1):
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"### **{i}. {item['word']}**")
            st.caption(f"意味: {item['meaning']}")
        with col2:
            st.markdown(f"**📝 例文:** `{item['sentence']}`")
            st.markdown(f"**🇯🇵 和訳:** {item['translation']}")

# フッター
st.markdown("---")
st.markdown("💡 *Tip: ボタンを押すたびに、異なる10件の単語セットに入れ替わります。*")