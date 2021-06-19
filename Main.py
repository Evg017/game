# Игра на PyGame
# Персонаж умеет бегать, прыгать, присутвует "анимация"
# Управление стрелками на клавиатуре

# Импорт
import pygame
from pygame import *
from player import *
from blocks import * 
from level import *

# Объявляем переменные
WIN_WIDTH = 1090 # Ширина создаваемого окна
WIN_HEIGHT = 780 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000" # Цвет фона   


def main():
    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Игра на PyGame") # Название приложения
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом
    
    hero = Player(190,700) # создаем героя по (x,y) координатам
    left = right = False # по умолчанию - стоим
    up = False
    
    entities = pygame.sprite.Group() # Все объекты
    platforms = [] # то, во что мы будем врезаться или опираться
    
    entities.add(hero)
       
    timer = pygame.time.Clock()
    x=y=0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    # то же самое и с высотой
        x = 0                   # на каждой новой строчке начинаем с нуля
    
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту
        
    while 1: # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit; "QUIT"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True


            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать 


        hero.update(left, right, up,platforms) # передвижение
        entities.draw(screen) # отображение     
        
        pygame.display.update()     # обновление и вывод всех изменений на экран
        
if __name__ == "__main__":
    main()
