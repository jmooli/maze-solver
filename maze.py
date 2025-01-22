import random
import time
from tkinter import Tk, BOTH, Canvas

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 768 

class Point:
    def __init__(self, x : float, y: float):
        self.x = x 
        self.y = y

class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)

class Window:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.__root  = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(self.__root, width=self.width, height=self.height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        while self.running:
            self.redraw()
    
    def close(self):
        self.running = False

    def draw_line(self, line: Line, fill_color):
        line.draw(self.canvas, fill_color)

    def draw_move(self, from_cell, to_cell, undo=False):
        from_point = from_cell.get_center()
        dest_point = to_cell.get_center()
        line = Line(from_point, dest_point)
        
        color : str = "red" 
        if undo :
            color = "grey"
        
        self.draw_line(line, color)

class Cell:
    def __init__(self, x1, y1, x2, y2, win : Window = None, coord=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.color = "black"
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.walls = {}
        self.visited = False
        self.coord = coord

    def draw(self, debug = False):
        
        #left wall
        left_start : Point = Point(self._x1, self._y1)
        left_end : Point = Point(self._x1, self._y2)
        left_line : Line = Line(left_start, left_end)
        self.walls["left"] = left_line

        #right wall
        right_start : Point = Point(self._x2, self._y1)
        right_end : Point = Point(self._x2, self._y2)
        right_line : Line = Line(right_start, right_end)
        self.walls["right"] = right_line

        #bottom wall
        bottom_start : Point = Point(self._x1, self._y2)
        bottom_end : Point = Point(self._x2, self._y2)
        bottom_line : Line = Line(bottom_start, bottom_end)
        self.walls["bottom"] = bottom_line
        
        #top wall
        top_start : Point = Point(self._x1, self._y1)
        top_end : Point = Point(self._x2, self._y1)
        top_line : Line = Line(top_start, top_end)
        self.walls["top"] = top_line

        #draw lines
        if self._win: 
            for k, v in self.walls.items():
                if k == "top" and not self.has_top_wall:
                    self.color = "white"
                elif k == "bottom" and not self.has_bottom_wall:
                    self.color = "white"
                elif k == "right" and not self.has_right_wall:
                    self.color = "white"
                elif k == "left" and not self.has_left_wall:
                    self.color = "white"
                else:
                    self.color = "black"
                
                self._win.draw_line(v, self.color)
        
        if debug and self._win:
            self.draw_debug_info()
    
    def draw_debug_info(self):
        # Draw cell coordinates and visited status
        if self._win:
            center = self.get_center()
            text = f"{self.coord}\n{'Visited' if self.visited else 'Unvisited'}"
            self._win.canvas.create_text(
                center.x, center.y,
                text=text,
                fill="red",
                font=("Arial", 10),
                anchor="center"
            )
    
    def get_center(self) -> Point:
        _x = (self._x1 + self._x2) / 2
        _y = (self._y1 + self._y2) / 2
        _center = Point(_x, _y)
        return _center
    
class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, _win=None, seed = None ):
        self._win = _win
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.cells = []
        self.path = []
        self._create_cells()
        if seed != None:
            random.seed(seed)      

    def _draw_cell(self, i, j):
        cell : Cell = self.cells[i][j]

        x_offset = self.x1 + (i * self.cell_size_x)
        y_offset = self.y1 + (j * self.cell_size_y)

        cell._x1 += x_offset
        cell._x2 += x_offset
        cell._y1 += y_offset
        cell._y2 += y_offset

        cell.draw()
        self._animate()


    def _create_cells(self):
        for _ in range(self.num_cols):
            col = []
            for _ in range(self.num_rows):
                _cell = Cell(0, 0, self.cell_size_x, self.cell_size_y, self._win, )
                col.append(_cell)
            self.cells.append(col)

        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j].coord = (i, j)
                self._draw_cell(i, j)

        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _break_entrance_and_exit(self):
        start_cell : Cell = self.cells[0][0]
        exit_cell : Cell = self.cells[-1][-1]

        start_cell.has_top_wall = False
        exit_cell.has_bottom_wall = False
        start_cell.draw()
        exit_cell.draw()

    def _reset_cells_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False


    def get_nearby_cells(self, i, j):
        directions = []

        # Debug: Print current cell
        print(f"Getting neighbors for cell ({i}, {j})")

        if i > 0:  # West
            neighbor = self.cells[i-1][j]
            if not neighbor.visited:
                print(f"Checking west: ({i-1}, {j}) - visited: {neighbor.visited}, left_wall: {self.cells[i][j].has_left_wall}, right_wall: {neighbor.has_right_wall}")
                directions.append(neighbor)
        if i < len(self.cells) - 1:  # East
            neighbor = self.cells[i+1][j]
            if not neighbor.visited:
                print(f"Checking east: ({i+1}, {j}) - visited: {neighbor.visited}, right_wall: {self.cells[i][j].has_right_wall}, left_wall: {neighbor.has_left_wall}")
                directions.append(neighbor)
        if j > 0:  # North
            neighbor = self.cells[i][j-1]
            if not neighbor.visited:
                print(f"Checking north: ({i}, {j-1}) - visited: {neighbor.visited}, top_wall: {self.cells[i][j].has_top_wall}, bottom_wall: {neighbor.has_bottom_wall}")
                directions.append(neighbor)
        if j < len(self.cells[0]) - 1:  # South
            neighbor = self.cells[i][j+1]
            if not neighbor.visited:
                print(f"Checking south: ({i}, {j+1}) - visited: {neighbor.visited}, bottom_wall: {self.cells[i][j].has_bottom_wall}, top_wall: {neighbor.has_top_wall}")
                directions.append(neighbor)

        # Debug: Print found neighbors
        print(f"Neighbors for cell ({i}, {j}): {[cell.coord for cell in directions]}")

        return directions


    def break_walls_between_cells(self, cur: Cell, next: Cell):
        cur_x, cur_y = cur.coord  # cur_x: column, cur_y: row
        next_x, next_y = next.coord

        if cur_x > next_x:  # West
            cur.has_left_wall = False
            next.has_right_wall = False
        elif cur_x < next_x:  # East
            cur.has_right_wall = False
            next.has_left_wall = False
        elif cur_y > next_y:  # North
            cur.has_top_wall = False
            next.has_bottom_wall = False
        elif cur_y < next_y:  # South
            cur.has_bottom_wall = False
            next.has_top_wall = False

        cur.draw()
        next.draw()

    def is_wall_in_between(self, cur: Cell, next: Cell):
        cur_x, cur_y = cur.coord  # cur_x: column, cur_y: row
        next_x, next_y = next.coord

        if cur_x > next_x:  # West
            if cur.has_left_wall == False and next.has_right_wall == False:
                return False
            
        elif cur_x < next_x:  # East
            if cur.has_right_wall == False and  next.has_left_wall == False:
                return False
                    
        elif cur_y > next_y:  # North
            if cur.has_top_wall == False and next.has_bottom_wall == False:
                return False
            
        elif cur_y < next_y:  # South
            if cur.has_bottom_wall == False and next.has_top_wall == False:
                return False
        return True
            
        
    def _break_walls_r(self, i, j):
        current_cell : Cell = self.cells[i][j]
        current_cell.visited = True

        while True:
            possible_moves = self.get_nearby_cells(i, j)
            num_of_possible_moves = len(possible_moves)

            if num_of_possible_moves == 0:
                current_cell.draw
                return
            
            next_cell = possible_moves[random.randint(0, num_of_possible_moves - 1)]
            self.break_walls_between_cells(current_cell, next_cell)
            self._break_walls_r(next_cell.coord[0], next_cell.coord[1])

    def _animate(self):
        if self._win:
            self._win.redraw()
            time.sleep(0.05)
    
    def _solve_r(self, i, j) -> bool:
        self._animate()
        current_cell : Cell = self.cells[i][j]
        end_cell : Cell = self.cells[-1][-1]
        current_cell.visited = True

        if current_cell == end_cell:
            return True
        possible_moves = self.get_nearby_cells(i, j)
        for dir in possible_moves:
            if not self.is_wall_in_between(current_cell, dir):
                self._win.draw_move(current_cell, dir, undo=False)
                _i, _j = dir.coord
                if self._solve_r(_i, _j):
                    return True
                else: 
                    self._win.draw_move(current_cell, dir, undo=True)
        return False

    def solve(self) -> bool:
        return self._solve_r(0, 0)


def main():
    win = Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    win.running = True
    
    num_cols = 15
    num_rows = 8
    m1 = Maze(60, 20, num_rows, num_cols, 80, 80, win)
    m1.solve()
    
    win.wait_for_close()

if __name__ == "__main__":
    main()
