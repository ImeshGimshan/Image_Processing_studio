import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import streamlit as st
from PIL import Image as PILImage

import styles
from image_processor import (
    load_image_as_gray,
    load_image_for_display,
    apply_sharpening,
    apply_denoising,
)

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Image Processing Studio",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>◈</text></svg>",
    layout="wide",
    initial_sidebar_state="expanded",
)
styles.inject_css()
styles.hero()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    styles.sidebar_logo()

    styles.sb_label("Input")
    uploaded_file = st.file_uploader(
        "Upload Image", type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
    )

    styles.sb_label("Operation", margin_top=True)
    operation = st.radio(
        "Operation",
        ["Sharpen (Matrix Inverse)", "Denoise (Conjugate Gradient)"],
        label_visibility="collapsed",
    )
    styles.sb_algorithm_card(operation)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    run_btn = st.button("Run Processing", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown(
        '<p style="color:#475569;font-size:0.8rem;text-align:center">NumPy · PIL · Streamlit</p>',
        unsafe_allow_html=True,
    )

# ── Guard: no image uploaded ──────────────────────────────────────────────────
if uploaded_file is None:
    styles.upload_prompt()
    st.stop()

# ── Load image at two resolutions ─────────────────────────────────────────────
display_image = load_image_for_display(uploaded_file)   # native res (≤512px)
uploaded_file.seek(0)
image_array = load_image_as_gray(uploaded_file)          # 128×128 for processing

# ── Main columns ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")
with col1:
    styles.img_frame(display_image, variant="a", label="Original Image")

if not run_btn:
    with col2:
        styles.ready_box()
    st.stop()

# ── Processing ────────────────────────────────────────────────────────────────
with st.spinner("Processing — please wait…"):

    # ── 1. Sharpen (Matrix Inverse) ───────────────────────────────────────────
    if operation == "Sharpen (Matrix Inverse)":
        result, blur_matrix, inv_matrix = apply_sharpening(display_image)

        with col2:
            styles.img_frame(result, variant="b", label="Sharpened")

        styles.section_header("Matrix Inverse — Gauss-Jordan Elimination", dot="purple")

        mc1, mc2, mc3 = st.columns(3, gap="medium")
        with mc1:
            styles.math_header("Step 1 — Define", "Blur Matrix (A)")
            st.dataframe({f"col{i}": blur_matrix[:, i].round(4) for i in range(3)},
                         use_container_width=True, hide_index=False)
        with mc2:
            styles.math_header("Step 2 — Invert", "Inverse Filter (A⁻¹)")
            st.dataframe({f"col{i}": inv_matrix[:, i].round(4) for i in range(3)},
                         use_container_width=True, hide_index=False)
        with mc3:
            product = np.round(blur_matrix @ inv_matrix, 2)
            styles.math_header("Step 3 — Verify", "A × A⁻¹ = I")
            st.dataframe({f"col{i}": product[:, i] for i in range(3)},
                         use_container_width=True, hide_index=False)

        styles.ok_strip("Sharpening applied via Gauss-Jordan Elimination")

    # ── 2. Denoise (Conjugate Gradient) ──────────────────────────────────────
    elif operation == "Denoise (Conjugate Gradient)":

        # Downscale to max 256px for CG processing, then upscale result
        disp_h, disp_w = display_image.shape
        scale  = min(1.0, 256 / max(disp_h, disp_w))
        proc_h = max(1, int(disp_h * scale))
        proc_w = max(1, int(disp_w * scale))

        proc_arr = (
            np.array(
                PILImage.fromarray((display_image * 255).astype(np.uint8))
                        .resize((proc_w, proc_h), PILImage.LANCZOS),
                dtype=float,
            ) / 255.0
        )

        denoised, noisy, history = apply_denoising(proc_arr)

        def upscale(arr):
            return (
                np.array(
                    PILImage.fromarray((arr * 255).astype(np.uint8))
                            .resize((disp_w, disp_h), PILImage.LANCZOS),
                    dtype=float,
                ) / 255.0
            )

        noisy_display  = upscale(noisy)
        result_display = upscale(denoised)

        with col2:
            styles.img_frame(result_display, variant="b", label="Denoised")

        # Side-by-side comparison
        styles.section_header("Side-by-Side Comparison", dot="cyan")
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            styles.img_frame(display_image, variant="a", label="Original")
        with c2:
            styles.img_label('Noisy Input &nbsp;<span style="font-weight:400;color:#64748b">(σ = 0.05)</span>', variant="c")
            st.markdown('<div class="img-frame">', unsafe_allow_html=True)
            st.image(noisy_display, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            styles.img_frame(result_display, variant="b", label="CG Denoised")

        # Convergence chart
        styles.section_header("Conjugate Gradient — Convergence", dot="green")

        ks    = [h["k"]             for h in history]
        norms = [h["residual_norm"] for h in history]

        matplotlib.rcParams.update(styles.PLOT_STYLE)
        fig, ax = plt.subplots(figsize=(9, 3.2))
        ax.semilogy(ks, norms, color="#6366f1", linewidth=2.0, zorder=3)
        ax.fill_between(ks, norms, alpha=0.1, color="#6366f1")
        ax.scatter(ks, norms, color="#818cf8", s=22, zorder=5, edgecolors="none")
        ax.set_xlabel("Iteration  k", fontsize=10)
        ax.set_ylabel("Residual norm  ‖r‖", fontsize=10)
        ax.set_title("Residual Norm vs. Iteration Number", fontsize=11,
                     fontweight="bold", color=styles.PLOT_TITLE_COLOR, pad=10)
        ax.grid(True, alpha=0.5)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        styles.metric_pills(len(history), norms[-1], norms[0])
        styles.ok_strip(
            "Denoising complete — Conjugate Gradient solved (I + λL)x = b "
            "with Tikhonov regularisation"
        )