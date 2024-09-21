import pygame
import random

# 초기 설정
pygame.init()

# 화면 크기 설정
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

# 색상 정의 - 색상은 모든 언어에서 RGB로 적용 / 가끔 오른쪽에서 왼쪽으로 인식 하는 것이 있다
black = (0, 0, 0)
shape_colors = [
    (0, 255, 0),  # S-Shape (초록색)
    (255, 0, 0),  # Z-Shape (빨간색)
    (0, 255, 255),  # I-Shape (청록색)
    (255, 255, 0),  # O-Shape (노란색)
    (0, 0, 255),  # J-Shape (파란색)
    (255, 165, 0),  # L-Shape (주황색)
    (128, 0, 128)  # T-Shape (보라색)
]

# 블록 크기 및 속도
block_size = 30
fall_speed = 500  # milliseconds -> 대부분 이걸로 표현

# 테트리스 보드 설정
cols = screen_width // block_size
rows = screen_height // block_size

# 테트리스 모양
shapes = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],  # S-Shape
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],  # Z-Shape
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],

    [['.....',
      '.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],  # I-Shape
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '..00.',
      '..00.',
      '.....']],  # O-Shape

    [['.....',
      '.....',
      '..0..',
      '..000',
      '.....'],  # J-Shape
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '000..',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']],

    [['.....',
      '.....',
      '...0.',
      '..000',
      '.....'],  # L-Shape
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '000..',
      '.0...',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']],

    [['.....',
      '.....',
      '..0..',
      '.000.',
      '.....'],  # T-Shape
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
]


# 블록 클래스 정의
class Piece:
    def __init__(self, x, y, shape):   # 일종의 최소 조건 -> self : 이 클래스 안에 자신이 있다고 정의
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

    def get_blocks(self): # -> 값을 불러올 때 쓸 수 있음 ; self값 불러오기
        positions = []
        shape_format = self.shape[self.rotation % len(self.shape)] # self.shape : 어떤 블록을 가져올지 정의하는 구간
        for i, line in enumerate(shape_format): # 반복 - enumerate: 인덱스와 항목 값 같이 출력
            row = list(line)
            for j, column in enumerate(row): # 반복 = column값이 다 꽉 찰때 까지 도형 출력
                if column == '0': # column값이 0일때 x와 y에 라인 1씩 추가하기
                    positions.append((self.x + j, self.y + i))
        return positions


# 보드 초기화
def create_grid(locked_positions={}): # 딕셔너리 - items는 딕셔너리에서 씀
    grid = [[black for _ in range(cols)] for _ in range(rows)] # _은 for문 돌리긴 하지만 각각에 대한 값을 가지고 오지 않았을 때; 변수를 쓰지 않을 때 사용

    for (x, y), color in locked_positions.items(): # locked_positions에 안에 있는 x, y값 (블럭)
        if y > -1: # y값이 없을 때 (-1보다 클 때)
            grid[y][x] = color # 보드에 해당 블럭 색깔 채우기
    return grid


# 블록이 보드 내에 있는지 확인
def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(cols) if grid[i] # 리스트 형태 - 보드에 아무것도 없는 상태
                     [j] == black] for i in range(rows)]
    accepted_pos = [j for sub in accepted_pos for j in sub] # y값만 뽑고 싶을 때 사용
    formatted = shape.get_blocks() # 블록이 보드 내애 있는 것을 formatted에 저장

    for pos in formatted: # formatted 안에 있는 블록
        if pos not in accepted_pos: # 블록이 없을 경우
            if pos[1] > -1: # 첫줄에 아무것도 없을 경우
                return False
    return True


# 보드에 블록 위치 고정
def lock_positions(shape, grid, locked_positions):
    for pos in shape.get_blocks(): # 블록이 내려올 때
        x, y = pos # x, y에 내려오는 블록
        locked_positions[(x, y)] = shape.color # 내려온 블록 색깔 지정


# 게임 루프
def main():
    locked_positions = {}
    grid = create_grid(locked_positions) # 블록 위치 고정
    current_piece = Piece(5, 0, random.choice(shapes)) # 랜덤으로 모양을 골라 x좌표 5위치에 생성
    next_piece = Piece(5, 0, random.choice(shapes)) # 다음 조각도 랜덤으로 모양을 골라 x좌표 5위치에서 생성
    clock = pygame.time.Clock()
    fall_time = 0 # 떨어지는 속도 조절

    running = True
    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime() # 본래의 pygame이 가지고 있는 속도 + 본래 떨어지는 속도
        clock.tick() # 시간을 흐르게 함

        if fall_time / 1000 >= 0.27:  # 블록이 일정 시간마다 떨어짐
            fall_time = 0 # 디폴트 값
            current_piece.y += 1 # 오른쪽 아래로 갈 수록 + 값이 됨 -> 현재 조각을 한 칸 아래로 내리는 것
            if not valid_space(current_piece, grid) and current_piece.y > 0: # 블록 위치가 유효하지 않을 때
                current_piece.y -= 1 # 블록이 꽉차서 한 칸 올려야 함 -> 언젠가는 필연적으로 겹치기 때문에
                lock_positions(current_piece, grid, locked_positions) # 블록을 잠궈두기
                current_piece = next_piece
                next_piece = Piece(5, 0, random.choice(shapes))

                if not valid_space(current_piece, grid):
                    running = False  # 게임 종료

        for event in pygame.event.get(): # 키보드 좌표값
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid): # 블록 위치가 유호하지 않을 때
                        current_piece.y -= 1 # 블록이 겹치지 않도록 해주는 것
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid): # 블록 위치가 유호하지 않을 때
                        current_piece.rotation -= 1 # 블록이 겹치지 않도록 해주는 것

        # 그리드에 현재 블록 위치 업데이트
        for i in range(rows):
            for j in range(cols):
                pygame.draw.rect(
                    screen, grid[i][j], (j * block_size, i * block_size, block_size, block_size), 0)
                    # draw.rect : 사각형 그리기

        for pos in current_piece.get_blocks():
            x, y = pos
            if y > -1:
                pygame.draw.rect(screen, current_piece.color, (x *
                                 block_size, y * block_size, block_size, block_size), 0)

        pygame.display.update()

    pygame.quit()


# 게임 실행
if __name__ == "__main__":
    main()