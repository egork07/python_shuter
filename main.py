from pygame import*
from random import randint
from time import\
    time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.Font(None, 36)

back_img = "galaxy.jpg"
hero_img = "rocket.png"
enemy_img = 'ufo.png'
bullet_img = 'bullet.png'
ast_img = 'asteroid.png'

score = 0
lost = 0

win_width = 900
win_height = 600
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(back_img), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def rest(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(bullet_img, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 400)
            self.rect.y = 0
            lost += 1

bullets = sprite.Group()

ship = Player(hero_img, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(enemy_img, randint(80, win_width - 800), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(ast_img, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

finish = False
run = True

num_fire = 0
rel_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire +1
                    fire_sound.play()
                    ship.fire()
                if num_fire >=5 and rel_time ==False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))   

        text = font2.render('Рахунок:'+ str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущенно:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        win_img = "win_image.png"
        lose_img = "lose_image.png"

        win = transform.scale(image.load(win_img), (400, 200))
        lose = transform.scale(image.load(lose_img), (400, 200))

        life = 3
        max_lost = 3
        goal = 15

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.rest()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time <2:
                reload =font2.render('Wait, reload...', 4, (237, 5, 5))
                window.blit(reload, (350, 460))
            else:
                num_fire = 0
                rel_time =False


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score +1
            monster = Enemy(enemy_img, randint(80, win_width - 80,), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        collides_asteroids = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides_asteroids:
            score += 1  # You can adjust the score as needed
            asteroid = Enemy(ast_img, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))


        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()

    else:
        finish = False
        score =0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(enemy_img, randint(80, win_width - 800), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(ast_img, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)

    time.delay(50)
