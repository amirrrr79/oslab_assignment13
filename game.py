import arcade
import random
import time
import math
import threading

WIDTH=800
HEIGHT=600

class spaceship(arcade.Sprite):
    def __init__(self):
        super().__init__('playerShip2_orange.png')
        self.width=48
        self.height=48
        self.score=0
        self.helth=3
        self.center_x=WIDTH//2
        self.center_y=32
        self.angle=0
        self.change_angle=0 
        self.speed=6
        self.bullet_list=[]
        self.fire_sound=arcade.load_sound('arcade_resources_sounds_laser2.wav')
        
    
    def fire(self):
        self.bullet_list.append(Bullet(self))
        arcade.play_sound(self.fire_sound)
    
    def rotate(self):
        self.angle +=self.speed*self.change_angle
    
            


class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__('enemy.png')
        self.width=48
        self.height=48
        self.center_x=random.randint(0,WIDTH)
        self.center_y=HEIGHT+self.height//2
        self.speed=2
        self.enemy_list=[]
    
    
    def move(self):
        self.center_y-=self.speed
            
        
        
class Bullet(arcade.Sprite):
    def __init__(self,host):
        super().__init__('laserRed01.png')
        self.center_x=host.center_x
        self.center_y=host.center_y
        self.speed=6
        self.angle=host.angle
    
    
    
    def move(self):
        a=math.radians(self.angle)
        self.center_x -=self.speed*math.sin(a)
        self.center_y +=self.speed*math.cos(a)  
    
class game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH,HEIGHT,'Interrstallar')
        self.background = arcade.load_texture('space.png')
        self.me=spaceship()
        self.enemy_list=[]
        self.enemy_time=random.randint(4,8)
        self.speed_enemy=0.1
        self.hit_sound=arcade.load_sound('hit.wav')
        self.point_sound=arcade.load_sound('Silver-Spacecraft_sfx_point.wav')
        self.helth_image = arcade.load_texture('helth.png')
        self.gameover_imaga=arcade.load_texture('gameover.jpg')
        self.my_threed=threading.Thread(target=self.add_enemy)
        self.my_threed.start()
        
        
        
    def add_enemy(self):
        while True:
          self.enemy_list.append(Enemy())
          time.sleep(self.enemy_time)
          
          
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(400,300,800,600,self.background)
        arcade.draw_text('Score: ' + str(self.me.score), self.width-100, 10, arcade.color.WHITE, 20, width=200)
        for i in range(self.me.helth):
                arcade.draw_xywh_rectangle_textured(10+i*35 ,10 ,30 ,30 ,self.helth_image)
        self.me.draw()
        for enemy in self.enemy_list:
            enemy.draw()
        for b in self.me.bullet_list:
            b.draw()
    def on_update(self):    
        self.me.rotate()
    
        for enemy in self.enemy_list:
            enemy.move()
            if enemy.center_y < 0:
                self.enemy_list.remove(enemy)
                self.me.helth -=1 
                
                
        if self.me.helth<1:
            arcade.draw_xywh_rectangle_textured(0,0,WIDTH,HEIGHT,self.gameover_imaga)
            
            
        for b in self.me.bullet_list:
            b.move()   
            if b.center_y > HEIGHT or b.center_x>WIDTH or b.center_x<0 :
                self.me.bullet_list.remove(b)
                    

        for enemy in self.enemy_list:
                for b in self.me.bullet_list:
                    if arcade.check_for_collision(b, enemy):
                        arcade.play_sound(self.hit_sound)
                        self.me.bullet_list.remove(b)
                        self.enemy_list.remove(enemy)
                        self.me.score += 1
                        arcade.play_sound(self.point_sound)
        
            
                          
        
        
    def on_key_press(self, symbol: int, modifiers: int):
         if symbol== arcade.key.LEFT:
             self.me.center_x-=30
         if symbol==arcade.key.RIGHT:
             self.me.center_x+=30  
         if symbol==arcade.key.SPACE:
             self.me.fire()     
         if symbol==arcade.key.A:
             self.me.change_angle=1
         if symbol==arcade.key.D:
             self.me.change_angle=-1    
                  
    def on_key_release(self, symbol: int, modifiers: int):
        self.me.change_angle=0              
        
        
        
        
play_game=game()
arcade.run()           
                