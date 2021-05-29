from pygame import *
from random import randint
import json

 
#fonts and captions
font.init()
font1 = font.SysFont('Comic Sans', 60)
win = font1.render('Dam you actually poggers', True, (255, 255, 255))
lose = font1.render('Yeah you suck, you lost', True, (180, 0, 0))
font2 = font.SysFont('Comic Sans', 36)

ammo_lose = font1.render('You ran out of Ammo :(', True, (180, 0, 0))
#we need the following images:
img_back = "galaxy.jpg" #game background
img_hero = "rocket.png" #hero
img_bullet = "bullet.png" #bullet
img_enemy = "ufo.png" #enemy
img_powerup = "Ruby_Icon.png"
# very cool images yummy images
 
score = 0 #ships destroyed
lost = 0 #ships missed
max_lost = 3 #lose if you miss that many
 
#parent class for other sprites
class GameSprite(sprite.Sprite):
 #class constructor
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Call for the class (Sprite) constructor:
       sprite.Sprite.__init__(self)
 
       #every sprite must store the image property
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
       #every sprite must have the rect property that represents the rectangle it is fitted in
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #method drawing the character on the window
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
dday = 2
level = 1
#main player class
class Player(GameSprite):
   #method to control the sprite with arrow keys
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #method to "shoot" (use the player position to create a bullet there)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
 
#enemy sprite class  
class Enemy(GameSprite):
   #enemy movement
   def update(self):
       self.rect.y += self.speed
       global lost
       #disappears upon reaching the screen edge
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

#bullet sprite class  
class Bullet(GameSprite):
   #enemy movement
   def update(self):
       self.rect.y += self.speed
       #disappears upon reaching the screen edge
       if self.rect.y < 0:
           self.kill()
 
#Create a window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
powerups = sprite.Group()

for i in range(1, dday):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

 
bullets = sprite.Group()
 
#the finish variable: as soon as True is there, sprites stop working in the main loop
finish = False
#Main game loop:
run = True #the flag is reset by the window close button
score_req = 1
total_score = 0
ammo = 20
with open('best_score.json', "r") as f:
  data = json.load(f)
best_play = data["best_score"]

def restart():
  global score, lost, dday, level, score_req, ammo, best_play
  score = 0
  lost = 0
  text = font2.render("Score: " + str(score), 1, (255, 255, 255))
  window.blit(text, (10, 20))
  text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
  window.blit(text_lose, (10, 50))
  for i in bullets:
    i.kill()
  for i in monsters:
    i.kill()
  dday = dday + 1
  level += 1
  ammo += 20
  with open("best_score.json", "r") as f:
    data = json.load(f)
  best_play = data["best_score"]
  
  score_req = score_req + randint(1, 5)
  for i in range(1, dday):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

def update_stats_on_lose():
  global best_play, total_score, level, score_req, dday, ammo
  if best_play < total_score:
    best_play = total_score
    data["best_score"] = total_score
    with open('best_score.json', "w") as f:
      json.dump(data, f)
  total_score = 0
  level = 0
  score_req = 0
  dday = 1
  ammo = 0
  
while run:
   #"Close" button press event
   for e in event.get():
       if e.type == QUIT:
           run = False
       #event of pressing the space bar - the sprite shoots
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ammo -= 1
               ship.fire()
 
   if not finish:
       #update the background
       window.blit(background,(0,0))
 
       #write text on the screen
       text_level = font2.render("Level: " + str(level), 1, (255, 255, 255))
       window.blit(text_level, (10, 80))

       text_ammo = font2.render("Ammo: " + str(ammo), 1, (255, 255, 255))
       window.blit(text_ammo, (560, 10))

       text_highscore = font2.render("Best Score Ever: " + str(best_play), 1, (255, 255, 255))
       window.blit(text_highscore, (10, 140))

       text_score_overall = font2.render("Total Score: " + str(total_score), 1, (255,255,255))
       window.blit(text_score_overall, (10, 110))

       text = font2.render("This Level Score: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))

       spriteslist = sprite.groupcollide(
         monsters, bullets, True, True
       )

       spriteslist2 = sprite.groupcollide(
         powerups, bullets, True, True
       )

       if spriteslist2:
         amount_of_powerups_claimed += 1

       if ammo == 0:
         update_stats_on_lose()
         window.blit(ammo_lose, (10, 200))
         finish = True

       if spriteslist:
         score += 1
         total_score += 1
         monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
         monsters.add(monster)
         if score >= score_req:
           window.blit(win, (10, 200))
           finish = True
        
      
 
       text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))
       if lost >= 3:
         update_stats_on_lose()
         window.blit(lose, (10, 200))
         finish = True

 
       #launch sprite movements
       ship.update()
       monsters.update()
       bullets.update()
       powerups.update()
 
       #update them in a new location in each loop iteration
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       powerups.draw(window)
 
       display.update()
       if finish == True:
         time.delay(1000)
         restart()
         finish = False
   #the loop is executed each 0.05 sec
   time.delay(50)
