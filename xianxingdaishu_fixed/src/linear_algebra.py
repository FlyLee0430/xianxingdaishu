from __future__ import annotations

from math import isclose
from typing import Iterable, List

TOL = 1e-10


class MatrixError(ValueError):
    """矩阵输入或计算错误。"""


Number = float
Matrix = list[list[Number]]
Vector = list[Number]


def _ensure_number(value: object, *, name: str) -> float:
    if isinstance(value, bool):
        raise MatrixError(f"{name} 不能是布尔值")
    if not isinstance(value, (int, float)):
        raise MatrixError(f"{name} 必须是数字")
    return float(value)


def validate_matrix(matrix: object, *, name: str = "matrix") -> Matrix:
    if not isinstance(matrix, list) or not matrix:
        raise MatrixError(f"{name} 必须是非空二维数组")

    normalized: Matrix = []
    row_length: int | None = None

    for i, row in enumerate(matrix):
        if not isinstance(row, list) or not row:
            raise MatrixError(f"{name} 的第 {i + 1} 行必须是非空数组")
        if row_length is None:
            row_length = len(row)
        elif len(row) != row_length:
            raise MatrixError(f"{name} 的每一行长度必须一致")

        normalized_row = [
            _ensure_number(value, name=f"{name}[{i}][{j}]") for j, value in enumerate(row)
        ]
        normalized.append(normalized_row)

    return normalized


def validate_vector(vector: object, *, name: str = "vector") -> Vector:
    if not isinstance(vector, list) or not vector:
        raise MatrixError(f"{name} 必须是非空一维数组")
    return [_ensure_number(value, name=f"{name}[{i}]") for i, value in enumerate(vector)]


def shape(matrix: Matrix) -> tuple[int, int]:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    return rows, cols


def is_square(matrix: Matrix) -> bool:
    rows, cols = shape(matrix)
    return rows == cols


def _normalize_number(value: float, *, tol: float = TOL, digits: int = 10) -> int | float:
    if abs(value) < tol:
        value = 0.0
    rounded = round(value, digits)
    if isclose(rounded, round(rounded), abs_tol=tol):
        return int(round(rounded))
    return rounded


def normalize_matrix(matrix: Matrix, *, tol: float = TOL, digits: int = 10) -> list[list[int | float]]:
    return [[_normalize_number(value, tol=tol, digits=digits) for value in row] for row in matrix]


def normalize_vector(vector: Vector, *, tol: float = TOL, digits: int = 10) -> list[int | float]:
    return [_normalize_number(value, tol=tol, digits=digits) for value in vector]


def transpose(matrix: object) -> list[list[int | float]]:
    m = validate_matrix(matrix)
    return normalize_matrix([list(col) for col in zip(*m)])


def matrix_add(a: object, b: object) -> list[list[int | float]]:
    left = validate_matrix(a, name="a")
    right = validate_matrix(b, name="b")
    if shape(left) != shape(right):
        raise MatrixError("矩阵加法要求两个矩阵形状相同")
    result = [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]
    return normalize_matrix(result)


def matrix_subtract(a: object, b: object) -> list[list[int | float]]:
    left = validate_matrix(a, name="a")
    right = validate_matrix(b, name="b")
    if shape(left) != shape(right):
        raise MatrixError("矩阵减法要求两个矩阵形状相同")
    result = [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]
    return normalize_matrix(result)


def matrix_multiply(a: object, b: object) -> list[list[int | float]]:
    left = validate_matrix(a, name="a")
    right = validate_matrix(b, name="b")
    left_rows, left_cols = shape(left)
    right_rows, right_cols = shape(right)
    if left_cols != right_rows:
        raise MatrixError("矩阵乘法要求 a 的列数等于 b 的行数")

    result: Matrix = []
    for i in range(left_rows):
        row: Vector = []
        for j in range(right_cols):
            value = sum(left[i][k] * right[k][j] for k in range(left_cols))
            row.append(value)
        result.append(row)
    return normalize_matrix(result)


def determinant(matrix: object, *, tol: float = TOL) -> int | float:
    m = validate_matrix(matrix)
    n_rows, n_cols = shape(m)
    if n_rows != n_cols:
        raise MatrixError("行列式只适用于方阵")

    work = [row[:] for row in m]
    det = 1.0
    swap_count = 0

    for col in range(n_cols):
        pivot_row = max(range(col, n_rows), key=lambda r: abs(work[r][col]))
        pivot_value = work[pivot_row][col]
        if abs(pivot_value) < tol:
            return 0

        if pivot_row != col:
            work[col], work[pivot_row] = work[pivot_row], work[col]
            swap_count += 1

        pivot = work[col][col]
        det *= pivot

        for row in range(col + 1, n_rows):
            factor = work[row][col] / pivot
            if abs(factor) < tol:
                continue
            for k in range(col, n_cols):
                work[row][k] -= factor * work[col][k]

    if swap_count % 2 == 1:
        det *= -1

    return _normalize_number(det, tol=tol)


