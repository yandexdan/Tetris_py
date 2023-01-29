import pygame
from random import choice, randrange
from copy import deepcopy
import sys
import os
import random

pygame.init()
width, height = 10, 20
tile = 30
game_rise = width * tile, height * tile
size = 700, 600
v = 180
fps = 60


screen = pygame.display.set_mode(size)
screen_rect = (0, 0, size)
game_sc = pygame.Surface(game_rise)
pygame.init()

pygame.mixer.music.load('data/sound_start.mp3')

grid = [pygame.Rect(x * tile, y * tile, tile, tile) for x in range(width) for y in range(height)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + width // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, tile - 2, tile - 2)
field = [[0 for i in range(width)] for j in range(height)]

anim_count, anim_speed, anim_limit = 0, 60, 2000
figure = deepcopy(choice(figures))

main_font = pygame.font.Font('data/font.ttf', 65)
font = pygame.font.Font('data/font.ttf', 45)

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
next_figure_text = font.render('Next:', True, pygame.Color('red'))
title_record = font.render('record:', True, pygame.Color('purple'))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def get_color():
    return (randrange(30, 256),
            randrange(30, 256),
            randrange(30, 256))


start_screen = load_image('start_screen.png')
bg = load_image('bg.png')
game_bg = load_image('game_bg.png')


color, next_color = get_color(), get_color()

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500, 5: 2500}


def check_borders():
    if figure[i].x < 0 or figure[i].x > width - 1:
        return False
    elif figure[i].y > height - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record', 'r') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('start_screen.png'), size)
    screen.blit((fon), (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


GRAVITY = 1


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super()._init_(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
running = True
if __name__ == '__main__':
    bool = False
    count_bool = 0
    pygame.mixer.music.play(-1)
    start_screen()
    # игровой цикл
    while running:
        record = get_record()

        if bool:
            pygame.mixer.music.play(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and count_bool == 1:
                        bool = False
                        count_bool = 0
        else:
            mx, rotate = 0, False
            screen.blit(game_sc, (20, 20))
            screen.fill((0, 0, 0))
            for i in range(lines):
                pygame.time.wait(200)
            # фоны
            screen.blit(bg, (0, 0))
            screen.blit(game_sc, (0, 0))
            game_sc.blit(game_bg, (0, 0))

            # управление
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        mx = -1
                    elif event.key == pygame.K_SPACE and count_bool == 0:
                        bool = True
                        count_bool = 1
                    elif event.key == pygame.K_SPACE and count_bool == 1:
                        bool = False
                        count_bool = 0
                    elif event.key == pygame.K_RIGHT:
                        mx = 1
                    elif event.key == pygame.K_DOWN:
                        anim_limit = 100
                    elif event.key == pygame.K_UP:
                        rotate = True

            # перемещение фигуры по горизонтале
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].x += mx
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break

            # перемещение фигуры ро вертикали
            anim_count += anim_speed
            if anim_count > anim_limit:
                anim_count = 0
                figure_old = deepcopy(figure)
                for i in range(4):
                    figure[i].y += 1
                    if not check_borders():
                        for j in range(4):
                            field[figure_old[j].y][figure_old[j].x] = color
                        figure, color = next_figure, next_color
                        next_figure, next_color = deepcopy(choice(figures)), get_color()
                        anim_limit = 2000
                        break

            # вращение фигур
            center = figure[0]
            figure_old = deepcopy(figure)
            if rotate:
                for i in range(4):
                    x = figure[i].y - center.y
                    y = figure[i].x - center.x
                    figure[i].x = center.x - x
                    figure[i].y = center.y + y
                    if not check_borders():
                        figure = deepcopy(figure_old)
                        break

            # проверка линии
            line, lines = height - 1, 0
            for row in range(height - 1, -1, -1):
                count = 0
                for i in range(width):
                    if field[row][i]:
                        count += 1
                    field[line][i] = field[row][i]
                if count < width:
                    line -= 1
                else:
                    pos = 100, 0
                    create_particles(pos)
                    pos = 200, 0
                    create_particles(pos)
                    pos = 150, 0
                    create_particles(pos)
                    pos = 50, 0
                    create_particles(pos)
                    pos = 250, 0
                    create_particles(pos)
                    anim_speed += 3
                    lines += 1

            # начисляем очки
            score += scores[lines]

            # отрисовываем сетку
            for i in grid:
                pygame.draw.rect(screen, (50, 50, 50), i, 1)

            # отрисовываем фигуры
            for i in range(4):
                figure_rect.x = figure[i].x * tile
                figure_rect.y = figure[i].y * tile
                pygame.draw.rect(screen, color, figure_rect)

            # отрисовываем упавшие фигуры
            for y, raw in enumerate(field):
                for x, col in enumerate(raw):
                    if col:
                        figure_rect.x, figure_rect.y = x * tile, y * tile
                        pygame.draw.rect(screen, col, figure_rect)

            # отрисовываем следующию фигуру
            for i in range(4):
                figure_rect.x = next_figure[i].x * tile + 380
                figure_rect.y = next_figure[i].y * tile + 140
                pygame.draw.rect(screen, next_color, figure_rect)

            # отрисовываем надпись
            screen.blit(title_tetris, (350, 0))
            screen.blit(next_figure_text, (350, 150))
            screen.blit(title_score, (350, 500))
            screen.blit(font.render(str(score), True, pygame.Color('white')), (490, 500))
            screen.blit(title_record, (350, 400))
            screen.blit(font.render(str(record), True, pygame.Color('white')), (510, 400))

            # провиряем рекорд и обнуляем поле
            for i in range(width):
                if field[0][i]:
                    set_record(record, score)
                    field = [[0 for i in range(width)] for i in range(height)]
                    anim_count, anim_speed, anim_limit = 0, 60, 2000
                    score = 0
                    # заставка проигрыша
                    for i_rect in grid:
                        pygame.draw.rect(game_sc, get_color(), i_rect)
                        screen.blit(game_sc, (0, 0))
                        pygame.display.flip()
                        clock.tick(200)

            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(fps)