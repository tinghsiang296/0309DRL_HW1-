import streamlit as st
import grid_logic
import pandas as pd

st.set_page_config(page_title="和風 GridWorld: Value Iteration", layout="wide")

# Enhanced Japanese Zen Artistic Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Noto Serif JP', serif;
    }

    /* Traditional Washi Paper Background with discrete texture */
    .stApp {
        background-color: #fcfcfc;
        background-image: 
            radial-gradient(#d1d5db 0.4px, transparent 0.4px),
            radial-gradient(#d1d5db 0.4px, #fcfcfc 0.4px);
        background-size: 24px 24px;
        background-position: 0 0, 12px 12px;
        color: #111827;
    }

    /* Sidebar Styling - Lacquer Red Border */
    [data-testid="stSidebar"] {
        background-color: #f9fafb !important;
        border-right: 2px solid #ef4444;
    }

    /* Calligraphic Header with deeper red */
    h1 {
        color: #b91c1c;
        font-weight: 700;
        text-align: center;
        border-bottom: 1px solid #b91c1c;
        padding-bottom: 20px;
        margin-bottom: 40px !important;
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }

    /* Grid Button Styling - Zen Minimalist Box */
    .stButton > button {
        border-radius: 0px !important; /* Sharp corners for traditional feel */
        height: 80px !important;
        background: white !important;
        border: 1.5px solid #1f2937 !important;
        color: #1f2937 !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        box-shadow: 4px 4px 0px #1f2937 !important;
        font-size: 1.1rem !important;
    }

    .stButton > button:hover {
        border-color: #ef4444 !important;
        color: #ef4444 !important;
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #ef4444 !important;
    }

    .stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 0px 0px 0px #ef4444 !important;
    }

    /* Primary Button Styling (VI Button) */
    div.stButton > button[kind="primary"] {
        background: #ef4444 !important;
        color: white !important;
        border: 1.5px solid #b91c1c !important;
        box-shadow: 4px 4px 0px #991b1b !important;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #dc2626 !important;
        box-shadow: 6px 6px 0px #991b1b !important;
    }

    /* Status Card - Subtle Ink Wash Effect */
    .status-card {
        background: rgba(255, 255, 255, 0.9);
        border-left: 8px solid #b91c1c;
        padding: 1.5rem;
        margin-bottom: 3rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        font-style: italic;
    }

    /* Table Styling */
    .stTable {
        border: 1px solid #e5e7eb;
        border-radius: 4px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "n" not in st.session_state: st.session_state.n = 5
if "start_cell" not in st.session_state: st.session_state.start_cell = None
if "end_cell" not in st.session_state: st.session_state.end_cell = None
if "obstacles" not in st.session_state: st.session_state.obstacles = []
if "pi_policy" not in st.session_state: st.session_state.pi_policy = None
if "v_vals" not in st.session_state: st.session_state.v_vals = None

def reset_callback():
    st.session_state.start_cell = None
    st.session_state.end_cell = None
    st.session_state.obstacles = []
    st.session_state.pi_policy = None
    st.session_state.v_vals = None

st.title("⛩️ 和風 GridWorld")

with st.sidebar:
    st.markdown("### 📜 卷軸設定 (Settings)")
    new_n = st.number_input("次元 n (Dimension)", min_value=5, max_value=9, value=st.session_state.n)
    if new_n != st.session_state.n:
        st.session_state.n = new_n
        reset_callback()
    
    st.button("🧹 淨空網格 (Reset)", on_click=reset_callback, use_container_width=True)
    
    st.divider()
    
    # Specific Button Names requested by user
    if st.button("🎲 隨機初始化", use_container_width=True):
        st.session_state.pi_policy = grid_logic.generate_random_policy(st.session_state.n)
        st.session_state.v_vals = None
        st.toast("隨機策略已載入。")

    if st.button("✨ 執行價值迭代 (VI)", use_container_width=True, type="primary"):
        if st.session_state.start_cell and st.session_state.end_cell and \
           len(st.session_state.obstacles) == st.session_state.n - 2:
            
            v_vals, pi_policy = grid_logic.value_iteration(
                st.session_state.n, 
                st.session_state.end_cell, 
                st.session_state.obstacles
            )
            st.session_state.v_vals = v_vals
            st.session_state.pi_policy = pi_policy
        else:
            st.error(f"佈局未全。需起點、終點與 {st.session_state.n-2} 個障礙物。")

# Status Guidance
with st.container():
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    if not st.session_state.start_cell:
        st.markdown("🎋 **第一步**：選定 **起始之處** (Start)。")
    elif not st.session_state.end_cell:
        st.markdown("⛩️ **第二步**：指明 **歸宿之所** (Goal)。")
    elif len(st.session_state.obstacles) < st.session_state.n - 2:
        rem = st.session_state.n - 2 - len(st.session_state.obstacles)
        st.markdown(f"🪨 **第三步**：佈置 **礙世之石** ({len(st.session_state.obstacles)}/{st.session_state.n-2})。")
    elif not st.session_state.pi_policy and not st.session_state.v_vals:
        st.markdown("🎲 **第四步**：點擊「隨機初始化」或直接「執行價值迭代」。")
    else:
        st.markdown("🌸 **心法大成**：最優價值與策略已顯現於網格。")
    st.markdown('</div>', unsafe_allow_html=True)

# Grid Layout
n = st.session_state.n
grid_cols = st.columns(n)

for r in range(n):
    for c in range(n):
        pos = f"{r},{c}"
        label = " "
        
        # Display Icons/Arrows
        if pos == st.session_state.start_cell:
            label = "🎋"
        elif pos == st.session_state.end_cell:
            label = "⛩️"
        elif pos in st.session_state.obstacles:
            label = "🪨"
        elif st.session_state.pi_policy:
            policy = st.session_state.pi_policy[pos]
            arrow_map = { 'U': '↑', 'D': '↓', 'L': '←', 'R': '→', '': ' ' }
            
            if st.session_state.v_vals:
                val = st.session_state.v_vals[pos]
                label = f"{arrow_map[policy]}\n{val:.2f}"
            else:
                label = f"{arrow_map[policy]}"
        
        def cell_click(p=pos):
            if not st.session_state.start_cell:
                st.session_state.start_cell = p
            elif not st.session_state.end_cell:
                if p != st.session_state.start_cell: st.session_state.end_cell = p
            elif len(st.session_state.obstacles) < st.session_state.n - 2:
                if p not in [st.session_state.start_cell, st.session_state.end_cell] and p not in st.session_state.obstacles:
                    st.session_state.obstacles.append(p)

        with grid_cols[c]:
            st.button(label, key=pos, on_click=cell_click, use_container_width=True)

# Zen Summary Table
if st.session_state.v_vals:
    st.divider()
    st.markdown("### 📊 萬象價值清單 (Universal State Values)")
    df_rows = []
    for r in range(n):
        row = {}
        for c in range(n):
            pos = f"{r},{c}"
            if pos in st.session_state.obstacles: row[f"C{c}"] = "🪨"
            elif pos == st.session_state.end_cell: row[f"C{c}"] = "⛩️"
            else: row[f"C{c}"] = f"{st.session_state.v_vals[pos]:.2f}"
        df_rows.append(row)
    st.table(pd.DataFrame(df_rows))