def inverse(matrix: object, *, tol: float = TOL) -> list[list[int | float]]:
    m = validate_matrix(matrix)
    n_rows, n_cols = shape(m)
    if n_rows != n_cols:
        raise MatrixError("只有方阵才能求逆")

    augmented = [
        row[:] + [1.0 if i == j else 0.0 for j in range(n_cols)]
        for i, row in enumerate(m)
    ]

    for col in range(n_cols):
        pivot_row = max(range(col, n_rows), key=lambda r: abs(augmented[r][col]))
        pivot_value = augmented[pivot_row][col]
        if abs(pivot_value) < tol:
            raise MatrixError("矩阵不可逆（行列式为 0）")

        if pivot_row != col:
            augmented[col], augmented[pivot_row] = augmented[pivot_row], augmented[col]

        pivot = augmented[col][col]
        for j in range(2 * n_cols):
            augmented[col][j] /= pivot

        for row in range(n_rows):
            if row == col:
                continue
            factor = augmented[row][col]
            if abs(factor) < tol:
                continue
            for j in range(2 * n_cols):
                augmented[row][j] -= factor * augmented[col][j]

    result = [row[n_cols:] for row in augmented]
    return normalize_matrix(result, tol=tol)


def rank(matrix: object, *, tol: float = TOL) -> int:
    m = validate_matrix(matrix)
    work = [row[:] for row in m]
    rows, cols = shape(work)
    rank_value = 0
    row = 0

    for col in range(cols):
        pivot_row = max(range(row, rows), key=lambda r: abs(work[r][col]), default=row)
        if row >= rows or abs(work[pivot_row][col]) < tol:
            continue

        work[row], work[pivot_row] = work[pivot_row], work[row]
        pivot = work[row][col]

        for j in range(col, cols):
            work[row][j] /= pivot

        for r in range(rows):
            if r == row:
                continue
            factor = work[r][col]
            if abs(factor) < tol:
                continue
            for j in range(col, cols):
                work[r][j] -= factor * work[row][j]

        rank_value += 1
        row += 1
        if row == rows:
            break

    return rank_value


def rref(matrix: object, *, tol: float = TOL) -> list[list[int | float]]:
    m = validate_matrix(matrix)
    work = [row[:] for row in m]
    rows, cols = shape(work)
    lead = 0

    for r in range(rows):
        if lead >= cols:
            break

        pivot_row = r
        while abs(work[pivot_row][lead]) < tol:
            pivot_row += 1
            if pivot_row == rows:
                pivot_row = r
                lead += 1
                if lead == cols:
                    return normalize_matrix(work, tol=tol)
        work[r], work[pivot_row] = work[pivot_row], work[r]

        pivot = work[r][lead]
        for j in range(cols):
            work[r][j] /= pivot

        for i in range(rows):
            if i == r:
                continue
            factor = work[i][lead]
            if abs(factor) < tol:
                continue
            for j in range(cols):
                work[i][j] -= factor * work[r][j]

        lead += 1

    return normalize_matrix(work, tol=tol)


def solve_linear_system(matrix: object, vector: object, *, tol: float = TOL) -> dict:
    a = validate_matrix(matrix, name="matrix")
    b = validate_vector(vector, name="vector")
    n_rows, n_cols = shape(a)

    if n_rows != n_cols:
        raise MatrixError("当前实现只支持方阵线性方程组")
    if len(b) != n_rows:
        raise MatrixError("向量长度必须等于矩阵行数")

    augmented = [a[i][:] + [b[i]] for i in range(n_rows)]

    for col in range(n_cols):
        pivot_row = max(range(col, n_rows), key=lambda r: abs(augmented[r][col]))
        pivot_value = augmented[pivot_row][col]
        if abs(pivot_value) < tol:
            raise MatrixError("方程组无唯一解（矩阵奇异或存在自由变量）")

        if pivot_row != col:
            augmented[col], augmented[pivot_row] = augmented[pivot_row], augmented[col]

        pivot = augmented[col][col]
        for j in range(col, n_cols + 1):
            augmented[col][j] /= pivot

        for row in range(n_rows):
            if row == col:
                continue
            factor = augmented[row][col]
            if abs(factor) < tol:
                continue
            for j in range(col, n_cols + 1):
                augmented[row][j] -= factor * augmented[col][j]

    solution = [augmented[i][n_cols] for i in range(n_rows)]

    residual = []
    for i in range(n_rows):
        lhs = sum(a[i][j] * solution[j] for j in range(n_cols))
        residual.append(lhs - b[i])

    return {
        "solution": normalize_vector(solution, tol=tol),
        "residual": normalize_vector(residual, tol=tol),
        "has_unique_solution": True,
    }


def matrix_info(matrix: object, *, tol: float = TOL) -> dict:
    m = validate_matrix(matrix)
    rows, cols = shape(m)
    square = rows == cols

    info: dict[str, object] = {
        "shape": [rows, cols],
        "is_square": square,
        "transpose": normalize_matrix([list(col) for col in zip(*m)], tol=tol),
        "rank": rank(m, tol=tol),
    }

    if square:
        trace_value = sum(m[i][i] for i in range(rows))
        det_value = determinant(m, tol=tol)
        info.update(
            {
                "trace": _normalize_number(trace_value, tol=tol),
                "determinant": det_value,
                "is_invertible": det_value != 0,
            }
        )
    else:
        info.update(
            {
                "trace": None,
                "determinant": None,
                "is_invertible": False,
            }
        )

    symmetric = square and all(
        abs(m[i][j] - m[j][i]) < tol for i in range(rows) for j in range(cols)
    )
    info["is_symmetric"] = symmetric

    return info
