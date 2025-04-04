import pygame as py

class Food(py.sprite.Sprite):
    # Классовые переменные для хранения загруженных спрайт-листов
    _food_sheet = None
    _drinks_sheet = None
    _sweets_sheet = None
    _initialized = False

    @classmethod
    def init_resources(cls):
        """Инициализация ресурсов"""
        if not cls._initialized:
            cls._food_sheet = py.image.load("Sprite/Food/general-food.png").convert_alpha()
            cls._drinks_sheet = py.image.load("Sprite/Food/drinks.png").convert_alpha()
            cls._sweets_sheet = py.image.load("Sprite/Food/sweets.png").convert_alpha()
            cls._initialized = True

    def __init__(self, pos, food_type, scale, quantity=1, price=10):
        super().__init__()
        Food.init_resources()

        # Словарь с едой
        self.food_types = {
            # General-food
            "Pasta": (self._food_sheet, py.Rect(0, 0, 16, 16)),
            "Tacos": (self._food_sheet, py.Rect(16, 0, 16, 16)),
            "Ramen": (self._food_sheet, py.Rect(32, 0, 16, 16)),
            "Hamburg": (self._food_sheet, py.Rect(0, 16, 16, 16)),
            "Pizza": (self._food_sheet, py.Rect(16, 16, 16, 16)),
            "Rolls": (self._food_sheet, py.Rect(0, 32, 16, 16)),
            "Soup": (self._food_sheet, py.Rect(16, 32, 16, 16)),
            "Fried_egg": (self._food_sheet, py.Rect(32, 32, 16, 16)),

            # Drinks
            "Water": (self._drinks_sheet, py.Rect(0, 0, 16, 16)),
            "Cocoa": (self._drinks_sheet, py.Rect(16, 0, 16, 16)),
            "Tea": (self._drinks_sheet, py.Rect(0, 16, 16, 16)),
            "Milkshake": (self._drinks_sheet, py.Rect(16, 16, 16, 16)),
            "Coffee": (self._drinks_sheet, py.Rect(32, 16, 16, 16)),
            "Cocktail": (self._drinks_sheet, py.Rect(0, 32, 16, 16)),
            "Lemonade": (self._drinks_sheet, py.Rect(16, 32, 16, 16)),
            "Soda": (self._drinks_sheet, py.Rect(32, 32, 16, 16)),

            # Sweets
            "Cupcake": (self._sweets_sheet, py.Rect(0, 0, 16, 16)),
            "Cheesecake": (self._sweets_sheet, py.Rect(16, 16, 16, 16)),
            "Cake": (self._sweets_sheet, py.Rect(0, 32, 16, 16)),
            "Ice_cream": (self._sweets_sheet, py.Rect(16, 32, 16, 16)),
            "Pie": (self._sweets_sheet, py.Rect(32, 32, 16, 16)),
        }

        # Получаем спрайт из соответствующего листа
        sprite_sheet, frame = self.food_types.get(food_type, (self._food_sheet, py.Rect(0, 0, 16, 16)))
        self.image = sprite_sheet.subsurface(frame)
        self.rect = self.image.get_rect(center=pos)
        self.type = food_type
        self.collected = False

        # Масштабируем спрайт
        self.scale = scale
        if self.scale != 1:
            orig_size = self.image.get_size()
            self.image = py.transform.scale(
                self.image,
                (int(orig_size[0] * self.scale),
                 int(orig_size[1] * self.scale))
            )

        self.rect = self.image.get_rect(center=pos)
        self.type = food_type

        self.price = price
        self.quantity = quantity
        self.font = py.font.Font("Font/PixelizerBold.ttf", 20)

        # Загрузка только первого кадра монеты
        coin_sheet = py.image.load("Sprite/coins/coins.png").convert_alpha()
        self.coin_icon = coin_sheet.subsurface(py.Rect(0, 0, 16, 16))
        self.coin_icon = py.transform.scale(self.coin_icon, (24, 24))

        # Размеры фоновых прямоугольников
        self.price_bg = py.Surface((70, 28), py.SRCALPHA)
        self.price_bg.fill((0, 0, 0, 200))

        self.quantity_bg = py.Surface((40, 28), py.SRCALPHA)
        self.quantity_bg.fill((0, 100, 0, 200))

        self.update_ui()

    def update_ui(self):
        """Обновляет элементы интерфейса"""

        # Ценник
        self.price_text = self.font.render(str(self.price), True, (255, 255, 0))
        self.price_rect = self.price_text.get_rect(center=(25, 14))

        # Количество
        self.quantity_text = self.font.render(str(self.quantity), True, (255, 255, 255))
        self.quantity_rect = self.quantity_text.get_rect(center=(20, 14))

    def update_quantity_surface(self):
        """Обновляет поверхность с количеством"""
        self.quantity_surface = self.font.render(f"x{self.quantity}", True, (255, 255, 255))
        self.quantity_rect = self.quantity_surface.get_rect(
            midtop=(self.rect.centerx, self.rect.bottom + 5)
        )

    def draw(self, surface, camera_y=0):
        """Отрисовка с UI"""
        pos_y = self.rect.y - camera_y

        # Отрисовываем само блюдо
        surface.blit(self.image, (self.rect.x, pos_y))

        # Позиция ценника
        price_bg_pos = (self.rect.centerx - 35, pos_y + self.rect.height - 5)
        surface.blit(self.price_bg, price_bg_pos)
        surface.blit(self.price_text, (price_bg_pos[0] + self.price_rect.x,
                                       price_bg_pos[1] + self.price_rect.y))
        surface.blit(self.coin_icon, (price_bg_pos[0] + 40, price_bg_pos[1] + 2))

        # Позиция количества
        quantity_bg_pos = (self.rect.centerx - 20, pos_y - 25)
        surface.blit(self.quantity_bg, quantity_bg_pos)
        surface.blit(self.quantity_text, (quantity_bg_pos[0] + self.quantity_rect.x,
                                          quantity_bg_pos[1] + self.quantity_rect.y))
    def decrease_quantity(self):
        """Уменьшает количество на 1 и обновляет отображение"""
        self.quantity -= 1
        if self.quantity <= 0:
            self.kill()
        else:
            self.update_quantity_surface()

    def collect(self):
        """Вызывается при сборе еды"""
        self.collected = True
        self.kill()

    def is_clicked(self, pos, camera_y=0):
        """Проверяет, был ли клик по спрайту с учетом камеры"""
        adjusted_pos = (pos[0], pos[1] + camera_y)
        return self.rect.collidepoint(adjusted_pos)