import sys

import pygame as pg

pg.init()  # инициализация pygame

FPS = 120
window_width = 600
window_height = 400

white = (255, 255, 255)
black = (0, 0, 0)
background_color = (70, 130, 180)

r = 20  # Радиус шарика

width_rect = 100  # Высота платформы
height_rect = 10  # Ширина платформы

x_ball, y_ball = 100, 200  # Положение шарика
direct_x_ball, direct_y_ball = 1, 1  # Перемещение шарика за один кадр

x_rect = (window_width // 2 - width_rect // 2)  # Положение платформы по оси x
y_rect = (window_height - height_rect)  # Положение платформы по оси y
direct_x_rect = 5  # Перемещение  платформы за один кадр

screen = pg.display.set_mode((window_width, window_height))

clock = pg.time.Clock()

score_count = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEMOTION:
            position = event.pos
            x_rect = position[0] - (width_rect // 2 )

    """Анимация"""
    clock.tick(FPS)
    screen.fill(background_color)

    ball = pg.draw.circle(screen, white, (x_ball, y_ball), r)
    pg.draw.line(screen, white, (window_width // 2, 0), (window_width // 2, window_height), 5)
    pg.draw.rect(screen, black, (x_rect, y_rect, width_rect, height_rect))
    """Перемещение"""
    x_ball += direct_x_ball
    if x_ball >= window_width - r or x_ball <= 0 + r:
        direct_x_ball = -direct_x_ball

    y_ball += direct_y_ball
    if y_ball <= 0 + r:
        direct_y_ball = -direct_y_ball

    if x_ball in range(x_rect, x_rect + width_rect) and y_ball + r in range(y_rect, y_rect + height_rect):
        direct_y_ball = -direct_y_ball
        score_count += 1
        FPS += 10

    if y_ball + r >= window_height:
        font_ = pg.font.SysFont('tahoma', 30)
        text = font_.render(f'Ваш счет: {score_count}', True, white)
        screen.blit(text, (225, 175))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_KP_ENTER:
                    x_ball, y_ball = 100, 50
                    score_count = 0
    pg.display.update()
