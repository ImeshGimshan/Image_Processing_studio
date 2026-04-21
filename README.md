# Image Processing Studio

> **ADMC Assignment — Group 33**  
> Applied Linear Algebra in Practice: Matrix Inverse & Conjugate Gradient Method

A professional-grade, interactive image processing application built with **Streamlit**, demonstrating two fundamental linear algebra algorithms — **Gauss-Jordan Matrix Inversion** (for image sharpening) and the **Conjugate Gradient Method** (for image denoising) — applied directly to real images.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Installation & Setup](#installation--setup)
5. [Running the Application](#running-the-application)
6. [How to Use the App](#how-to-use-the-app)
7. [Mathematics — Matrix Inverse (Gauss-Jordan)](#mathematics--matrix-inverse-gauss-jordan)
8. [Mathematics — Conjugate Gradient Method](#mathematics--conjugate-gradient-method)
9. [Code Architecture](#code-architecture)
10. [Troubleshooting](#troubleshooting)

---

## Features

| Feature | Description |
|---|---|
| **Image Upload** | Upload PNG, JPG, or JPEG images |
| **Sharpen (Matrix Inverse)** | Edge enhancement via Gauss-Jordan matrix inversion |
| **Denoise (Conjugate Gradient)** | Noise removal via Tikhonov regularisation solved with CG |
| **Live Math Visualisation** | Blur matrix, inverse matrix, and identity verification displayed in-app |
| **Convergence Plot** | Residual norm vs. iteration number charted in real-time |
| **Dark Glassmorphism UI** | Premium dark-mode interface with animated gradients |

---

## Project Structure

```
image_processing_studio/
│
├── app.py                  # Main Streamlit application (UI layout & orchestration)
├── image_processor.py      # Image loading, sharpening, and denoising pipelines
├── matrix_inverse.py       # Gauss-Jordan matrix inversion (pure NumPy, from scratch)
├── conjugate_gradient.py   # Conjugate Gradient solver (pure NumPy, from scratch)
├── styles.py               # All CSS, HTML components, and Matplotlib theme
│
├── requirements.txt        # Python dependencies
├── .streamlit/             # Streamlit configuration (theme, server settings)
├── .devcontainer/          # VS Code Dev Container configuration
└── README.md               # This file
```

### Module Responsibilities

| File | Responsibility |
|---|---|
| `app.py` | Page config, sidebar controls, column layout, calls processors |
| `image_processor.py` | `load_image_*`, `apply_sharpening`, `apply_denoising` — pure logic |
| `matrix_inverse.py` | `matrix_inverse_gauss_jordan(matrix)` — standalone solver |
| `conjugate_gradient.py` | `conjugate_gradient(A, b, tol, max_iter)` — standalone solver |
| `styles.py` | CSS injection, hero banner, image frames, metric pills, plot theme |

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | ≥ 3.9 |
| pip | Latest recommended |
| Internet connection | Required on first run (Google Fonts CDN) |

---

## Installation & Setup

### Step 1 — Clone or Download the Repository

```bash
# Option A — Git clone
git clone https://github.com/ImeshGimshan/Image_Processing_studio.git
cd image_processing_studio

# Option B — Download ZIP and extract, then open a terminal in the folder
cd image_processing_studio
```

### Step 2 — Create a Virtual Environment (Recommended)

Using a virtual environment keeps your global Python installation clean.

**Windows (Gitbash)**
```powershell
python -m venv venv
source venv/Scripts/activate
```

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

> You should see `(venv)` prepended to your terminal prompt after activation.

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the four libraries the app depends on:

| Library | Purpose |
|---|---|
| `streamlit` | Interactive web UI framework |
| `numpy` | N-dimensional array maths (matrix ops, linear algebra) |
| `pillow` | Image loading, resizing, format conversion |
| `matplotlib` | Convergence plot rendering |

---

## Running the Application

```bash
streamlit run app.py
```

Streamlit will print two URLs:

```
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open **http://localhost:8501** in your browser. The app loads instantly.

### Stopping the Server

Press `Ctrl + C` in the terminal where Streamlit is running.

---

## How to Use the App

1. **Upload an image** — Click *Browse files* in the left sidebar. Supports PNG, JPG, JPEG. The image is automatically converted to **grayscale**.

2. **Select an operation** — Choose between:
   - **Sharpen (Matrix Inverse)** — enhances edges using matrix inversion
   - **Denoise (Conjugate Gradient)** — removes Gaussian noise iteratively

3. **Click "Run Processing"** — The algorithm runs and results appear on the right.

4. **Inspect the mathematics** — Scroll down to see:
   - For sharpening: the blur matrix **A**, its computed inverse **A⁻¹**, and the verification **A × A⁻¹ = I**
   - For denoising: a side-by-side comparison (original / noisy / denoised) and a convergence plot

---

## Mathematics — Matrix Inverse (Gauss-Jordan)

### 1. Overview

Image sharpening is implemented as **unsharp masking** driven by a matrix inverse. The inverse is computed from scratch using **Gauss-Jordan Elimination** — no `numpy.linalg.inv` is used in the main path.

### 2. The Blur Matrix A

A 3×3 weighted blur kernel is defined:

$$
A = \begin{bmatrix} 1 & 2 & 1 \\ 2 & 5 & 2 \\ 1 & 2 & 2 \end{bmatrix}
$$

This matrix is **full-rank** (`det(A) ≠ 0`), ensuring its inverse exists.

### 3. Gauss-Jordan Elimination Algorithm

The algorithm computes **A⁻¹** without using any built-in inverse function.

**Core idea:** Augment A with the identity matrix I to form [A | I], then apply row operations until the left half becomes I. At that point the right half is A⁻¹.

$$
[A \mid I] \xrightarrow{\text{row ops}} [I \mid A^{-1}]
$$

**Step-by-step:**

**Step 1 — Build the augmented matrix:**
```
aug = [A | I]  →  a (n × 2n) matrix
```

**Step 2 — For each column `col` from 0 to n-1:**

  a. **Partial Pivoting** — Find the row with the largest absolute value in column `col` (at or below the diagonal). Swap it to position `col`. This prevents division by near-zero values and improves numerical stability.

  $$
  \text{pivot\_row} = \arg\max_{i \geq \text{col}} |A_{i,\text{col}}|
  $$

  b. **Singularity Check** — If the pivot element is effectively zero (< 1e-10), the matrix is singular (non-invertible). Return `None`.

  c. **Normalise the pivot row** — Divide the entire row by the pivot value so the diagonal element becomes 1:

  $$
  R_{\text{col}} \leftarrow \frac{R_{\text{col}}}{A_{\text{col},\text{col}}}
  $$

  d. **Eliminate all other rows** — For every row `row ≠ col`, subtract the appropriate multiple of the pivot row to zero out the column `col`:

  $$
  R_{\text{row}} \leftarrow R_{\text{row}} - A_{\text{row},\text{col}} \cdot R_{\text{col}}
  $$

**Step 3 — Extract the inverse:**
```
A_inv = aug[:, n:]   # right half is now A⁻¹
```

**Verification (shown in-app):**
$$
A \times A^{-1} = I \quad \checkmark
$$

### 4. Applying Sharpening (Unsharp Masking)

Once A⁻¹ is found, the pipeline continues:

**Step 3 — Blur the image:**
The normalised kernel `K = A / sum(A)` is applied as a 2D convolution using vectorised NumPy (zero Python loops):

```python
blur_kernel = blur_matrix / blur_matrix.sum()
# Vectorised convolution on padded image array
blurred = (
    blur_kernel[0,0]*pad[:-2, :-2] + blur_kernel[0,1]*pad[:-2, 1:-1] + ...
)
```

**Step 4 — Unsharp Masking:**

$$
\text{sharpened} = \text{original} + \alpha \times (\text{original} - \text{blurred})
$$

where `α = 1.5` (sharpening strength). The term `(original − blurred)` isolates high-frequency details (edges). Adding it back amplifies those edges, making the image visibly sharper.

**Why use matrix inverse for sharpening?**  
The blur operation is modelled as a linear system `b = Ax` (blurred = A × original). To recover `x` (sharper version) from `b`, we compute `x = A⁻¹ b`. The unsharp masking step is the practical approximation of this inverse filter applied pixel-by-pixel.

---

## Mathematics — Conjugate Gradient Method

### 1. Overview

Image denoising is cast as a **regularised least-squares problem** solved iteratively with the **Conjugate Gradient (CG) Method**. CG is an efficient iterative solver for large symmetric positive-definite (SPD) linear systems.

### 2. The Denoising Problem (Tikhonov Regularisation)

Given a noisy image `b`, we want a clean image `x` that:
- Stays close to the noisy input: `‖x − b‖²` (data fidelity)
- Is spatially smooth: `‖Dx‖²` where D measures pixel differences (regularisation)

This is a **Tikhonov regularisation** problem:

$$
\min_x \; \|x - b\|^2 + \lambda \|Dx\|^2
$$

Taking the derivative and setting it to zero gives a linear system:

$$
(I + \lambda L)\,x = b
$$

where:
- **I** is the identity matrix
- **L** is the discrete **Laplacian** (second-difference) matrix, encoding spatial smoothness
- **λ = 0.8** is the regularisation parameter (larger = smoother result)
- **b** is the noisy signal (a row or column of the image)

### 3. The Laplacian Matrix L

For a 1D signal of length n, L captures the second-order finite difference (Neumann boundary conditions):

$$
L = \begin{bmatrix}
 1 & -1 &  0 & \cdots \\
-1 &  2 & -1 & \cdots \\
 0 & -1 &  2 & \cdots \\
\vdots & & & \ddots
\end{bmatrix}
$$

**Neumann boundary conditions** set `L[0,0] = L[n-1,n-1] = 1` (instead of 2), meaning there is no "outside" flux — the signal does not bleed past the image edge.

The system matrix `A = I + λL` is:
- **Symmetric** (`A = Aᵀ`)
- **Positive definite** (all eigenvalues > 0)
- **Sparse** (tridiagonal structure)

These three properties make it an ideal candidate for the Conjugate Gradient Method.

### 4. Conjugate Gradient Algorithm (Pure Implementation)

The CG method finds the exact solution of `Ax = b` for an SPD matrix in at most **n iterations**, but usually converges far faster in practice.

**Initialization:**
```
x₀ = 0          (initial guess: zero vector)
r₀ = b − A·x₀  = b    (initial residual)
p₀ = r₀         (initial search direction)
```

**Iteration k = 0, 1, 2, …:**

1. **Step size** along search direction `p`:

$$
\alpha_k = \frac{r_k^T r_k}{p_k^T A\, p_k}
$$

2. **Update solution:**

$$
x_{k+1} = x_k + \alpha_k\, p_k
$$

3. **Update residual** (how far the current solution is from exact):

$$
r_{k+1} = r_k - \alpha_k\, A\, p_k
$$

4. **Compute conjugation coefficient** β (ensures new direction is A-conjugate to all previous directions):

$$
\beta_k = \frac{r_{k+1}^T r_{k+1}}{r_k^T r_k}
$$

5. **Update search direction** (conjugate to all previous directions):

$$
p_{k+1} = r_{k+1} + \beta_k\, p_k
$$

**Stopping condition:**

$$
\|r_k\| = \sqrt{r_k^T r_k} < \text{tol} \quad (\text{tol} = 10^{-4})
$$

**A-conjugacy** (why it's efficient): Two vectors u, v are **A-conjugate** if `uᵀAv = 0`. CG generates a set of mutually A-conjugate search directions, meaning each iteration explores a completely new dimension of the solution space. This guarantees convergence in at most n steps, compared to potentially many more for gradient descent.

### 5. 2D Denoising (Separable Passes)

The CG solver works on 1D signals. To extend this to 2D images, the denoising is applied in **two separable passes**:

```
Pass 1 — Along rows:
  For each row i:   solve (I + λ·L_col) · x = noisy_row_i

Pass 2 — Along columns:
  For each column j:  solve (I + λ·L_row) · x = smoothed_col_j
```

This separable approach is equivalent to applying 2D Tikhonov regularisation along both spatial axes independently, making the smoothing **isotropic** (equal in all directions) while keeping computation manageable.

**Complexity:**
- Per 1D CG solve: **O(n·k)** where k << n (far fewer iterations than signal length)
- Total: **O((n_rows × n_cols) · n · k)** — efficient for moderate image sizes

### 6. Convergence Metrics (shown in-app)

| Metric | Meaning |
|---|---|
| **Total Iterations** | How many CG steps were needed |
| **Initial Residual ‖r₀‖** | Error magnitude before solving |
| **Final Residual ‖r_k‖** | Remaining error after convergence |
| **Reduction Factor** | `‖r₀‖ / ‖r_k‖` — how much the error shrank |

The **convergence plot** shows `‖r_k‖` on a log scale vs. iteration number, demonstrating the superlinear convergence characteristic of CG.

---

## Code Architecture

```
User uploads image
        │
        ▼
   app.py (UI)
   ├── load_image_for_display()    ─┐
   │   (native res, max 512px)     │  image_processor.py
   ├── load_image_as_gray()        │
   │   (128×128 for processing)   ─┘
   │
   ├── [Sharpen path]
   │   └── apply_sharpening(image_array)
   │         ├── matrix_inverse_gauss_jordan(blur_matrix)  ← matrix_inverse.py
   │         └── vectorised convolution + unsharp masking
   │
   └── [Denoise path]
         └── apply_denoising(image_array)
               ├── Add Gaussian noise (σ = 0.05, seed 42)
               ├── build_A(n)  →  (I + λL) for rows & columns
               ├── Pass 1: CG solve per row  ─┐
               └── Pass 2: CG solve per col  ─┘  conjugate_gradient.py
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'streamlit'`
You are running outside the virtual environment. Activate it first:
```powershell
.\venv\Scripts\Activate.ps1   # Windows PowerShell
```

### Port 8501 already in use
Run on a different port:
```bash
streamlit run app.py --server.port 8502
```

### Streamlit opens but shows a blank page
Hard-refresh the browser (`Ctrl + Shift + R` on Windows). If the problem persists, stop and restart the Streamlit server.

### Processing is slow on large images
The app automatically downscales images to **max 256 px** before CG processing and **max 512 px** for display, so processing should remain fast. If you upload a very large image (e.g., 4K), the initial loading step may take a moment.

### Image appears too dark / too bright after sharpening
This is normal for high-contrast images. The unsharp masking strength is set to `α = 1.5`. Pixel values are clipped to [0, 1] to prevent overflow.

---

## Dependencies

```
streamlit       # Web UI framework
numpy           # Numerical computing (arrays, matrix ops)
pillow          # Image I/O and resizing
matplotlib      # Convergence chart rendering
```

---

## Academic Context

This project is a submission for **Group 33, ADMC Assignment** demonstrating applied numerical linear algebra:

| Concept | Application |
|---|---|
| Matrix Inversion | Reversing a blur kernel to sharpen images |
| Gauss-Jordan Elimination | Computing the matrix inverse from scratch |
| Tikhonov Regularisation | Formulating denoising as a least-squares problem |
| Conjugate Gradient Method | Efficiently solving the resulting SPD linear system |
| Neumann Boundary Conditions | Preventing edge artefacts in the Laplacian operator |
| Unsharp Masking | Practical image sharpening using the inverse filter concept |

---

*Built with Python · NumPy · Pillow · Streamlit · Matplotlib*
