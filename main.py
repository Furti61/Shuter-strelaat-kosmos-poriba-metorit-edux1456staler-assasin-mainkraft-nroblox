from pygame import *
from random import *
from time import time as timer
a = 0

window = display.set_mode((1600, 800))
display.set_caption('  ')
background = transform.scale(image.load('background.jpg'), (1600, 900))


class GameBaikal(sprite.Sprite):
    def __init__(self, picture, x, y, speed, widht, height):
        super().__init__()
        self.image = transform.scale(image.load(picture), (widht, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(GameBaikal):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Hero(GameBaikal):
    def fire(self):
        if a == 0:
            bulled = Bullet('ammo.png', self.rect.centerx, self.rect.top, -60, 5, 10)
            bullets.add(bulled)
        if a == 1:
            bulled = Bullet('big_ammo.png', self.rect.centerx, self.rect.top, -60, 20, 100)
            bullets.add(bulled)

    def update(self):
        keys_pressed = key.get_pressed()
        global a
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= 10
        if keys_pressed[K_d] and self.rect.x < 1600 - 105:
            self.rect.x += 10
        if keys_pressed[K_LSHIFT]:
            self.speed += 20
        if not keys_pressed[K_LSHIFT]:
            self.speed -= 20
        if keys_pressed[K_r]:
            a = 0
        if keys_pressed[K_t]:
            a = 1


lost = 0

num_fire = 0
rel_time = False

class NoEmeny(GameBaikal):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 800:
            lost += 1
            self.rect.y = 0
            randomick = randint(0, 1800 - 65)
            self.rect.x = randomick


font.init()

font = font.Font(None, 70)

hero = Hero("hero.png", 100, 700, 86, 65, 80)

bullets = sprite.Group()

e1 = NoEmeny("enemy.png", randint(0, 1800 - 65), 0, randint(1, 3), 65, 80)
e2 = NoEmeny("enemy.png", randint(0, 1800 - 65), 0, randint(1, 3), 65, 80)
e3 = NoEmeny("enemy.png", randint(0, 1800 - 65), 0, randint(1, 3), 65, 80)
e4 = NoEmeny("enemy.png", randint(0, 1800 - 65), 0, randint(1, 3), 65, 80)
e5 = NoEmeny("enemy.png", randint(0, 1800 - 65), 0, randint(1, 3), 65, 80)

f1 = NoEmeny("friend.png", randint(0, 1800 - 65), 0, randint(2, 5), 65, 80)
f2 = NoEmeny("friend.png", randint(0, 1800 - 65), 0, randint(2, 5), 65, 80)
f3 = NoEmeny("friend.png", randint(0, 1800 - 65), 0, randint(2, 5), 65, 80)

monsters = sprite.Group()
monsters.add(e1)
monsters.add(e2)
monsters.add(e3)
monsters.add(e4)
monsters.add(e5)

friends = sprite.Group()
friends.add(f1)
friends.add(f2)
friends.add(f3)




win = font.render('You Win', 1, (255, 0, 105))
fals = font.render('You Lose', 1, (255, 0, 105))
loset = font.render("Пробежало" + str(lost), 1, (255, 255, 255))
kills = 0

finish = False
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
fire = mixer.Sound('fire.ogg')
game = True
clock = time.Clock()
FPS = 300
nn = 0
abv = 10



while game == True:
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    hero.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

        if e.type == KEYUP:
            pass

    if finish != True:

        sprite_list = sprite.groupcollide(bullets, monsters, True, True)
        for e in sprite_list:
            if a == 0:
                kills += 1
                abv -= 1

        sprite_list = sprite.groupcollide(bullets, friends, True, True)
        if sprite_list:
            finish = True
            window.blit(fals, (800, 400))

        if sprite.spritecollide(hero, monsters, False):
            finish = True
            window.blit(fals, (800, 400))

        if sprite.spritecollide(hero, friends, False):
            finish = True
            window.blit(fals, (800, 400))

        if lost > 25:
            finish = True
            window.blit(fals, (800, 400))

        if abv <= 5:
            for i in range(5):
                e = NoEmeny("enemy.png", randint(0, 1800 - 65), 0, randint(2, 7), 65, 80)
                monsters.add(e)
                abv = 7

        hero.reset()
        hero.update()

        monsters.draw(window)
        monsters.update()

        friends.draw(window)
        friends.update()

        bullets.draw(window)
        bullets.update()

        if rel_time == True:
            num_fire = timer()

            if num_fire - last_time < 3:
                reload = font.render('Перезарядка', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        loset = font.render("Пробежало: " + str(lost), 1, (255, 255, 255))
        kill = font.render("Убито: " + str(kills), 1, (255, 255, 255))
        window.blit(loset, (20, 20))
        window.blit(kill, (20, 80))

        clock.tick(FPS)
        display.update()
