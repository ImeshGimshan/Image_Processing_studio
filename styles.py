import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #07080f 0%, #0b0e18 60%, #080c16 100%);
}
[data-testid="stHeader"] { background: transparent; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c0e18 0%, #0a0d1a 100%);
    border-right: 1px solid rgba(99,102,241,0.15);
}

/* Hero */
.hero {
    background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(139,92,246,0.08) 50%, rgba(6,182,212,0.07) 100%);
    border: 1px solid rgba(99,102,241,0.22);
    border-radius: 18px; padding: 2.8rem 2.4rem 2.4rem;
    margin-bottom: 1.8rem; position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -60%; left: -5%;
    width: 45%; height: 220%;
    background: radial-gradient(ellipse, rgba(99,102,241,0.1) 0%, transparent 65%);
    pointer-events: none;
}
.hero::after {
    content: ''; position: absolute; top: -40%; right: -5%;
    width: 38%; height: 200%;
    background: radial-gradient(ellipse, rgba(6,182,212,0.07) 0%, transparent 65%);
    pointer-events: none;
}
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: rgba(99,102,241,0.18); border: 1px solid rgba(99,102,241,0.35);
    border-radius: 999px; padding: 0.3rem 1rem;
    font-size: 0.82rem; font-weight: 700; color: #ddd6fe;
    letter-spacing: 0.09em; text-transform: uppercase; margin-bottom: 1rem;
}
.hero-dot  { width: 6px; height: 6px; border-radius: 50%; background: #818cf8; flex-shrink: 0; }
.hero-title {
    font-size: 2.8rem; font-weight: 800; line-height: 1.15;
    background: linear-gradient(135deg, #a78bfa 0%, #818cf8 50%, #38bdf8 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0 0 0.75rem;
}
.hero-sub { color: #cbd5e1; font-size: 1.1rem; font-weight: 400; margin: 0; }

/* Section headings */
.sec-head  { display: flex; align-items: center; gap: 0.75rem; margin: 2rem 0 1.2rem; }
.sec-dot   { width: 10px; height: 10px; border-radius: 3px; flex-shrink: 0; }
.dot-purple { background: linear-gradient(135deg,#6366f1,#8b5cf6); }
.dot-cyan   { background: linear-gradient(135deg,#0ea5e9,#06b6d4); }
.dot-green  { background: linear-gradient(135deg,#10b981,#059669); }
.sec-title  { font-size: 1.25rem; font-weight: 700; color: #f1f5f9; margin: 0; }

/* Image labels */
.img-label { font-size: 0.82rem; font-weight: 700; letter-spacing: 0.08em;
             text-transform: uppercase; margin-bottom: 0.6rem; color: #94a3b8; }
.label-a { color: #a5b4fc; }
.label-b { color: #6ee7b7; }
.label-c { color: #fcd34d; }
.label-d { color: #7dd3fc; }

/* Image frames */
.img-frame {
    border: 1px solid rgba(99,102,241,0.22); border-radius: 12px; overflow: hidden;
    box-shadow: 0 6px 32px rgba(0,0,0,0.5);
    transition: border-color 0.25s, box-shadow 0.25s;
}
.img-frame:hover { border-color: rgba(99,102,241,0.5); box-shadow: 0 10px 40px rgba(99,102,241,0.14); }

/* Upload & ready */
.upload-prompt {
    background: rgba(99,102,241,0.05); border: 1.5px dashed rgba(99,102,241,0.28);
    border-radius: 14px; padding: 3.5rem 2rem; text-align: center;
}
.upload-prompt h4 { color: #a5b4fc; font-size: 1.2rem; margin: 0 0 0.5rem; font-weight: 600; }
.upload-prompt p  { color: #94a3b8; font-size: 1rem; margin: 0; }

.ready-box {
    height: 100%; min-height: 220px; display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    border: 1.5px dashed rgba(99,102,241,0.2); border-radius: 14px;
    padding: 2.5rem; text-align: center;
}
.ready-box p   { margin: 0; }
.ready-box .t1 { color: #a5b4fc; font-weight: 600; font-size: 1rem; }
.ready-box .t2 { color: #94a3b8; font-size: 0.92rem; margin-top: 0.3rem; }

/* Math headers */
.math-step  { font-size: 0.8rem; font-weight: 600; color: #94a3b8;
              text-transform: uppercase; letter-spacing: 0.09em; margin-bottom: 0.3rem; }
.math-title { font-size: 1.05rem; font-weight: 700; color: #ddd6fe; margin-bottom: 0.6rem; }

/* Metric pills */
.metrics { display: flex; gap: 0.8rem; flex-wrap: wrap; margin: 1.1rem 0; }
.mpill {
    background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.22);
    border-radius: 10px; padding: 0.8rem 1.1rem; flex: 1; min-width: 130px;
}
.mpill-label { font-size: 0.76rem; font-weight: 600; color: #94a3b8;
               text-transform: uppercase; letter-spacing: 0.08em; }
.mpill-value { font-size: 1.3rem; font-weight: 700; color: #c4b5fd;
               font-family: 'JetBrains Mono', monospace; margin-top: 0.2rem; }

/* Status strip */
.ok-strip {
    background: rgba(16,185,129,0.09); border: 1px solid rgba(16,185,129,0.28);
    border-radius: 10px; padding: 0.9rem 1.2rem;
    color: #a7f3d0; font-size: 0.97rem; font-weight: 500;
    margin: 1.2rem 0; display: flex; align-items: center; gap: 0.55rem;
}

/* Run button */
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg,#4f46e5,#7c3aed) !important;
    border: none !important; border-radius: 9px !important;
    font-weight: 600 !important; font-size: 0.95rem !important; color: #fff !important;
    box-shadow: 0 3px 18px rgba(79,70,229,0.3) !important; transition: all 0.2s !important;
}
button[data-testid="baseButton-primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 26px rgba(79,70,229,0.45) !important;
}

/* Sidebar */
.sb-label {
    font-size: 0.75rem; font-weight: 700; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.5rem;
    padding-left: 0.65rem; border-left: 2px solid rgba(99,102,241,0.6);
}
.sb-card {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(99,102,241,0.15);
    border-radius: 10px; padding: 1rem 1.1rem; margin: 0.5rem 0;
}
.sb-algo-name { font-size: 0.97rem; font-weight: 700; margin: 0 0 0.35rem; }
.sb-algo-desc { font-size: 0.9rem; color: #94a3b8; margin: 0; line-height: 1.6; }

div[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }
</style>
"""

PLOT_STYLE = {
    "figure.facecolor": "#0a0c14",
    "axes.facecolor":   "#0a0c14",
    "axes.edgecolor":   "#1a1f2e",
    "axes.labelcolor":  "#94a3b8",
    "xtick.color":      "#64748b",
    "ytick.color":      "#64748b",
    "text.color":       "#94a3b8",
    "grid.color":       "#131720",
    "grid.linestyle":   "--",
}
PLOT_TITLE_COLOR = "#cbd5e1"


def inject_css():
    """Inject the dark-theme stylesheet."""
    st.markdown(_CSS, unsafe_allow_html=True)


def hero():
    """Render the gradient hero banner."""
    st.markdown("""
    <div class="hero">
      <div class="hero-eyebrow"><span class="hero-dot"></span>Group 33 &nbsp;·&nbsp; ADMC Assignment</div>
      <h1 class="hero-title">Image Processing Studio</h1>
      <p class="hero-sub">Matrix Inverse &amp; Conjugate Gradient — Applied Linear Algebra in Practice</p>
    </div>
    """, unsafe_allow_html=True)


def upload_prompt():
    """Render the 'no file uploaded' prompt."""
    st.markdown("""
    <div class="upload-prompt">
      <h4>Upload an image to get started</h4>
      <p>Supports PNG, JPG, JPEG &nbsp;·&nbsp; Converted to grayscale automatically</p>
    </div>
    """, unsafe_allow_html=True)


def ready_box():
    """Render the 'ready to process' placeholder in col2."""
    st.markdown("""
    <div class="ready-box">
      <p class="t1">Ready to process</p>
      <p class="t2">Press <b style="color:#818cf8">Run Processing</b> to begin</p>
    </div>
    """, unsafe_allow_html=True)


def sidebar_logo():
    """Render the IPS logo and subtitle."""
    st.markdown("""
    <div style="margin-bottom:1.4rem">
      <div style="font-size:1.4rem;font-weight:800;
                  background:linear-gradient(135deg,#a78bfa,#38bdf8);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  background-clip:text;">IPS</div>
      <div style="font-size:0.85rem;color:#64748b;margin-top:0.15rem">Image Processing Studio</div>
    </div>
    """, unsafe_allow_html=True)


def sb_label(text, margin_top=False):
    """Render a sidebar section label."""
    style = ' style="margin-top:1.2rem"' if margin_top else ""
    st.markdown(f'<div class="sb-label"{style}>{text}</div>', unsafe_allow_html=True)


def sb_algorithm_card(operation):
    """Render the algorithm info card based on selected operation."""
    if operation == "Sharpen (Matrix Inverse)":
        st.markdown("""
        <div class="sb-card">
          <div class="sb-label">Algorithm</div>
          <p class="sb-algo-name" style="color:#a5b4fc">Gauss-Jordan Elimination</p>
          <p class="sb-algo-desc">Computes A⁻¹ to reverse blur, then applies unsharp masking to enhance edges.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sb-card">
          <div class="sb-label">Algorithm</div>
          <p class="sb-algo-name" style="color:#7dd3fc">Conjugate Gradient Method</p>
          <p class="sb-algo-desc">Solves (I + λL)x = b iteratively. Tikhonov regularisation with Neumann boundary conditions.</p>
        </div>
        """, unsafe_allow_html=True)


def img_label(text, variant="a"):
    """Render a colour-coded image label (variant: a/b/c/d)."""
    st.markdown(f'<p class="img-label label-{variant}">{text}</p>', unsafe_allow_html=True)


def img_frame(image, variant="a", label=None):
    """Render an image inside a styled frame, with an optional label above it."""
    if label:
        img_label(label, variant)
    st.markdown('<div class="img-frame">', unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def section_header(title, dot="purple"):
    """Render a coloured-dot section heading."""
    st.markdown(f"""
    <div class="sec-head">
      <div class="sec-dot dot-{dot}"></div>
      <h2 class="sec-title">{title}</h2>
    </div>
    """, unsafe_allow_html=True)


def math_header(step, title):
    """Render a two-line math step label above a dataframe."""
    st.markdown(
        f'<div class="math-step">{step}</div>'
        f'<div class="math-title">{title}</div>',
        unsafe_allow_html=True,
    )


def ok_strip(text):
    """Render a green success confirmation strip."""
    st.markdown(f"""
    <div class="ok-strip">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <circle cx="8" cy="8" r="7" stroke="#10b981" stroke-width="1.5"/>
        <path d="M5 8l2 2 4-4" stroke="#10b981" stroke-width="1.5"
              stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      {text}
    </div>
    """, unsafe_allow_html=True)


def metric_pills(total_iter, final_res, initial_res):
    """Render four CG convergence metric pills."""
    factor = initial_res / max(final_res, 1e-15)
    st.markdown(f"""
    <div class="metrics">
      <div class="mpill">
        <div class="mpill-label">Total Iterations</div>
        <div class="mpill-value">{total_iter}</div>
      </div>
      <div class="mpill">
        <div class="mpill-label">Final Residual</div>
        <div class="mpill-value">{final_res:.2e}</div>
      </div>
      <div class="mpill">
        <div class="mpill-label">Initial Residual</div>
        <div class="mpill-value">{initial_res:.2e}</div>
      </div>
      <div class="mpill">
        <div class="mpill-label">Reduction Factor</div>
        <div class="mpill-value">{factor:.1e}x</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
