from __future__ import annotations

from fastmcp import FastMCP

from . import linear_algebra as la

mcp = FastMCP(
    name="LinearAlgebraMCP",
    instructions=(
        "这是一个线性代数 MCP 服务。"
        "优先使用这些工具做精确矩阵运算，而不是靠模型心算。"
        "输入矩阵统一使用二维数组，例如 [[1,2],[3,4]]。"
    ),
)


@mcp.tool
def matrix_info(matrix: list[list[float]]) -> dict:
    """返回矩阵基础信息：形状、秩、转置、是否方阵、是否对称、迹、行列式、是否可逆。"""
    return la.matrix_info(matrix)


@mcp.tool
def matrix_add(a: list[list[float]], b: list[list[float]]) -> list[list[int | float]]:
    """计算两个同形矩阵的加法。"""
    return la.matrix_add(a, b)


@mcp.tool
def matrix_subtract(a: list[list[float]], b: list[list[float]]) -> list[list[int | float]]:
    """计算两个同形矩阵的减法 a - b。"""
    return la.matrix_subtract(a, b)


@mcp.tool
def matrix_multiply(a: list[list[float]], b: list[list[float]]) -> list[list[int | float]]:
    """计算矩阵乘法 a × b。要求 a 的列数等于 b 的行数。"""
    return la.matrix_multiply(a, b)


@mcp.tool
def matrix_transpose(matrix: list[list[float]]) -> list[list[int | float]]:
    """计算矩阵转置。"""
    return la.transpose(matrix)


@mcp.tool
def matrix_determinant(matrix: list[list[float]]) -> int | float:
    """计算方阵的行列式。"""
    return la.determinant(matrix)


@mcp.tool
def matrix_inverse(matrix: list[list[float]]) -> list[list[int | float]]:
    """计算方阵逆矩阵。若矩阵不可逆会抛出错误。"""
    return la.inverse(matrix)


@mcp.tool
def matrix_rank(matrix: list[list[float]]) -> int:
    """计算矩阵的秩。"""
    return la.rank(matrix)


@mcp.tool
def matrix_rref(matrix: list[list[float]]) -> list[list[int | float]]:
    """把矩阵化为最简行阶梯形（RREF）。"""
    return la.rref(matrix)


@mcp.tool
def solve_linear_system(matrix: list[list[float]], vector: list[float]) -> dict:
    """求解线性方程组 Ax=b。当前版本要求 A 为可逆方阵，返回解向量和残差。"""
    return la.solve_linear_system(matrix, vector)
