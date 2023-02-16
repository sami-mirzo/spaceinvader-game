import pygame as pg, random, math

pg.init()
clock = pg.time.Clock()
FPS = 80


class Game():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((self.width,self.height))
        self.BG = pg.image.load("spr_space_himmel.png")
        self.run = True
        self.spaceshipe = Spaceshipe(self,370,515)
        self.score = 0

        self.enemies = []
        for i in range(12):
            self.enemies.append(Enemy(self, random.randint(0,736), random.randint(30,130)))

        self.items = []
        self.items.append(Item(self, random.randint(0,736), random.randint(-50,-50)))


        while self.run:
            clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
               # if pg.key.get_pressed()[pg.K_w]:
                #    self.spaceshipe.move(10)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.spaceshipe.move(-10)
                    if event.key == pg.K_RIGHT:
                        self.spaceshipe.move(10)
                    if event.key == pg.K_SPACE:
                        self.spaceshipe.fire_bullet()

                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT:
                        self.spaceshipe.move(10)
                    if event.key == pg.K_RIGHT:
                        self.spaceshipe.move(-10)

            self.screen.blit(self.BG, (0,0))
            self.spaceshipe.update()

            # Geschoss
            if len(self.spaceshipe.bullets) > 0:
                for bullet in self.spaceshipe.bullets:
                      if bullet.is_fired == True:
                        bullet.update()
                        if bullet.bullet_speed_item == True:
                            bullet.bullet_speed = 40
                      else:
                          self.spaceshipe.bullets.remove(bullet)

            # Enemys
            for enemy in self.enemies:
                enemy.update()
                enemy.check_collision()
                if enemy.y > 470:
                    for i in self.enemies:
                        i.y = 1000
                        self.game_over()

            # Items
            for i in self.items:
                i.update()
                i.check_collison()

# Jetzt wird kontrolliert ob hit == True ist, wenn ja, dann soll jetzt bullet_item() func. aufgerufen werden
                if i.hit == True:
                    for w in self.spaceshipe.bullets:
                        w.bullet_item()

                # Damit das Item verschwindet, wenn y > 460 ist
                if i.y > 470:
                    for items in self.items:
                        items.y = 600

                    # Weil ich das Objekt entfernt habe, hat es mit der Schleife nicht funktioniert
                      # also speed wird direkt wieder auf value gesetzt
                  #  else:
                   #     self.items.remove(i)

            self.print_score()
            pg.display.update()


    def game_over(self):
        game_over_font = pg.font.Font("freesansbold.ttf", 70)
        game_over_text = game_over_font.render("GAME OVER", True, (255,255,255))
        self.screen.blit(game_over_text, (200,250))

    def print_score(self):
        score_font = pg.font.Font("freesansbold.ttf", 22)
        score_text = score_font.render("Punkte " + str(self.score), True, (255,255,255))
        self.screen.blit(score_text, (8, 8))


class Spaceshipe():
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.change_x = 0
        self.schiff_img = pg.image.load("spr_spaceship.png")
        self.bullets = []

    def fire_bullet(self):
        self.bullets.append(Bullet(self.game, self.x, self.y))
        self.bullets[len(self.bullets) - 1].firer()

    def move(self, speed):
        self.change_x += speed

    def update(self):
        self.game.screen.blit(self.schiff_img, (self.x, self.y))
        self.x += self.change_x

        if self.x <= 0:
            self.schiff_collision_left()
        if self.x >= 736:
            self.schiff_collision_right()


# Collison links u. rechts
    def schiff_collision_left(self):
        self.x = 0

    def schiff_collision_right(self):
        self.x = 736

# BULLET
class Bullet():
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.bullet_img = pg.image.load("spr_patrone.png")
        self.is_fired = False
        self.bullet_speed = 10
        self.bullet_speed_item = False

    def firer(self):
        self.is_fired = True

    def bullet_item(self):
        self.bullet_speed_item = True

    def update(self):
        self.game.screen.blit(self.bullet_img, (self.x, self.y))
        self.y -= self.bullet_speed
        if self.y < 0:
            self.is_fired = False

# ENEMY
class Enemy():
    def __init__(self,game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.change_x = 5
        self.change_y = 60
        self.enemy_image = pg.image.load("spr_space_enemy.png")

    def check_collision(self):
        for bullet in self.game.spaceshipe.bullets:
            distance = math.sqrt(math.pow(self.x - bullet.x, 2) + math.pow(self.y - bullet.y, 2))
            if distance < 35:
                self.game.score +=1
                bullet.is_fired = False
                self.x = random.randint(0, 736)
                self.y = random.randint(50, 150)


    def update(self):
        self.game.screen.blit(self.enemy_image, (self.x, self.y))
        self.x += self.change_x

        if self.x >= 736:
            self.y += self.change_y
            self.change_x = -5
        elif self.x <= 0: # elif wird nur ausgeführt, wenn die obere if Anweisung nicht True ergibt
            self.y += self.change_y
            self.change_x = 5

# ITEMS
class Item():
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.health_img = pg.image.load("J_Ur_u.png")
        self.health_img = pg.transform.scale(self.health_img, (50, 50))
        self.change_y = 4.4
        self.hit = False

    def update(self):
        self.game.screen.blit(self.health_img, (self.x, self.y))
        self.y += self.change_y

    def check_collison(self):
        for item in self.game.spaceshipe.bullets:
            distance = math.sqrt(math.pow(self.x - item.x, 2) + math.pow(self.y - item.y, 2))
            if distance < 35:
                self.y = 1000
                self.hit = True



Game(width=800, height=600)




