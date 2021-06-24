# Игра на PyGame
# Персонаж умеет бегать, прыгать, присутвует "анимация"
# Для победы надо найти принцессу
# Управление стрелками на клавиатуре

# Импорт
import pygame
from pygame import *
from player import *
from blocks import * 
from level import *

# Объявляем переменные
WIN_WIDTH = 1280 # Ширина создаваемого окна
WIN_HEIGHT = 720 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000" # Цвет фона   

# Класс, отвечающий за движение камеры
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
        
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)

def main():
    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окно приложения
    pygame.display.set_caption("Игра на PyGame") # Название приложения
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности будет использоваться как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом
    
    hero = Player(190,700) # Создаем героя по (x,y) координатам
    left = right = False # По умолчанию - стоим
    up = False
    
    entities = pygame.sprite.Group() # Все объекты
    platforms = [] # То, во что мы будем врезаться или опираться
    
    entities.add(hero)
       
    timer = pygame.time.Clock()
    x=y=0 # Координаты
    for row in level: # Вся строка
        for col in row: # каждый символ
            if col == "-":  # Блоки
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)
            if col == "P": # Принцесса
                pr = Princess(x,y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)

            x += PLATFORM_WIDTH # Блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    # То же самое и с высотой
        x = 0                   # На каждой новой строчке начинаем с нуля
    
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # Высоту
    
    camera = Camera(camera_configure, total_level_width, total_level_height) 
            
    while not hero.winner: # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit; "QUIT"
            # Привязка к кнопкам на клавиатуре
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

        screen.blit(bg, (0,0)) # Каждую итерацию необходимо всё перерисовывать 
        animatedEntities.update() # Показываеaм анимацию 
        camera.update(hero) # Центризируем камеру относительно персонажа
        hero.update(left, right, up,platforms) # Передвижение
        for e in entities:
            screen.blit(e.image, camera.apply(e))   
        pygame.display.update()     # Обновление и вывод всех изменений на экран
animatedEntities = pygame.sprite.Group() # Все анимированные объекты, за исключением героя     
if __name__ == "__main__":
    main()
