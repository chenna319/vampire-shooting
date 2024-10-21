
from settings import *
from player import Player
from sprites import *
from random import randint,choice
from pytmx.util_pygame import load_pygame
from groups import *



class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire-shooter')
        self.running = True
        self.clock = pygame.time.Clock()
        

        #enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event,300)
        self.spawn_positions = []

        

        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


        #audio
        self.shoot_music = pygame.mixer.Sound(join('audio','shoot.wav'))
        self.shoot_music.set_volume(0.4)
        self.impact_music = pygame.mixer.Sound(join('audio','impact.ogg'))
        self.game_music = pygame.mixer.Sound(join('audio','music.wav'))
        self.game_music.set_volume(0.3)
        self.game_music.play()
        
        
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_image = pygame.image.load(join('images','gun','bullet.png')).convert_alpha()

        folders = list(walk(join('images','enemies')))[0][1]
        
        self.enemy_frames = {}
        for folder in folders:
            for folder_path,_,file_names in walk(join('images','enemies',folder)):
                
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path,file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)
        
        
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            self.shoot_music.play()
            Bullet(self.bullet_image,pos,self.gun.player_direction,(self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if(current_time - self.shoot_time>self.gun_cooldown):
                self.can_shoot = True
    
    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collisons = pygame.sprite.spritecollide(bullet,self.enemy_sprites,False,pygame.sprite.collide_mask)
                if collisons:
                    self.impact_music.play()
                    for collision in collisons:
                        collision.destroy()
                    bullet.kill()
    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def setup(self):
        map = load_pygame(join('data','maps','world.tmx'))

        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite(image,(x*TILE_SIZE,y*TILE_SIZE),self.all_sprites)

        
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprites(obj.image,(obj.x,obj.y),  (self.all_sprites,self.collision_sprites))

        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprites(pygame.Surface((obj.width,obj.height)),(obj.x,obj.y), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y), self.all_sprites,self.collision_sprites)
                self.gun = Gun(self.player,self.all_sprites)
            else:
                self.spawn_positions.append((obj.x,obj.y))
    
    def run(self):
        while self.running:
            #delta time
            
            dt = self.clock.tick()/1000

            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
                if event.type == self.enemy_event:
                    Enemy(choice(list(self.enemy_frames.values())),choice(self.spawn_positions),self.player,(self.all_sprites,self.enemy_sprites),self.collision_sprites)

            #update
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()

            #draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()

