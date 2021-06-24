from pygame import *
import pyganim # Для использования анимаций
import os
import blocks

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR =  "#000000"
JUMP_POWER = 10
GRAVITY = 0.50 # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.05 # скорость смены кадров
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_RIGHT = [('%s/img/r1.png' % ICON_DIR),
            ('%s/img/r2.png' % ICON_DIR),
            ('%s/img/r3.png' % ICON_DIR),
            ('%s/img/r4.png' % ICON_DIR),
            ('%s/img/r5.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/img/l1.png' % ICON_DIR),
            ('%s/img/l2.png' % ICON_DIR),
            ('%s/img/l3.png' % ICON_DIR),
            ('%s/img/l4.png' % ICON_DIR),
            ('%s/img/l5.png' % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/img/jl.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/img/jr.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/img/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/img/0.png' % ICON_DIR, 0.1)]

# Класс о главном персонаже
# Скорость движения, анимации перемещения главного героя
class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   # Скорость перемещения. 0 - стоять на месте
        self.yvel = 0 # Скорость вертикального перемещения
        self.onGround = False # Проверка, на земле ли я?
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # Прямоугольный объект
        self.image.set_colorkey(Color(COLOR)) # Делаем фон прозрачным

        # Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        # Анимация движения влево        
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0)) # По умолчанию, стоим
        
        self.boltAnimJumpLeft= pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()
        
        self.boltAnimJumpRight= pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()
        
        self.boltAnimJump= pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()
        self.winner = False 


    def update(self, left, right, up, platforms):
        # Прыжок
        if up:
            if self.onGround: # Прыгаем, только тога, когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))
               
        # Движение налево               
        if left:
            self.xvel = -MOVE_SPEED # Лево = x - n
            self.image.fill(Color(COLOR))
            if up: # Для прыжка влево отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))
        
        # Движение направо
        if right:
            self.xvel = MOVE_SPEED # Право = x + n
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))
         
        if not(left or right): # Стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))
            
        if not self.onGround:
            self.yvel +=  GRAVITY
            
        self.onGround = False; # Мы не знаем, когда мы на земле   
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)
   
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
                if isinstance(p, blocks.Princess): # если коснулись принцессы
                       self.winner = True # победили!!!
                else:
                    if xvel > 0:                      # если движется вправо
                        self.rect.right = p.rect.left # то не движется вправо

                    if xvel < 0:                      # если движется влево
                        self.rect.left = p.rect.right # то не движется влево

                    if yvel > 0:                      # если падает вниз
                        self.rect.bottom = p.rect.top # то не падает вниз
                        self.onGround = True          # и становится на что-то твердое
                        self.yvel = 0                 # и энергия падения пропадает

                    if yvel < 0:                      # если движется вверх
                        self.rect.top = p.rect.bottom # то не движется вверх
                        self.yvel = 0                 # и энергия прыжка пропадает