import numpy as np

def conjugate_gradient(A, b, tol=1e-6, max_iter=None):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    if max_iter is None:
        max_iter = n

    x = np.zeros(n)
    r = b - A @ x
    p = r.copy()
    rs_old = r @ r
    history = []

    for k in range(max_iter):
        res_norm = np.sqrt(rs_old)
        history.append({"k": k, "residual_norm": res_norm})

        if res_norm < tol:
            break

        Ap = A @ p
        pAp = p @ Ap
        if abs(pAp) < 1e-15:
            break

        alpha = rs_old / pAp
        x += alpha * p
        r -= alpha * Ap
        rs_new = r @ r
        beta = rs_new / rs_old
        p = r + beta * p
        rs_old = rs_new

    return x, history