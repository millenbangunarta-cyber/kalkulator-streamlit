import streamlit as st
import ast, operator as op

st.set_page_config(page_title="Kalkulator Streamlit", page_icon="🧮", layout="centered")

# ====== CSS Background + Warna Tulisan ======
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    color: black; /* warna teks default */
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
[data-testid="stToolbar"] {
    right: 2rem;
}
h1, h2, h3, h4, h5, h6, p, div, span, label {
    color: black !important; /* pastikan semua teks jadi hitam */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ====== Judul ======
st.title("🧮 Kalkulator Sederhana")

# Operator yang diizinkan
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def safe_eval(node):
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        return operators[type(node.op)](safe_eval(node.left), safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return operators[type(node.op)](safe_eval(node.operand))
    raise ValueError("Ekspresi tidak valid atau operator tidak diizinkan.")

def evaluate(expr):
    try:
        tree = ast.parse(expr, mode="eval")
        return safe_eval(tree)
    except Exception as e:
        return f"ERROR: {e}"

expr = st.text_input("Masukkan ekspresi matematika:", value="2+3")

if st.button("Hitung"):
    result = evaluate(expr)
    st.success(f"Hasil: {result}")
