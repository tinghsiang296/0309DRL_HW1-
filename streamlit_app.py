import streamlit as st
import grid_logic
import pandas as pd

st.set_page_config(page_title="GridWorld Elite", layout="wide")

# Premium Artistic Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Gradient Background */
    .stApp {
        background: radial-gradient(circle at top left, #1e293b, #0f172a);
        color: #f8fafc;
    }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Header Styling */
    h1 {
        background: linear-gradient(90deg, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        letter-spacing: -0.02em;
        text-align: center;
        margin-bottom: 2rem !important;
    }

    /* Grid Cell Styling */
    .stButton > button {
        border-radius: 12px !important;
        height: 70px !important;
        background: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #94a3b8 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }

    .stButton > button:hover {
        border-color: #3b82f6 !important;
        transform: translateY(-2px);
        background: rgba(59, 130, 246, 0.1) !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
    }

    /* Special Cell States */
    div.stButton > button:active { transform: scale(0.95); }
    
    /* Start, End, Obstacle Highlights (Injecting via class logic in Python is limited, so we use themes) */
    
    .status-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        margin-bottom: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "n" not in st.session_state:
    st.session_state.n = 5
if "start_cell" not in st.session_state:
    st.session_state.start_cell = None
if "end_cell" not in st.session_state:
    st.session_state.end_cell = None
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "results" not in st.session_state:
    st.session_state.results = None

def reset_callback():
    st.session_state.start_cell = None
    st.session_state.end_cell = None
    st.session_state.obstacles = []
    st.session_state.results = None

st.title("GridWorld RL Optimization: Value Iteration")

with st.sidebar:
    st.markdown("### ⚙️ System Controls")
    new_n = st.number_input("Dimension n (5-9)", min_value=5, max_value=9, value=st.session_state.n)
    if new_n != st.session_state.n:
        st.session_state.n = new_n
        reset_callback()
    
    st.button("🔄 Reset Grid Environment", on_click=reset_callback, use_container_width=True)
    
    st.divider()
    
    if st.button("🚀 Run Value Iteration", use_container_width=True, type="primary"):
        if st.session_state.start_cell and st.session_state.end_cell and len(st.session_state.obstacles) == st.session_state.n - 2:
            values, policy = grid_logic.value_iteration(
                st.session_state.n, 
                st.session_state.end_cell, 
                st.session_state.obstacles
            )
            st.session_state.results = {"policy": policy, "values": values}
        else:
            st.error(f"Setup missing. Requires Start, End, and {st.session_state.n-2} Obstacles.")

# Instructions with glassmorphism container
with st.container():
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    if not st.session_state.start_cell:
        st.markdown("📍 Step 1: Initialize the **START** position (Green).")
    elif not st.session_state.end_cell:
        st.markdown("🎯 Step 2: Establish the **GOAL** destination (Red).")
    elif len(st.session_state.obstacles) < st.session_state.n - 2:
        rem = st.session_state.n - 2 - len(st.session_state.obstacles)
        st.markdown(f"🚧 Step 3: Deploy **OBSTACLES** ({len(st.session_state.obstacles)}/{st.session_state.n-2}). {rem} remaining.")
    else:
        st.markdown("✨ **Configuration Finalized**. Execute Value Iteration via sidebar.")
    st.markdown('</div>', unsafe_allow_html=True)

# Grid Rendering with Dynamic Icons
n = st.session_state.n
grid_cols = st.columns(n)

for r in range(n):
    for c in range(n):
        pos = f"{r},{c}"
        label = " "
        help_text = f"Cell ({r}, {c})"
        
        # Determine Cell Label and Display
        if pos == st.session_state.start_cell:
            label = "🟢 START"
        elif pos == st.session_state.end_cell:
            label = "🔴 GOAL"
        elif pos in st.session_state.obstacles:
            label = "⬛ OBS"
        elif st.session_state.results:
            policy = st.session_state.results["policy"][pos]
            val = st.session_state.results["values"][pos]
            arrow_map = { 'U': '↑', 'D': '↓', 'L': '←', 'R': '→', '': '' }
            label = f"{arrow_map[policy]}\n{val:.2f}"
            help_text = f"Value: {val:.4f}"
        
        def cell_click(p=pos):
            if not st.session_state.start_cell:
                st.session_state.start_cell = p
            elif not st.session_state.end_cell:
                if p != st.session_state.start_cell:
                    st.session_state.end_cell = p
            elif len(st.session_state.obstacles) < st.session_state.n - 2:
                if p not in [st.session_state.start_cell, st.session_state.end_cell] and p not in st.session_state.obstacles:
                    st.session_state.obstacles.append(p)

        with grid_cols[c]:
            st.button(label, key=pos, on_click=cell_click, use_container_width=True, help=help_text)

# Analysis Table
if st.session_state.results:
    st.divider()
    st.subheader("📊 Convergence Analytics")
    df_data = []
    for r in range(n):
        row = {}
        for c in range(n):
            pos = f"{r},{c}"
            if pos == st.session_state.end_cell:
                row[f"Col {c}"] = "GOAL"
            elif pos in st.session_state.obstacles:
                row[f"Col {c}"] = "X"
            else:
                row[f"Col {c}"] = f"{st.session_state.results['values'][pos]:.2f}"
        df_data.append(row)
    st.dataframe(pd.DataFrame(df_data), height=250, use_container_width=True)
