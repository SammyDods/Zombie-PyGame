import pygame
import os
from SpriteSheet import SpriteSheet
from Settings import SCREEN_HEIGHT, WHITE

class Player(pygame.sprite.Sprite):
    def __init__(self):
 
        super().__init__()
        width = 80
        height = 200
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.health = 100
        self.damage = 1
        self.suit = "marki"
        self.rect = self.image.get_rect()
 
        self.change_x = 0
        self.change_y = 0

        # This holds all the images for the animated walk left/right
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []
 
        # What direction is the player facing?
        self.direction = "R"
 
        # List of sprites we can bump against
        self.level = None
 
        sprite_sheet = SpriteSheet(os.path.join(os.path.dirname(__file__), "Assets", "Sprites" , "marki.png"))
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 80, 200)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(80, 0, 80, 200)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(160, 0, 80, 200)
        self.walking_frames_r.append(image)
       
 
        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 80, 200)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(80, 0, 80, 200)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(160, 0, 80, 200)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        
 
        # Set the image the player starts with
        self.image = self.walking_frames_r[0]
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        
    def update(self):
        # Gravity
        self.calc_grav()
        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]


 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0

    def findselfrect(self):
        return self.rectdw

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
    
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -12

    #movment
    def go_left(self):
        self.change_x = -6
        self.direction= "L"
 
    def go_right(self):
        self.change_x = 6
        self.direction= "R"

    #When player lets go
    def stop(self): 
        self.change_x = 0

    def take_damage(self, damage):
        self.health -= damage

    def change_suit(self, suit):

        self.suit = suit
        suits_damages = {"marki" : 1, "markii" : 10, "markiii" : 50}

        self.damage = suits_damages[suit]
        sprite_sheet = SpriteSheet(os.path.join(os.path.dirname(__file__), "Assets", "Sprites" , suit + ".png"))
        self.walking_frames_r.clear()
        self.walking_frames_l.clear()
        
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 80, 200)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(80, 0, 80, 200)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(160, 0, 80, 200)
        self.walking_frames_r.append(image)
           
        # Load all the right facing images, then flip them to face left.
        image = sprite_sheet.get_image(0, 0, 80, 200)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(80, 0, 80, 200)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(160, 0, 80, 200)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        
    