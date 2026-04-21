import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from image_processor import load_image_as_gray, load_image_for_display, apply_sharpening, apply_denoising

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="Image Processing Studio",
    page_icon="🖼️",
    layout="wide"
)

st.title("🖼️ Image Processing Studio")
st.markdown("**Group 33 | ADMC Assignment** — Matrix Inverse & Conjugate Gradient")
st.divider()

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Controls")
    uploaded_file = st.file_uploader(
        "Upload an Image", type=["png", "jpg", "jpeg"]
    )
    operation = st.radio(
        "Choose Operation",
        ["Sharpen (Matrix Inverse)", "Denoise (Conjugate Gradient)"]
    )
    run_btn = st.button("▶ Run Processing", type="primary")

# ── Main area ─────────────────────────────────────────────
if uploaded_file is None:
    st.info("👈 Upload an image from the sidebar to get started.")
    st.stop()

# Load image — high-res for display, small for processing
display_image = load_image_for_display(uploaded_file)
uploaded_file.seek(0)          # reset stream so it can be read again
image_array = load_image_as_gray(uploaded_file)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📷 Original Image")
    st.image(display_image, width=300)

if run_btn:
    with st.spinner("Processing..."):

        # ── Sharpen ──────────────────────────────────────
        if operation == "Sharpen (Matrix Inverse)":
            result, blur_matrix, inv = apply_sharpening(display_image)  # full-res

            with col2:
                st.subheader("✨ Sharpened Image")
                st.image(result, width=300)

            st.divider()
            st.subheader("🧮 Math Behind It — Matrix Inverse")

            mc1, mc2, mc3 = st.columns(3)

            with mc1:
                st.markdown("**Blur Matrix (A)**")
                st.dataframe(
                    {f"col{i}": blur_matrix[:, i].round(4) for i in range(3)},
                    use_container_width=True
                )

            with mc2:
                st.markdown("**Inverse Filter (A⁻¹)**")
                st.dataframe(
                    {f"col{i}": inv[:, i].round(4) for i in range(3)},
                    use_container_width=True
                )

            with mc3:
                product = np.round(blur_matrix @ inv, 4)
                st.markdown("**Verification: A × A⁻¹ = I**")
                st.dataframe(
                    {f"col{i}": product[:, i] for i in range(3)},
                    use_container_width=True
                )

            st.success("✅ Sharpening applied using Gauss-Jordan Elimination!")

        # ── Denoise ──────────────────────────────────────
        elif operation == "Denoise (Conjugate Gradient)":
            from PIL import Image as PILImage
            disp_h, disp_w = display_image.shape

            # Downscale to max 256px for fast CG processing (still 2× sharper than 128px)
            scale   = min(1.0, 256 / max(disp_h, disp_w))
            proc_h  = max(1, int(disp_h * scale))
            proc_w  = max(1, int(disp_w * scale))
            proc_pil = PILImage.fromarray((display_image * 255).astype(np.uint8))
            proc_arr = np.array(proc_pil.resize((proc_w, proc_h), PILImage.LANCZOS), dtype=float) / 255.0

            result, noisy, history = apply_denoising(proc_arr)   # 256px-resolution

            # Upscale both back to the original display size
            def upscale(arr):
                pil = PILImage.fromarray((arr * 255).astype(np.uint8))
                return np.array(pil.resize((disp_w, disp_h), PILImage.LANCZOS), dtype=float) / 255.0

            noisy_display  = upscale(noisy)
            result_display = upscale(result)

            # 3-column comparison: clean → noisy → denoised
            st.divider()
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**📷 Original (clean)**")
                st.image(display_image, use_container_width=True)
            with c2:
                st.markdown("**🔊 Noisy input** *(σ = 0.05)*")
                st.image(noisy_display, use_container_width=True)
            with c3:
                st.markdown("**🧹 CG Denoised**")
                st.image(result_display, use_container_width=True)

            st.divider()
            st.subheader("📈 Conjugate Gradient — Convergence")

            ks    = [h["k"] for h in history]
            norms = [h["residual_norm"] for h in history]

            fig, ax = plt.subplots(figsize=(8, 3))
            ax.semilogy(ks, norms, marker="o", color="#0F6E56",
                        linewidth=2, markersize=4)
            ax.set_xlabel("Iteration k")
            ax.set_ylabel("||r|| (log scale)")
            ax.set_title("Residual Norm vs Iteration")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

            st.metric("Total Iterations", len(history))
            st.metric("Final Residual Norm", f"{norms[-1]:.2e}")
            st.success("✅ Denoising solved using Conjugate Gradient Method!")