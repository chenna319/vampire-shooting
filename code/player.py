from settings import * 

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,collision_sprite):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_ind = 'down', 0
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.collision_sprite = collision_sprite
        self.hitbox_rect = self.rect.inflate(-70,-90)

        #movement
        self.direction = pygame.Vector2()
        self.speed = 500
        

    def load_images(self):
        self.frames = {'left':[], 'right':[], 'up':[], 'down':[]}
        for state in self.frames.keys():
            for folder_path, sub_folder, file_names in walk(join('images','player',state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path,file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)
    
    def move(self,dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collison('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collison('vertical')
        self.rect.center = self.hitbox_rect.center

    def collison(self,direction):
        for sprite in self.collision_sprite:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0 : self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0 : self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def animate(self,dt):

        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        self.frame_ind = self.frame_ind + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_ind)%len(self.frames[self.state])]

    def update(self,dt):
        self.move(dt)
        self.input()
        self.animate(dt)