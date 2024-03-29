import pygame
from random import *
from os.path import join as join_path, dirname

from Player import Player
from Level_01 import Level_01
from Bullet import Bullet
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH
from Settings import WHITE, GREEN, YELLOW, LIGHT_GREEN, LIGHT_YELLOW

from Gui import start, pause, wavescore, endgamescreen

#pygame.mixer.pre_init(44100,6,2,4096)
pygame.init()

# Set the height and width of the screen
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode((size),pygame.FULLSCREEN) 
pygame.display.set_caption("Zombinator")

#icon = pygame.image.load("apple.png")       
#pygame.display.set_icon(icon)

# Global constants
clock = pygame.time.Clock()
#Suits
starter = 0

#VARIABLES
buildingshop = False
sateliteshop = False
q = False 
done1=0
money=0
Building_list = [0,0]
zombie_list=[0,0]
zombie_list= pygame.sprite.Group()
buildingshopopener = None
num_banks = 0
banking = 0
suit = starter
playerhealth = 1
wave = 0
cooltext=""
starttimer= 150000

#newbackground = pygame.image.load("Assets\Sprites\background.png").convert()
bankimage = pygame.image.load(join_path(dirname(__file__), "Assets", "Sprites" ,"bank.png")).convert_alpha()
bankimage = pygame.transform.scale(bankimage,(350,350))
wallimage = pygame.image.load(join_path(dirname(__file__), "Assets", "Sprites" ,"Wall.png")).convert_alpha()
wallimage = pygame.transform.scale(wallimage,(350,350))
lasersound = pygame.mixer.Sound(join_path(dirname(__file__), "Assets", "Audio" ,"laser.wav"))

bankimage = pygame.image.load(join_path(dirname(__file__), "Assets", "Sprites" ,"bank.png")).convert_alpha()
bankimage = pygame.transform.scale(bankimage,(350,350))
wallimage = pygame.image.load(join_path(dirname(__file__), "Assets", "Sprites" ,"Wall.png")).convert_alpha()
wallimage = pygame.transform.scale(wallimage,(350,350))

player = Player()


def main():
    pygame.init()
    global bullet_list
    global zombie_list
    global zombie_list

    # --- Sprite lists
    # This is a list of every sprite. All blocks and the player block as well.

    # List of each block in the game
    zombie_list= pygame.sprite.Group()
    zombie_list = pygame.sprite.Group()
    
    # List of each bullet
    bullet_list = pygame.sprite.Group()
 
    # --- Create the sprites

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode((size),pygame.FULLSCREEN) 
    screen.fill(WHITE)
    pygame.display.set_caption("ZOMBINATOR")
    
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 2500
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
     
    # Loop until the user clicks the close button.
    done = False
     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()


    #Background music
    pygame.mixer.music.load(join_path(join_path(__file__), "Assets", "Audio" , join_path(dirname(__file__), "Assets", "Audio" ,"ChasingGhosts.mp3")))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    startingnow = True
     
    # -------- Main Program Loop -----------
    start1=True
    reload = 15
    wave = 1
    banking = 0
    while not done:
        # --- Event Processing

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                    buildingshop = False
                    sateliteshop = False
                if event.key == pygame.K_d:
                    player.go_right()
                    buildingshop=False
                    sateliteshop = False
                if event.key == pygame.K_w:
                    player.jump()
                    buildingshop=False
                    sateliteshop=False
                if event.key == pygame.K_p:
                    pause()

                if event.key == pygame.K_q:
                    q = True
                else:
                    q = False
                    

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                    buildingshop=False
                    sateliteshop = False

                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop()
                    buildingshop=False
                    sateliteshop=False
            click = pygame.mouse.get_pressed()
            #elif event.type == pygame.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button
            if click[0] == 1 and reload <=0:
                print(player.damage)
                lasersound.play()
                reload= 15
                # Get the mouse position
                pos = pygame.mouse.get_pos()
     
                mouse_x = pos[0]
                mouse_y = pos[1]
     
                # Create the bullet based on where we are, and where we want to go.
                bullet = Bullet(player.rect.x, player.rect.y+50, mouse_x, mouse_y)
                # Add the bullet to the lists
                active_sprite_list.add(bullet)
                bullet_list.add(bullet)
        cur = pygame.mouse.get_pos()


        # --- Game logic

        
        reload -= 1
        # Call the update() method on all the sprites
        #Calles wave function when there are no zombies
        #print(zombie_list.sprites())
        if not zombie_list.sprites():
            #print(zombie_list.sprites())
            wave+=1
            level_01=Level_01(player)
            level_01.wavefunc(wave, zombie_list)
            #print("it worked?!")
        if startingnow == True:
            startingnow=False
            start(gameDisplay)
        active_sprite_list.update()
     
        # Calculate mechanics for each bullet
        for bullet in bullet_list:
            # See if it hit a block
            zombie_hit_list = pygame.sprite.spritecollide(bullet, zombie_list, False)
            # For each block hit, remove the bullet and add to the score
            for zombie in zombie_hit_list:
                zombie.take_damage(player.damage)
                if zombie.is_dead():
                    zombie.die()
                    zombie_list.remove(zombie)
                    money+=10+wave*10
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)
            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)

        #calculate zombbie collisions
        for zombie in zombie_list:
            hit = pygame.sprite.collide_rect(zombie, player)
            if hit:
                zombie.attack(player)
            
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 1020:
            diff = player.rect.right - 1020
            player.rect.right = 1020
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 900:
            diff = 900 - player.rect.left
            player.rect.left = 900
            current_level.shift_world(diff)
         
        # --- Draw a frame
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()

        #banks
        banking += 2*num_banks
        if banking >= 30:
            money+=2
            banking= 0

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

                
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        # Draw all the spites
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        
        zombie_list.draw(screen)


        """
        if buildingshop == True:
            button("Buy wall (350)", 650,500,200,100, LIGHT_GREEN, GREEN, action="buywall")
            button("Buy bank (450)", 1110,500,200,100, YELLOW, LIGHT_YELLOW, action="buybank")

        if sateliteshop == True:
            button("Buy Mark II (1000)", 600,500,300,100, LIGHT_GREEN, GREEN, action="buymark2")
            button("Buy Mark III (5000)", 1150,500,300,100, YELLOW, LIGHT_YELLOW, action="buymark3")

        #score
        moneyscore(money)
        """
        wavescore(wave)
            
        #if game ends     
        if playerhealth <= 0:
            endgamescreen()

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # --- Limit fps
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'on exit. 
    pygame.quit()

if __name__ == "__main__":
    main()
