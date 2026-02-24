import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase
import os
from random import randint

# 尝试注册中文字体
def register_chinese_font():
    # Windows 系统常见中文字体路径
    font_paths = [
        r'C:\Windows\Fonts\msyh.ttc',  # 微软雅黑
        r'C:\Windows\Fonts\simhei.ttf',  # 黑体
        r'C:\Windows\Fonts\simsun.ttc',  # 宋体
        r'C:\Windows\Fonts\simkai.ttf',  # 楷体
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name='chinese', fn_regular=font_path)
                print(f"成功加载中文字体: {font_path}")
                return 'chinese'
            except Exception as e:
                print(f"加载字体失败 {font_path}: {e}")
                continue

    print("未找到可用中文字体，使用默认字体")
    return 'Roboto'

# 注册中文字体
chinese_font = register_chinese_font()

# 游戏常量
BOARD_SIZE = 15  # 15x15的棋盘
GRID_SIZE = 40   # 每个格子的大小
MARGIN = 50      # 边距

# 玩家和AI的棋子颜色
PLAYER_PIECE = 1   # 玩家使用黑棋
AI_PIECE = 2       # AI使用白棋
EMPTY = 0          # 空位置

class GomokuBoard(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.game_over = False
        self.winner = None
        self.turn = PLAYER_PIECE

        # 绑定窗口大小变化事件
        Window.bind(size=self.on_window_resize)

        # 初始绘制棋盘
        Clock.schedule_once(lambda dt: self.draw_board(), 0)

    def on_window_resize(self, instance, size):
        """窗口大小变化时重新绘制棋盘"""
        self.draw_board()

    def draw_board(self):
        self.canvas.clear()

        # 获取当前窗口大小
        window_width, window_height = Window.size

        # 计算棋盘区域（除去底部按钮高度）
        board_height = window_height - 60  # 减去底部按钮高度

        # 计算动态网格大小
        grid_size = min(window_width, board_height) / (BOARD_SIZE + 1)
        margin = grid_size

        # 绘制背景（整个窗口）
        with self.canvas:
            Color(0.82, 0.71, 0.55, 1)  # 棕色背景
            Rectangle(pos=(0, 0), size=(window_width, board_height))

            # 绘制网格
            Color(0, 0, 0, 1)
            for i in range(BOARD_SIZE):
                # 垂直线
                x = margin + i * grid_size
                Line(points=[x, margin, x, board_height - margin], width=2)
                # 水平线
                y = margin + i * grid_size
                Line(points=[margin, y, window_width - margin, y], width=2)

            # 绘制五个小黑点（天元和星）
            dots_pos = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
            for x, y in dots_pos:
                center_x = margin + x * grid_size
                center_y = margin + y * grid_size
                Color(0, 0, 0, 1)
                Ellipse(pos=(center_x - 5, center_y - 5), size=(10, 10))

            # 绘制棋子
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.board[i][j] == PLAYER_PIECE:
                        center_x = margin + j * grid_size
                        center_y = margin + i * grid_size
                        Color(0, 0, 0, 1)
                        Ellipse(pos=(center_x - grid_size//2 + 2,
                                   center_y - grid_size//2 + 2),
                               size=(grid_size - 4, grid_size - 4))
                    elif self.board[i][j] == AI_PIECE:
                        center_x = margin + j * grid_size
                        center_y = margin + i * grid_size
                        Color(1, 1, 1, 1)
                        Ellipse(pos=(center_x - grid_size//2 + 2,
                                   center_y - grid_size//2 + 2),
                               size=(grid_size - 4, grid_size - 4))
                        # 白棋黑边
                        Color(0, 0, 0, 1)
                        Line(ellipse=(center_x - grid_size//2 + 2,
                                     center_y - grid_size//2 + 2,
                                     grid_size - 4, grid_size - 4), width=2)

    def on_touch_down(self, touch):
        # 首先调用父类的方法
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)

        if self.game_over:
            return

        # 获取当前窗口大小
        window_width, window_height = Window.size
        board_height = window_height - 60
        grid_size = min(window_width, board_height) / (BOARD_SIZE + 1)
        margin = grid_size

        # 检查是否点击在棋盘区域内
        if touch.y < margin or touch.y > board_height - margin:
            return
        if touch.x < margin or touch.x > window_width - margin:
            return

        # 转换触摸位置为棋盘索引
        col = int((touch.x - margin + grid_size // 2) // grid_size)
        row = int((touch.y - margin + grid_size // 2) // grid_size)

        # 确保位置在棋盘内并且为空
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == EMPTY:
            if self.turn == PLAYER_PIECE:
                # 放置棋子
                self.board[row][col] = PLAYER_PIECE
                self.draw_board()

                # 检查是否赢了
                if self.check_win(row, col, PLAYER_PIECE):
                    self.game_over = True
                    self.winner = PLAYER_PIECE
                    self.show_result("你赢了！")
                elif self.is_board_full():
                    self.game_over = True
                    self.winner = None
                    self.show_result("平局！")
                else:
                    self.turn = AI_PIECE
                    # AI延迟一秒后落子
                    Clock.schedule_once(self.ai_move_callback, 0.5)

    def ai_move_callback(self, dt):
        """AI落子的回调函数"""
        if self.game_over:
            return

        row, col = self.ai_move()

        if row is not None and col is not None:
            # 检查AI是否赢了
            if self.check_win(row, col, AI_PIECE):
                self.game_over = True
                self.winner = AI_PIECE
                self.show_result("AI赢了！")
            elif self.is_board_full():
                self.game_over = True
                self.winner = None
                self.show_result("平局！")
            else:
                self.turn = PLAYER_PIECE

    def check_win(self, row, col, piece):
        # 检查水平方向
        count = 0
        for j in range(max(0, col-4), min(BOARD_SIZE, col+5)):
            if self.board[row][j] == piece:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0

        # 检查垂直方向
        count = 0
        for i in range(max(0, row-4), min(BOARD_SIZE, row+5)):
            if self.board[i][col] == piece:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0

        # 检查正对角线 (/)
        count = 0
        for i in range(-4, 5):
            r, c = row + i, col + i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if self.board[r][c] == piece:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0

        # 检查反对角线 (\)
        count = 0
        for i in range(-4, 5):
            r, c = row + i, col - i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if self.board[r][c] == piece:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0

        return False

    def is_board_full(self):
        return np.all(self.board != EMPTY)

    def reset_game(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.game_over = False
        self.winner = None
        self.turn = PLAYER_PIECE
        self.draw_board()

    def ai_move(self):
        """简单的AI策略"""
        board_copy = self.board.copy()

        # 第一步：检查AI是否有赢的可能
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board_copy[i][j] == EMPTY:
                    board_copy[i][j] = AI_PIECE
                    if self.check_win(i, j, AI_PIECE):
                        self.board[i][j] = AI_PIECE
                        self.draw_board()
                        return i, j
                    board_copy[i][j] = EMPTY

        # 第二步：检查玩家是否下一步能赢
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board_copy[i][j] == EMPTY:
                    board_copy[i][j] = PLAYER_PIECE
                    if self.check_win(i, j, PLAYER_PIECE):
                        self.board[i][j] = AI_PIECE
                        self.draw_board()
                        return i, j
                    board_copy[i][j] = EMPTY

        # 第三步：使用评分系统
        best_score = -float('inf')
        move = None

        empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)
                      if self.board[i][j] == EMPTY]

        if len(empty_cells) == BOARD_SIZE * BOARD_SIZE:
            move = (BOARD_SIZE // 2, BOARD_SIZE // 2)
            self.board[move[0]][move[1]] = AI_PIECE
            self.draw_board()
            return move

        for i, j in empty_cells:
            score = self.evaluate_move(i, j)
            if score > best_score:
                best_score = score
                move = (i, j)

        if move:
            self.board[move[0]][move[1]] = AI_PIECE
            self.draw_board()
        return move

    def evaluate_move(self, row, col):
        """评估在特定位置落子的分数"""
        score = 10 - (abs(row - BOARD_SIZE//2) + abs(col - BOARD_SIZE//2))

        for piece in [AI_PIECE, PLAYER_PIECE]:
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                for direction in [-1, 1]:
                    count = 0
                    blocked = 0
                    r, c = row, col

                    temp_board = self.board.copy()
                    temp_board[row][col] = AI_PIECE

                    for step in range(1, 5):
                        r += direction * dr
                        c += direction * dc
                        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                            if temp_board[r][c] == piece:
                                count += 1
                            elif temp_board[r][c] != EMPTY:
                                blocked += 1
                                break
                            else:
                                break
                        else:
                            blocked += 1
                            break

                    if piece == AI_PIECE:
                        if count == 4:
                            score += 1000
                        elif count == 3 and blocked == 0:
                            score += 500
                        elif count == 3 and blocked == 1:
                            score += 100
                        elif count == 2 and blocked == 0:
                            score += 50
                        elif count == 2 and blocked == 1:
                            score += 10
                    else:
                        if count == 4:
                            score += 900
                        elif count == 3 and blocked == 0:
                            score += 450
                        elif count == 3 and blocked == 1:
                            score += 90
                        elif count == 2 and blocked == 0:
                            score += 40

        score += randint(0, 10)
        return score

    def show_result(self, message):
        """显示游戏结果"""
        popup = Popup(
            title='游戏结束',
            title_font=chinese_font,
            title_size='20sp',
            content=Label(text=message, font_size=30, font_name=chinese_font),
            size_hint=(0.6, 0.4)
        )
        popup.open()

class GomokuApp(App):
    def build(self):
        # 设置初始窗口大小（接近全屏）
        Window.size = (800, 860)

        # 创建主布局
        layout = BoxLayout(orientation='vertical')

        # 创建棋盘
        self.board = GomokuBoard()
        layout.add_widget(self.board)

        # 创建重新开始按钮
        button = Button(
            text='重新开始',
            size_hint_y=None,
            height=60,
            font_size=20,
            font_name=chinese_font
        )
        button.bind(on_press=self.reset_game)
        layout.add_widget(button)

        return layout

    def reset_game(self, instance):
        self.board.reset_game()

if __name__ == '__main__':
    GomokuApp().run()