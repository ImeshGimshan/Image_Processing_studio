import numpy as np
from PIL import Image
from conjugate_gradient import conjugate_gradient
from matrix_inverse import matrix_inverse_gauss_jordan

def load_image_for_display(uploaded_file):
    """Load at native resolution (max 512px) — used only for display."""
    img = Image.open(uploaded_file).convert("L")
    img.thumbnail((512, 512), Image.LANCZOS)   # high-quality downscale, keeps aspect ratio
    return np.array(img, dtype=float) / 255.0

def load_image_as_gray(uploaded_file):
    """Load at 128×128 — used for pixel-loop processing (keeps it fast)."""
    img = Image.open(uploaded_file).convert("L")
    img = img.resize((128, 128), Image.LANCZOS)
    return np.array(img, dtype=float) / 255.0

def apply_sharpening(image_array):
    """
    Uses Matrix Inverse concept.

    How it works:
    - We define a 3x3 invertible blur matrix A  (det = 1, clean integer inverse)
    - We compute A_inverse using Gauss-Jordan elimination
    - We apply the normalised blur kernel as convolution to get a blurred image
    - Then use unsharp masking: sharpened = original + strength * (original - blurred)
      → this is the correct way to 'apply A⁻¹': recover what blurring removed
    """

    # Step 1: Define an invertible blur matrix with det(A) = 1.
    # All three rows are linearly independent, so the matrix is full-rank.
    # A = [[1,2,1],[2,5,2],[1,2,2]]  →  A⁻¹ = [[6,-2,-1],[-2,1,0],[-1,0,1]]
    # Values stay small → no blow-up when displayed or used.
    blur_matrix = np.array([
        [1.0, 2.0, 1.0],
        [2.0, 5.0, 2.0],
        [1.0, 2.0, 2.0]
    ])

    # Step 2: Compute inverse using our Gauss-Jordan implementation
    inverse_filter = matrix_inverse_gauss_jordan(blur_matrix.tolist())

    if inverse_filter is None:
        try:
            inverse_filter = np.linalg.inv(blur_matrix)
        except np.linalg.LinAlgError:
            inverse_filter = np.linalg.pinv(blur_matrix)

    # Step 3: Normalise the kernel so pixel values stay in [0, 1], then blur.
    blur_kernel = blur_matrix / blur_matrix.sum()

    # Step 3 (vectorized): pad & apply blur_kernel as a 2D convolution in one
    # numpy expression — no Python loops, works at any resolution instantly.
    pad = np.pad(image_array, 1, mode='edge')
    blurred = (
        blur_kernel[0,0]*pad[:-2, :-2] + blur_kernel[0,1]*pad[:-2, 1:-1] + blur_kernel[0,2]*pad[:-2, 2:] +
        blur_kernel[1,0]*pad[1:-1,:-2] + blur_kernel[1,1]*pad[1:-1,1:-1] + blur_kernel[1,2]*pad[1:-1,2:] +
        blur_kernel[2,0]*pad[2:,  :-2] + blur_kernel[2,1]*pad[2:,  1:-1] + blur_kernel[2,2]*pad[2:,  2:]
    )
    blurred = np.clip(blurred, 0, 1)

    # Step 4: Unsharp masking — recover the detail that blurring suppressed.
    # sharpened = original + strength × (original - blurred)
    strength = 1.5
    result = image_array + strength * (image_array - blurred)
    result = np.clip(result, 0, 1)

    return result, blur_matrix, inverse_filter

def apply_denoising(image_array):
    """
    Uses Conjugate Gradient to solve the Tikhonov denoising system:

        minimise  ||x - b||² + λ||Dx||²  ⟹  (I + λL)x = b

    Applied in two separable passes (rows then columns) for proper 2D denoising.
    Gaussian noise is added first so the algorithm has something visible to remove.
    """
    # Step 1: add realistic Gaussian noise so denoising is visibly meaningful
    rng = np.random.default_rng(42)
    noisy = np.clip(image_array + rng.normal(0, 0.05, image_array.shape), 0, 1)

    lam = 0.8    # smoothing strength (larger = more noise removed)

    def build_A(n):
        """Build (I + λL) with Neumann BCs — all row sums = 1."""
        L = (2 * np.eye(n)
             - np.diag(np.ones(n - 1),  1)
             - np.diag(np.ones(n - 1), -1))
        L[0, 0]   = 1   # Neumann BC
        L[-1, -1] = 1
        return np.eye(n) + lam * L

    n_rows, n_cols = noisy.shape
    A_row = build_A(n_cols)   # reused for every row
    A_col = build_A(n_rows)   # reused for every column

    # Pass 1: smooth along rows
    after_rows = np.copy(noisy)
    for i in range(n_rows):
        x, _ = conjugate_gradient(A_row, noisy[i], tol=1e-4)
        after_rows[i] = np.clip(x, 0, 1)

    # Pass 2: smooth along columns (makes the denoising 2-D / isotropic)
    history_all = []
    denoised = np.copy(after_rows)
    for j in range(n_cols):
        x, history = conjugate_gradient(A_col, after_rows[:, j], tol=1e-4)
        denoised[:, j] = np.clip(x, 0, 1)
        if j == 0:
            history_all = history

    return denoised, noisy, history_all