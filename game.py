import numpy as np
import pygame
import sys
import random
from pygame.locals import *

# 游戏常量
BOARD_SIZE = 15  # 15x15的棋盘
GRID_SIZE = 40   # 每个格子的大小
MARGIN = 50      # 边距
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (210, 180, 140)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 玩家和AI的棋子颜色
PLAYER_PIECE = 1   # 玩家使用黑棋
AI_PIECE = 2       # AI使用白棋
EMPTY = 0          # 空位置

class GomokuGame:
    def __init__(self):
        pygame.init()
        self.window_size = BOARD_SIZE * GRID_SIZE + 2 * MARGIN
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption('五子棋 (Gomoku)')
        # 确保窗口获得焦点，以便接收键盘输入
        pygame.event.set_grab(False)
        pygame.key.set_repeat(0)

        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.game_over = False
        self.winner = None
        # 使用系统默认字体以支持中文
        self.font = pygame.font.Font(pygame.font.get_default_font(), 30)
        # 尝试加载特定的中文字体，如果失败则使用默认字体
        try:
            self.font = pygame.font.SysFont('SimHei', 30)  # 尝试使用黑体
        except:
            try:
                self.font = pygame.font.SysFont('Microsoft YaHei', 30)  # 尝试使用微软雅黑
            except:
                pass  # 如果都失败了就使用默认字体
        self.turn = PLAYER_PIECE  # 玩家先手

    def draw_board(self):
        # 填充背景色
        self.screen.fill(BROWN)

        # 绘制棋盘网格
        for i in range(BOARD_SIZE):
            # 垂直线
            start_pos = (MARGIN + i * GRID_SIZE, MARGIN)
            end_pos = (MARGIN + i * GRID_SIZE, self.window_size - MARGIN)
            pygame.draw.line(self.screen, BLACK, start_pos, end_pos, 2)

            # 水平线
            start_pos = (MARGIN, MARGIN + i * GRID_SIZE)
            end_pos = (self.window_size - MARGIN, MARGIN + i * GRID_SIZE)
            pygame.draw.line(self.screen, BLACK, start_pos, end_pos, 2)

        # 绘制五个小黑点（天元和星）
        dots_pos = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]  # 棋盘上的五个标记点
        for pos in dots_pos:
            x, y = pos
            center = (MARGIN + x * GRID_SIZE, MARGIN + y * GRID_SIZE)
            pygame.draw.circle(self.screen, BLACK, center, 5)

        # 绘制棋子
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == PLAYER_PIECE:
                    center = (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE)
                    pygame.draw.circle(self.screen, BLACK, center, GRID_SIZE // 2 - 2)
                elif self.board[i][j] == AI_PIECE:
                    center = (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE)
                    pygame.draw.circle(self.screen, WHITE, center, GRID_SIZE // 2 - 2)
                    pygame.draw.circle(self.screen, BLACK, center, GRID_SIZE // 2 - 2, 2)  # 白棋黑边

        # 如果游戏结束，显示胜利信息
        if self.game_over:
            if self.winner == PLAYER_PIECE:
                text = self.font.render("你赢了！", True, RED)
            elif self.winner == AI_PIECE:
                text = self.font.render("AI赢了！", True, BLUE)
            else:
                text = self.font.render("平局！", True, GREEN)

            text_rect = text.get_rect(center=(self.window_size//2, 20))
            self.screen.blit(text, text_rect)

            # 显示重新开始提示
            restart_text = self.font.render("按R键重新开始", True, BLACK)
            restart_rect = restart_text.get_rect(center=(self.window_size//2, self.window_size - 20))
            self.screen.blit(restart_text, restart_rect)
        else:
            # 显示当前轮到谁
            if self.turn == PLAYER_PIECE:
                turn_text = self.font.render("轮到你了", True, BLACK)
            else:
                turn_text = self.font.render("AI思考中...", True, BLACK)
            turn_rect = turn_text.get_rect(center=(self.window_size//2, 20))
            self.screen.blit(turn_text, turn_rect)

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

    def ai_move(self):
        """
        简单的AI策略:
        1. 如果AI能赢，直接下在赢的位置
        2. 如果玩家下一步能赢，阻止玩家
        3. 否则，使用评分系统选择最优位置
        """
        # 复制棋盘用于评估
        board_copy = self.board.copy()

        # 第一步：检查AI是否有赢的可能
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board_copy[i][j] == EMPTY:
                    board_copy[i][j] = AI_PIECE
                    if self.check_win(i, j, AI_PIECE):
                        self.board[i][j] = AI_PIECE
                        return i, j
                    board_copy[i][j] = EMPTY

        # 第二步：检查玩家是否下一步能赢，如果是则阻止
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board_copy[i][j] == EMPTY:
                    board_copy[i][j] = PLAYER_PIECE
                    if self.check_win(i, j, PLAYER_PIECE):
                        self.board[i][j] = AI_PIECE
                        return i, j
                    board_copy[i][j] = EMPTY

        # 第三步：使用评分系统选择最佳位置
        best_score = -float('inf')
        move = None

        # 获取所有空位置
        empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.board[i][j] == EMPTY]

        # 如果棋盘是空的，第一步下在天元（中心点）
        if len(empty_cells) == BOARD_SIZE * BOARD_SIZE:
            move = (BOARD_SIZE // 2, BOARD_SIZE // 2)
            self.board[move[0]][move[1]] = AI_PIECE
            return move

        # 对每个可能的位置进行评分
        for i, j in empty_cells:
            score = self.evaluate_move(i, j)
            if score > best_score:
                best_score = score
                move = (i, j)

        if move:
            self.board[move[0]][move[1]] = AI_PIECE
        return move

    def evaluate_move(self, row, col):
        """评估在特定位置落子的分数"""
        # 基础分数 - 偏好靠近中心的位置
        score = 10 - (abs(row - BOARD_SIZE//2) + abs(col - BOARD_SIZE//2))

        # 检查周围的棋子情况
        for piece in [AI_PIECE, PLAYER_PIECE]:
            # 检查每个方向的连续棋子
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:  # 水平、垂直、对角线
                for direction in [-1, 1]:  # 两个方向
                    count = 0
                    blocked = 0
                    r, c = row, col

                    # 模拟在此位置落子
                    temp_board = self.board.copy()
                    temp_board[row][col] = AI_PIECE

                    # 向一个方向延伸
                    for step in range(1, 5):  # 最多看4步
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

                    # 根据连续棋子数和是否被阻挡来调整分数
                    if piece == AI_PIECE:
                        # AI的连续棋子，加分
                        if count == 4:
                            score += 1000  # 形成五连
                        elif count == 3 and blocked == 0:
                            score += 500   # 开放的四连
                        elif count == 3 and blocked == 1:
                            score += 100   # 半开放的四连
                        elif count == 2 and blocked == 0:
                            score += 50    # 开放的三连
                        elif count == 2 and blocked == 1:
                            score += 10    # 半开放的三连
                    else:
                        # 玩家的连续棋子，考虑防守
                        if count == 4:
                            score += 900  # 阻止玩家五连
                        elif count == 3 and blocked == 0:
                            score += 450   # 阻止开放的四连
                        elif count == 3 and blocked == 1:
                            score += 90    # 阻止半开放的四连
                        elif count == 2 and blocked == 0:
                            score += 40    # 阻止开放的三连

        # 加入一些随机性以避免AI太容易预测
        score += random.randint(0, 10)

        return score

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # 键盘事件处理（任何时候都可以响应）
                if event.type == KEYDOWN:
                    # 调试输出
                    print(f"键盘事件: key={event.key}, unicode={event.unicode}, K_r={K_r}, ord('R')={ord('R')}")
                    # 检测r键（支持小写r和大写R）
                    if (event.key == K_r) or (event.key == ord('R')):  # 按R键重新开始（支持大小写）
                        print("检测到R键，重置游戏")
                        self.reset_game()
                # 检测窗口获得焦点
                elif event.type == ACTIVEEVENT:
                    print(f"焦点事件: gain={event.gain}, state={event.state}")
                    if event.gain:
                        # 窗口获得焦点，重绘棋盘
                        self.draw_board()
                        pygame.display.update()

                # 鼠标事件处理（只在游戏进行中且轮到玩家时响应）
                if event.type == MOUSEBUTTONDOWN and not self.game_over and self.turn == PLAYER_PIECE:
                    # 玩家回合
                    x, y = pygame.mouse.get_pos()
                    # 转换鼠标位置为棋盘索引
                    col = round((x - MARGIN) / GRID_SIZE)
                    row = round((y - MARGIN) / GRID_SIZE)

                    # 确保位置在棋盘内并且为空
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == EMPTY:
                        # 放置棋子
                        self.board[row][col] = PLAYER_PIECE

                        # 检查是否赢了
                        if self.check_win(row, col, PLAYER_PIECE):
                            self.game_over = True
                            self.winner = PLAYER_PIECE
                        elif self.is_board_full():
                            self.game_over = True
                            self.winner = None  # 平局
                        else:
                            self.turn = AI_PIECE

            # AI回合
            if not self.game_over and self.turn == AI_PIECE:
                # 让AI走棋
                row, col = self.ai_move()

                # 检查AI是否赢了
                if self.check_win(row, col, AI_PIECE):
                    self.game_over = True
                    self.winner = AI_PIECE
                elif self.is_board_full():
                    self.game_over = True
                    self.winner = None  # 平局
                else:
                    self.turn = PLAYER_PIECE

            # 绘制棋盘和棋子
            self.draw_board()
            pygame.display.update()
            clock.tick(30)

if __name__ == "__main__":
    game = GomokuGame()
    game.run()
