import unittest
from maze import Maze, Cell, Window, Point

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1.cells), num_cols) 
        self.assertEqual(len(m1.cells[0]), num_rows)  

    def test_cell_walls_initial_state(self):
        # Verify that all walls are present in a new cell
        cell = Cell(0, 0, 10, 10)
        self.assertTrue(cell.has_left_wall)
        self.assertTrue(cell.has_right_wall)
        self.assertTrue(cell.has_top_wall)
        self.assertTrue(cell.has_bottom_wall)

    def test_maze_cell_initialization(self):
        # Test if the maze initializes cells with the correct dimensions
        num_cols = 5
        num_rows = 4
        cell_size_x = 20
        cell_size_y = 30
        m1 = Maze(0, 0, num_rows, num_cols, cell_size_x, cell_size_y)

        for col in m1.cells:
            for cell in col:
                self.assertEqual(cell._x2 - cell._x1, cell_size_x)
                self.assertEqual(cell._y2 - cell._y1, cell_size_y)

    def test_maze_cell_coordinates(self):
        # Test if cells have correct coordinates after initialization
        num_cols = 3
        num_rows = 2
        cell_size_x = 10
        cell_size_y = 15
        m1 = Maze(0, 0, num_rows, num_cols, cell_size_x, cell_size_y)

        for i in range(num_cols):
            for j in range(num_rows):
                cell = m1.cells[i][j]
                expected_x1 = i * cell_size_x
                expected_y1 = j * cell_size_y
                expected_x2 = expected_x1 + cell_size_x
                expected_y2 = expected_y1 + cell_size_y

                self.assertEqual(cell._x1, expected_x1)
                self.assertEqual(cell._y1, expected_y1)
                self.assertEqual(cell._x2, expected_x2)
                self.assertEqual(cell._y2, expected_y2)

    def test_cell_center(self):
        # Test if the get_center method returns the correct center point
        cell = Cell(0, 0, 20, 20)
        center = cell.get_center()
        self.assertEqual(center.x, 10)
        self.assertEqual(center.y, 10)

    def test_break_entrance_and_exit(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 20, 20)

        # Get the entrance and exit cells
        entrance_cell = m1.cells[0][0]
        exit_cell = m1.cells[-1][-1]

        # Verify wall removal
        self.assertFalse(entrance_cell.has_top_wall, "Entrance cell's top wall should be removed.")
        self.assertFalse(exit_cell.has_bottom_wall, "Exit cell's bottom wall should be removed.")
    
    def test_visited_reset(self):
        num_cols = 10
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 20, 20)

        # Get the entrance and exit cells
        entrance_cell = m1.cells[0][0]
        exit_cell = m1.cells[-1][-1]

        # Verify visited
        for i in m1.cells:
            for j in m1.cells:
                if i == 0 and j == 0:
                    self.assertTrue(m1.cells[i][j].visited, "Entrace cell should be visited.")
                else:
                    self.assertFalse(m1.cells[i][j].visited, "Rest of the cells should be reset to NOT visited.")
                    


if __name__ == "__main__":
    unittest.main()
