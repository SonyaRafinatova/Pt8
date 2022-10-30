import sys
import pygame as pg
from pygame.sprite import Sprite
import time

from Alien_game.settings import GameSettings
from Alien_game.game_stats import GameStats


class Ship:
    """Класс для управления кораблем"""

    def __init__(self, ai_game):
        """Инициализация корабля и начальной позиции"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pg.image.load(r'images\StarShip.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        """Сохранение координаты центра корабля"""
        self.x = self.rect.x

        """Флаг перемещения"""
        self.move_right = False
        self.move_left = False

    def update(self):
        """Обновление позиции корабля с учетом флага"""
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.move_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        """Обновление значения х"""
        self.rect.x = float(self.x)

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещение корабля по центру"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


class Bullet(Sprite):
    """Класс для управления снарядами"""

    def __init__(self, ai_game):
        """Создает объект снарядов в текущей позиции корабля."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pg.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def draw_bullet(self):
        """Отрисовка снаряда на экране"""
        pg.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        """Перемещение снаряда вверх по экрану"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y


class Alien(Sprite):
    """Класс для создания пришельца"""

    def __init__(self, ai_game):
        """Инициализация пришельца и начального положения"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pg.image.load(r'images\alien.png')
        self.rect = self.image.get_rect()

        """Создание нового пришельца в левом верхнем углу экрана"""
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        """Перемещение пришельца вправо или влево"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Возвращвет True если пришелец у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


class AlienGame:
    """Класс для управления ресурсами игры"""

    def __init__(self):
        """Инциализация игры"""
        pg.init()

        self.settings = GameSettings()

        """Полноэкранный режим"""
        # self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.window_height = self.screen.get_rect().height

        """Оконный режим"""
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.window_height))
        pg.display.set_caption('Alien Game')

        self.stats = GameStats(self)
        self.ship = Ship(self)

        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()

        self._create_fleet()

    def _create_fleet(self):
        """Создание флота пришельцев"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        """Вычисление пришельцев по оси х"""
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_of_aliens_x = available_space_x // (2 * alien_width)

        """Вычисление рядов по оси y"""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.window_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_of_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_keydown_events(self, event):
        """Отслеживание нажатой клавиши"""
        if event.key == pg.K_RIGHT:
            """Перемещение корабля вправо"""
            self.ship.move_right = True
        elif event.key == pg.K_LEFT:
            """Переиещение корабля влево"""
            self.ship.move_left = True
        elif event.key == pg.K_q:
            """Завершение работы программы при нажатии на q"""
            sys.exit()
        elif event.key == pg.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """Создание нового снаряда и добавление его в группу"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keyup_events(self, event):
        """"Отслеживание прекращения зажатия клавиши"""
        if event.key == pg.K_RIGHT:
            """Прекращение перемещения корабля вправо"""
            self.ship.move_right = False
        elif event.key == pg.K_LEFT:
            """Прекращение перемещения корабля влево"""
            self.ship.move_left = False

    def _check_events(self):
        """Обработка нажатия клавиш и мыши"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        """Отрисовка последнего кадра"""
        pg.display.flip()

    def _update_bullet(self):
        self.bullets.update()
        """Удаление снарядов, вышедших за пределы экрана"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        collisions = pg.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            """Уничтожение снарядов и создание нового флота"""
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        self._check_fleet_edges()
        """Обновление позиции всех пришельцев"""
        self.aliens.update()

        """Обнаружение столкновения пришельцев с кораблем"""
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        """Проверка достижения низа экрана пришельцами"""
        self._check_aliens_bottom()

    def _change_fleet_direction(self):
        """Изменение неправления движения флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Проверка достижения флотом края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self):
        """Обработка столкновения пришельцев и корабля"""
        if self.stats.ship_lefts > 0:
            self.stats.ship_lefts -= 1

            """Очищение пришельцев и снарядов"""
            self.aliens.empty()
            self.bullets.empty()

            """Обновление корабля и флота"""
            self._create_fleet()
            self.ship.center_ship()

            time.sleep(2)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """Проверка достижения низа экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            """Отслеживание клавиатуры и мыши"""
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_aliens()

            self._update_screen()


if __name__ == "__main__":
    game = AlienGame()
    game.run_game()