from pygame import *
import os
import pyganim

# Размер платформ и цвет фона
PLATFORM_WIDTH = 32 
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#000000"
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

# Место хранения принцессы
ANIMATION_PRINCESS = [
            ('%s/img/princess_l.png' % ICON_DIR),
            ('%s/img/princess_r.png' % ICON_DIR)]

# Класс блоков на карте
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/img/platform.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

# Класс принцессы с анимацией
class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x,y)
        boltAnim = []
        for anim in ANIMATION_PRINCESS:
            boltAnim.append((anim, 0.5)) # Время обновления анимации
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        
    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
