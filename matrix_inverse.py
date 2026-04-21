import numpy as np

def matrix_inverse_gauss_jordan(matrix):
    """
    Compute the inverse of a matrix using Gauss-Jordan Elimination.
    Returns the inverse as a numpy array, or None if singular.
    """
    matrix = np.array(matrix, dtype=float)
    n = len(matrix)

    # Build augmented matrix [A | I]
    aug = np.hstack([matrix.copy(), np.eye(n)])

    for col in range(n):
        # Find pivot row (largest absolute value in this column)
        max_row = np.argmax(np.abs(aug[col:, col])) + col

        # Check for singular matrix
        if abs(aug[max_row, col]) < 1e-10:
            return None  # Singular

        # Swap rows
        if max_row != col:
            aug[[col, max_row]] = aug[[max_row, col]]

        # Scale pivot row so pivot = 1
        pivot = aug[col, col]
        aug[col] = aug[col] / pivot

        # Eliminate all other rows in this column
        for row in range(n):
            if row != col:
                factor = aug[row, col]
                aug[row] = aug[row] - factor * aug[col]

    # Right half is the inverse
    return aug[:, n:]