import unittest

from src import linear_algebra as la


class LinearAlgebraTests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(la.matrix_add([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[6, 8], [10, 12]])

    def test_multiply(self):
        self.assertEqual(la.matrix_multiply([[1, 2, 3]], [[1], [0], [1]]), [[4]])

    def test_determinant(self):
        self.assertEqual(la.determinant([[1, 2], [3, 4]]), -2)

    def test_inverse(self):
        self.assertEqual(la.inverse([[4, 7], [2, 6]]), [[0.6, -0.7], [-0.2, 0.4]])

    def test_rank(self):
        self.assertEqual(la.rank([[1, 2], [2, 4]]), 1)

    def test_rref(self):
        self.assertEqual(la.rref([[1, 2], [3, 4]]), [[1, 0], [0, 1]])

    def test_solve_linear_system(self):
        result = la.solve_linear_system([[2, 1], [5, 3]], [1, 2])
        self.assertEqual(result["solution"], [1, -1])
        self.assertEqual(result["residual"], [0, 0])


if __name__ == "__main__":
    unittest.main()
