import pygame as py
class Food(py.sprite.Sprite):
    def __init__(self, pos, food_type):
        super().__init__()

        self.food_sheet = py.image.load("Sprite/Food/general-food.png").convert_alpha()
        self.drinks_sheet = py.image.load("Sprite/Food/drinks.png").convert_alpha()
        self.sweets_sheet = py.image.load("Sprite/Food/sweets.png").convert_alpha()

        self.food_types = {
            # General-food
            "Pasta" : (self.food_sheet, py.Rect(0, 0, 16, 16)),
            "Tacos": (self.food_sheet, py.Rect(16, 0, 16, 16)),
            "Ramen": (self.food_sheet, py.Rect(32, 0, 16, 16)),
            "Hamdurg": (self.food_sheet, py.Rect(0, 16, 16, 16)),
            "Pizza": (self.food_sheet, py.Rect(16, 16, 16, 16)),
            "Rolls": (self.food_sheet, py.Rect(0, 32, 16, 16)),
            "Soup": (self.food_sheet, py.Rect(16, 32, 16, 16)),
            "Fried_egg": (self.food_sheet, py.Rect(32, 32, 16, 16)),
            # Drinks
            "Water": (self.drinks_sheet, py.Rect(0, 0, 16, 16)),
            "Cocoa": (self.drinks_sheet, py.Rect(16, 0, 16, 16)),
            "Tea": (self.drinks_sheet, py.Rect(0, 16, 16, 16)),
            "Milkshake": (self.drinks_sheet, py.Rect(16, 16, 16, 16)),
            "Coffe": (self.drinks_sheet, py.Rect(32, 16, 16, 16)),
            "Cocktail": (self.drinks_sheet, py.Rect(0, 32, 16, 16)),
            "Lemonade": (self.drinks_sheet, py.Rect(16, 32, 16, 16)),
            "Soda": (self.drinks_sheet, py.Rect(32, 32, 16, 16)),
            # Sweets
            "Cupcake": (self.sweets_sheet, py.Rect(0, 0, 16, 16)),
            "Cheesecake": (self.sweets_sheet, py.Rect(16, 16, 16, 16)),
            "Cake": (self.sweets_sheet, py.Rect(0, 32, 16, 16)),
            "Ice_cream": (self.sweets_sheet, py.Rect(16, 32, 16, 16)),
            "Pie": (self.sweets_sheet, py.Rect(32, 32, 16, 16)),
        }

