class GameSettings:
    """Класс для хранения настроек игры"""

    def __init__(self):
        """Инициализация настроек игры"""
        self.screen_width = 1200
        self.window_height = 800
        self.bg_color = (222, 222, 222)

        """Настройки корабля"""
        self.ship_speed = 1
        self.ship_limit = 3

        """Параметры снаряда"""
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 4

        """Настройки пришельцев"""
        self.alien_speed = 0.5
        self.fleet_drop_speed = 50
        self.fleet_direction = 1

# available_space_x = screen_width - (2 * alien_width)
# number_of_aliens = available_space_x // (2 * alien_width)