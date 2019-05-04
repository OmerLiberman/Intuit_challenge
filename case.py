from board import Board


# from sympy.solvers import solve, symbol, Eq


class Case:
    NO_SOLVE = -1

    def __init__(self, n, b, h, boxes_coords, hunters_coords):
        self.is_size_even = (n % 2 == 0)
        self.board = Board(n, b, h, self.is_size_even)
        if self.is_size_even:
            self.board.split_boxes_hunters_when_size_is_even(boxes_coords, hunters_coords)
        else:
            self.board.split_boxes_hunters_when_size_is_odd(boxes_coords, hunters_coords)

    def solve(self):
        if self.is_size_even:
            return self._solve_even_size_board()
        else:
            return self._solve_odd_size_board()

    def _solve_even_size_board(self):
        """
        the board looks like :
        A B
        D C
        - elaboration about this method is in the readme.
        :return: the number of hunters can be added to the board but it is still stable.
        """
        # part_a -> quarter A data -> num of empty cells, num of hunters]
        part_a, part_b, part_c, part_d = self._split_even_size_board()
        ext_a, ext_c = solve_equation(part_a[0], part_d[0], part_d[1] - part_a[1])
        ext_d, ext_b = solve_equation(part_c[0], part_b[0], part_b[1] - part_c[1])

        all_additions = [ext_a, ext_b, ext_c, ext_d]
        for add in all_additions:
            if add < 0:
                return self.NO_SOLVE
        return sum(all_additions)

    def _solve_odd_size_board(self):
        """
        the board looks like :
        ***
        - elaboration about this method is in the readme.
        :return: the number of hunters can be added to the board but it is still stable.
        """
        # part_a -> quarter A data -> num of empty cells, num of hunters]
        part_a, part_b, part_c, part_d, part_e, part_f, part_g, part_h = self._split_odd_size_board()
        ext_a, ext_c = solve_equation(part_a[0], part_d[0], part_d[1] - part_a[1])
        ext_d, ext_b = solve_equation(part_c[0], part_b[0], part_b[1] - part_c[1])
        ext_e, ext_g = solve_equation(part_e[0], part_g[0], part_g[1] - part_e[1])
        ext_h, ext_f = solve_equation(part_h[0], part_f[0], part_f[1] - part_h[1])

        all_additions = [ext_a, ext_b, ext_c, ext_d, ext_e, ext_g, ext_h, ext_f]
        if all(i >= 0 for i in all_additions):
            return sum(all_additions)
        else:
            return self.NO_SOLVE

    def _split_even_size_board(self):
        """
        Get the [num of empty cells, num of hunters] for each quarter of the board.
        the board looks like :
        A B
        D C
        where A, B, C, D are four equal size squares with edges of N/2
        :return: [num of empty cells, num of hunters] for each part in the board
        """
        seats_square = self.board.N / 2 * self.board.N / 2
        part_a = seats_square - self.board.boxes[0] - self.board.hunters[0], self.board.hunters[0]
        part_b = seats_square - self.board.boxes[1] - self.board.hunters[1], self.board.hunters[1]
        part_c = seats_square - self.board.boxes[2] - self.board.hunters[2], self.board.hunters[2]
        part_d = seats_square - self.board.boxes[3] - self.board.hunters[3], self.board.hunters[3]
        return part_a, part_b, part_c, part_d

    def _split_odd_size_board(self):
        """
        Get the [num of empty cells, num of hunters] of each part of the board.
        the board looks like :
        A E B
        H I F
        D G C
        where - A, B, C, D are four equal size squares with edges of (N-1)/2
                H, F have a shape of 1 * (N-1)/2
                E, G have a shape of (N-1)/2 * 1
                I is 1 * 1 (single seat) in the middle
        In this method I consider "square part" the A, B, C, D parts and
        "long part" the E, F, G, H
        :return: [num of empty cells, num of hunters] for each part in the board
        """
        seats_square = (self.board.N - 1) / 2 * (self.board.N - 1) / 2
        seats_long = (self.board.N - 1) / 2
        part_a = seats_square - self.board.boxes[0] - self.board.hunters[0], self.board.hunters[0]
        part_b = seats_square - self.board.boxes[1] - self.board.hunters[1], self.board.hunters[1]
        part_c = seats_square - self.board.boxes[2] - self.board.hunters[2], self.board.hunters[2]
        part_d = seats_square - self.board.boxes[3] - self.board.hunters[3], self.board.hunters[3]
        part_e = seats_long - self.board.boxes[4] - self.board.hunters[4], self.board.hunters[4]
        part_f = seats_long - self.board.boxes[5] - self.board.hunters[5], self.board.hunters[5]
        part_g = seats_long - self.board.boxes[6] - self.board.hunters[6], self.board.hunters[6]
        part_h = seats_long - self.board.boxes[7] - self.board.hunters[7], self.board.hunters[7]

        return part_a, part_b, part_c, part_d, part_e, part_f, part_g, part_h


def solve_equation(first_unknown_limit, second_unknown_limit, result):
    """
    Intend to solve the equation: first_unknown - second_unknown = result
    when : first_unknown <= first_unknown_limit
            second_unknown <= second_unknown_limit
    :param first_unknown_limit, second_unknown_limit:
    :return: tuple (first_unknown_value , second_unknown_value)
    """
    max_first, max_second = -1, -1
    for x in reversed(range(int(first_unknown_limit + 1))):
        for y in reversed(range(int(second_unknown_limit + 1))):
            if x - y == result and x + y > max_first + max_second:
                return x, y
    return max_first, max_second
