import streamlit as st
import grid_logic
import pandas as pd

st.set_page_config(page_title="GridWorld RL HW1", layout="wide")

st.markdown("""
<style>
.grid-container {
    display: grid;
    gap: 10px;
    margin-top: 20px;
}
.cell {
    width: 60px;
    height: 60px;
    border: 1px solid #ccc;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 0.8rem;
    cursor: pointer;
}
.start { background-color: #22c55e !important; color: white; }
.end { background-color: #ef4444 !important; color: white; }
.obstacle { background-color: #64748b !important; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("GridWorld RL HW1")

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

with st.sidebar:
    st.header("Controls")
    new_n = st.number_input("Dimension n (5-9)", min_value=5, max_value=9, value=st.session_state.n)
    if new_n != st.session_state.n:
        st.session_state.n = new_n
        reset_callback()
    
    st.button("Reset Grid", on_click=reset_callback)
    
    if st.button("Evaluate Policy"):
        if st.session_state.start_cell and st.session_state.end_cell and len(st.session_state.obstacles) == st.session_state.n - 2:
            policy = grid_logic.generate_random_policy(st.session_state.n)
            values = grid_logic.policy_evaluation(
                st.session_state.n, 
                st.session_state.start_cell, 
                st.session_state.end_cell, 
                st.session_state.obstacles, 
                policy
            )
            st.session_state.results = {"policy": policy, "values": values}
        else:
            st.error(f"Please set Start, End, and {st.session_state.n-2} Obstacles first.")

# Instructions
if not st.session_state.start_cell:
    st.info("Step 1: Click a cell to set the **START** point.")
elif not st.session_state.end_cell:
    st.info("Step 2: Click a cell to set the **END** point.")
elif len(st.session_state.obstacles) < st.session_state.n - 2:
    st.info(f"Step 3: Click cells to set **OBSTACLES** ({len(st.session_state.obstacles)}/{st.session_state.n-2}).")
else:
    st.success("Grid setup complete! click 'Evaluate Policy' in the sidebar.")

# Grid Rendering
n = st.session_state.n
cols = st.columns(n)

for r in range(n):
    for c in range(n):
        pos = f"{r},{c}"
        label = ""
        css_class = ""
        
        if pos == st.session_state.start_cell:
            label = "Start"
            css_class = "start"
        elif pos == st.session_state.end_cell:
            label = "End"
            css_class = "end"
        elif pos in st.session_state.obstacles:
            label = "Obs"
            css_class = "obstacle"
        elif st.session_state.results:
            policy = st.session_state.results["policy"][pos]
            val = st.session_state.results["values"][pos]
            arrow_map = { 'U': '↑', 'D': '↓', 'L': '←', 'R': '→' }
            label = f"{arrow_map[policy]}\n{val:.2f}"
        
        def cell_click(p=pos):
            if not st.session_state.start_cell:
                st.session_state.start_cell = p
            elif not st.session_state.end_cell:
                if p != st.session_state.start_cell:
                    st.session_state.end_cell = p
            elif len(st.session_state.obstacles) < st.session_state.n - 2:
                if p not in [st.session_state.start_cell, st.session_state.end_cell] and p not in st.session_state.obstacles:
                    st.session_state.obstacles.append(p)

        with cols[c]:
            st.button(label if label else " ", key=pos, on_click=cell_click, use_container_width=True)

# Status Table (Optional)
if st.session_state.results:
    st.divider()
    st.subheader("Results Data")
    df_data = []
    for r in range(n):
        row = []
        for c in range(n):
            pos = f"{r},{c}"
            if pos in st.session_state.obstacles or pos == st.session_state.end_cell:
                row.append("Goal/Obs")
            else:
                row.append(f"{st.session_state.results['values'][pos]:.2f}")
        df_data.append(row)
    st.table(pd.DataFrame(df_data))
