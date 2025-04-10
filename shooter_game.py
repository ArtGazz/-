#создай игру "Лабиринт" ! 
from pygame import *
from random import randint

# вынесем размер окна в константы для удобства
# W - width, ширина
# H - height, высота
WIN_W = 700
WIN_H = 500

size = 80

x1 = 100
x2 =200
y1 =400
y2 =0

speed = 5
FPS = 60

RED =  255, 0, 0
GREEN =0, 255, 0
BLACK = 255, 255, 255

UFOS = 10

font.init()
title_fint = font.SysFont('arial', 70)
win = title_fint.render('ПОБЕДА', True , GREEN )
lose = title_fint.render('ПОРОЖЕНИЕ', True, RED)

label_fint = font.SysFont('arial', 14)
schetchik_txt = label_fint.render('счётчик', True , GREEN )
ubezalo_txt = label_fint.render('пропущено', True, RED)



class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h):
        super().__init__()
        self.image = transform.scale(
            image.load(img),
            # здесь - размеры картинки
            (w, h)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, img, x, y, w, h, speed=speed):
        super().__init__(img,x,y,w,h)
        self.speed = speed
        self.ubezalo = 0
        self.schetchik = 0
        self.bullets = sprite.Group()

    def update(self, up, down, left, right):
        keys_pressed = key.get_pressed()

        if keys_pressed[right] and self.rect.x < WIN_W - size:
            self.rect.x += speed

        if keys_pressed[left] and self.rect.x >5:
            self.rect.x-= speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + self.rect.width / 2, self.rect.y, 5,15)
        self.bullets.add(bullet)
class Enemy(GameSprite):
    def __init__(self, img, x, y, w, h, speed=speed):
        super().__init__(img,x,y,w,h)
        self.speed = speed
        self.rect.x = randint(0, WIN_W - self.rect.width)
        self.rect.y = randint(0, 40)
    def update(self, rocket, is_ufo = True) :
        if self.rect.y >= WIN_H:
            rocket.ubezalo += 1
            self.rect.x = randint(0, WIN_W - self.rect.width)
            self.rect.y = randint(0, 40)
        self.rect.y += self.speed

class Bullet(GameSprite):  
    def __init__(self, img, x, y, w, h, speed=speed):
        super().__init__(img,x,y,speed,size)
        self.speed = speed

    def update(self):
        if self.rect.y <= 0:
            self.kill()
        self.rect.y -= self.speed
# создание окна размером 700 на 500
window = display.set_mode((WIN_W, WIN_H))

clock = time.Clock()

# название окна
display.set_caption("шутер")

font.init()
title_fint = font.SysFont('arial', 70)
win = title_fint.render('ПОБЕДА', True , GREEN )
lose = title_fint.render('ПОРОЖЕНИЕ', True, RED)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.01)

fire = mixer.Sound('fire.ogg')


# задать картинку фона такого же размера, как размер окна

galaxy_s25_ultra = GameSprite('galaxy.jpg', 0,0, WIN_W, WIN_H)


ufos = sprite.Group()
for i in range(UFOS):
    enemy = Enemy('ufo.png', 0,0, 123, 12, 2)
    ufos.add(enemy)
rocket = Player('rocket.png', x1,y1, 12, 123, 5)
#b = Player('sprite2.png', x2,y2, size, size)
finish = False
# игровой цикл
game = True
while game:
    if not finish:
        galaxy_s25_ultra.draw(window)
        rocket.draw(window)

        if sprite.spritecollide(rocket, ufos, False):
            window.blit(lose, (100, 200))
            display.update()
            finish = True

        schetchik = label_fint.render(str(rocket.schetchik), True , GREEN )
        ubezalo = label_fint.render(str(rocket.ubezalo), True, RED)
        
        window.blit(schetchik_txt, (10, 10))
        window.blit(schetchik, (50, 10))
        window.blit(ubezalo_txt, (0, 30))
        window.blit(ubezalo, (80, 30))

        ufo_vs_pula = sprite.groupcollide(
            ufos, rocket.bullets, True, True
        )
        for colide in ufo_vs_pula:
            rocket.schetchik +=1
            enemy = Enemy('ufo.png', 0,0, 123, 12)
            ufos.add(enemy)


        rocket.update(K_w, K_s, K_a, K_d)
        ufos.draw(window)
        ufos.update(rocket)
        
        rocket.bullets.draw(window)
        rocket.bullets.update()

        if rocket.ubezalo  >= 20:
            window.blit(lose, (100, 200))
            display.update()
            finish = True
        if rocket.schetchik >= 16:
            window.blit(win, (100, 200))
            display.update()
            finish = True
    for e in event.get():
        # выйти, если нажат "крестик"
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire()
                rocket.fire()

    display.update()
    clock.tick(FPS)
    # обновить экран, чтобы отобрзить все изменения
    

#создай окно игры

#задай фон сцены

#создай 2 спрайта и размести их на сцене

#обработай событие «клик по кнопке "Закрыть окно"»
