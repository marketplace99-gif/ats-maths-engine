import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Configurations & ATS Branding Setup
st.set_page_config(
    page_title="ATS Math Engine Pro", 
    page_icon="🧮",
    layout="centered"
)

# --- INJECT NATIVE APP LOOK & FEEL (Fixed Sidebar Navigation) ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* This keeps the sidebar menu visible and usable */
        div[data-testid="stSidebarCollapsedControl"] {
            visibility: visible;
            left: 10px;
            top: 10px;
        }
        
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 800px;
        }
        div[data-testid="stSidebar"] {
            background-color: #1E222B;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize a persistent background log for storing calculations if it doesn't exist yet
if "history_log" not in st.session_state:
    st.session_state.history_log = []

# Sidebar Design with ATS Theme
st.sidebar.markdown("# 🚀 ATS Math Engine")
st.sidebar.markdown("### *Professional Edition*")
st.sidebar.markdown("---")

operation_type = st.sidebar.radio(
    "Select ATS Workspace",
    ["🧮 ATS Arithmetic Lab", "📐 ATS Algebraic Solver", "📈 ATS Calculus Suite", "📊 ATS Matrix Studio", "🔮 ATS Vector Grapher"]
)

# --- HISTORICAL LOG PANEL ---
st.sidebar.markdown("---")
st.sidebar.markdown("### ⏳ Session Activity Log")

if len(st.session_state.history_log) == 0:
    st.sidebar.caption("No calculations recorded yet.")
else:
    for item in reversed(st.session_state.history_log[-7:]):
        st.sidebar.info(f"**{item['module']}**\n\nIn: `{item['input']}`\n\nOut: `{item['output']}`")
    
    if st.sidebar.button("Clear Log History", use_container_width=True):
        st.session_state.history_log = []
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("ATS System Module v2.6")

# Universal Variables
x, y, z = sp.symbols('x y z')

def clean_math_input(user_input: str) -> str:
    """Intelligently rewrites natural math inputs into valid Python/SymPy code."""
    cleaned = user_input.replace('^', '**')
    import re
    cleaned = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', cleaned)
    cleaned = re.sub(r'(\))(\()', r'\1*\2', cleaned)
    cleaned = re.sub(r'(\))([a-zA-Z])', r'\1*\2', cleaned)
    return cleaned

# Main Header Banner
st.title("🚀 ATS Math Engine Pro")
st.markdown("---")

# --- 1. ARITHMETIC LAB ---
if operation_type == "🧮 ATS Arithmetic Lab":
    st.subheader("ATS Core Arithmetic Lab")
    
    with st.container(border=True):
        expr_str = st.text_input("Mathematical String Input:", "2^3 + 5/2")
        submit = st.button("Compute Result", use_container_width=True, type="primary")
        
    if submit:
        try:
            processed_input = clean_math_input(expr_str)
            expr = sp.sympify(processed_input)
            exact_val = str(expr)
            approx_val = f"{float(expr.evalf()):.4f}"
            
            st.session_state.history_log.append({
                "module": "Arithmetic",
                "input": expr_str,
                "output": exact_val
            })
            
            st.markdown("### Rendering & Solution")
            with st.container(border=True):
                st.latex(sp.latex(expr))
                
                col1, col2 = st.columns(2)
                col1.metric("Exact Math Representation", exact_val)
                col2.metric("Decimal Representation", approx_val)
        except Exception as e:
            st.error(f"Syntax/Parsing Error: {e}")

# --- 2. ALGEBRAIC SOLVER ---
elif operation_type == "📐 ATS Algebraic Solver":
    st.subheader("ATS Algebraic & Equation Solver")
    
    with st.container(border=True):
        eq_str = st.text_input("Enter Equation (Implicitly equals 0 if no '=' provided):", "x^2 - 3x + 2")
        submit = st.button("Find Solution Sets", use_container_width=True, type="primary")
        
    if submit:
        try:
            processed_input = clean_math_input(eq_str)
            equation = sp.Eq(sp.sympify(processed_input.split('=')[0]), sp.sympify(processed_input.split('=')[1])) if '=' in processed_input else sp.sympify(processed_input)
            solutions = sp.solve(equation, x)
            
            st.session_state.history_log.append({
                "module": "Algebra",
                "input": eq_str,
                "output": str(solutions)
            })
            
            st.markdown("### Target Problem Context")
            with st.container(border=True):
                st.latex(sp.latex(equation) + " = 0" if '=' not in eq_str else sp.latex(equation))
            
            st.markdown("### Extracted Real/Complex Solutions")
            for i, sol in enumerate(solutions, start=1):
                with st.container(border=True):
                    st.latex(f"x_{i} = {sp.latex(sol)}")
        except Exception as e:
            st.error(f"Algebra Engine Fault: {e}")

# --- 3. CALCULUS SUITE ---
elif operation_type == "📈 ATS Calculus Suite":
    st.subheader("ATS Symbolic Calculus Suite")
    
    with st.container(border=True):
        calc_expr = st.text_input("Function expression $f(x)$:", "3x^3 + sin(x)")
        calc_type = st.tabs(["Derivative (d/dx)", "Indefinite Integral (∫)"])
        
    with calc_type[0]:
        if st.button("Differentiate Function", use_container_width=True, type="primary"):
            try:
                expr = sp.sympify(clean_math_input(calc_expr))
                result = sp.diff(expr, x)
                
                st.session_state.history_log.append({
                    "module": "Derivative",
                    "input": f"d/dx ({calc_expr})",
                    "output": str(result)
                })
                
                with st.container(border=True):
                    st.latex(r"\frac{d}{dx}\left(" + sp.latex(expr) + r"\right) = " + sp.latex(result))
            except Exception as e: st.error(f"Error: {e}")
            
    with calc_type[1]:
        if st.button("Integrate Function", use_container_width=True, type="primary"):
            try:
                expr = sp.sympify(clean_math_input(calc_expr))
                result = sp.integrate(expr, x)
                
                st.session_state.history_log.append({
                    "module": "Integral",
                    "input": f"∫ ({calc_expr}) dx",
                    "output": str(result)
                })
                
                with st.container(border=True):
                    st.latex(r"\int \left(" + sp.latex(expr) + r"\right) dx = " + sp.latex(result) + r" + C")
            except Exception as e: st.error(f"Error: {e}")

# --- 4. MATRIX STUDIO ---
elif operation_type == "📊 ATS Matrix Studio":
    st.subheader("ATS Matrix Laboratory")
    
    with st.container(border=True):
        matrix_str = st.text_area("Matrix Element Allocation (Spaces separate columns, rows split via newlines):", "1 2\n3 4")
        matrix_op = st.selectbox("Linear Algebra Calculations Available:", ["Determinant", "Inverse Matrix", "Matrix Transposition"])
        submit = st.button("Compute Linear Algebraic State", use_container_width=True, type="primary")
        
    if submit:
        try:
            raw_matrix = [list(map(float, row.split())) for row in matrix_str.strip().split('\n')]
            M = sp.Matrix(raw_matrix)
            
            st.markdown("### Processed Matrix Structural Matrix ($M$)")
            with st.container(border=True):
                st.latex(sp.latex(M))
            
            st.markdown("### Result Execution Matrix Output")
            with st.container(border=True):
                if matrix_op == "Determinant":
                    res_val = str(M.det())
                    st.metric("Matrix Determinant |M|", res_val)
                elif matrix_op == "Inverse Matrix":
                    res_val = str(M.inv())
                    st.latex(sp.latex(M.inv()))
                elif matrix_op == "Matrix Transposition":
                    res_val = str(M.T)
                    st.latex(sp.latex(M.T))
                    
            st.session_state.history_log.append({
                "module": matrix_op,
                "input": "Matrix input",
                "output": res_val
            })
        except Exception as e:
            st.error(f"Computation Dimension/Determinant Context Error: {e}")

# --- 5. VECTOR GRAPHER ---
elif operation_type == "🔮 ATS Vector Grapher":
    st.subheader("ATS Dynamic Functional Grapher")
    
    with st.container(border=True):
        graph_expr_str = st.text_input("Target Equation Curve $f(x)$:", "x^3 - 4x")
        x_min, x_max = st.slider("X-Axis Boundaries Domain Range Slider", -100, 100, (-10, 10))
        submit = st.button("Generate System Plots", use_container_width=True, type="primary")
        
    if submit:
        try:
            expr = sp.sympify(clean_math_input(graph_expr_str))
            f_num = sp.lambdify(x, expr, "numpy")
            
            x_vals = np.linspace(x_min, x_max, 500)
            y_vals = f_num(x_vals)
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x_vals, y_vals, label=f"$y = {sp.latex(expr)}$", color="#FF4B4B", lw=2.5)
            ax.axhline(0, color='black', lw=0.8, ls='-')
            ax.axvline(0, color='black', lw=0.8, ls='-')
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend()
            
            with st.container(border=True):
                st.pyplot(fig)
                
            st.session_state.history_log.append({
                "module": "Grapher",
                "input": graph_expr_str,
                "output": "Plot Rendered"
            })
        except Exception as e:
            st.error(f"Plot Render Error Exception: {e}")