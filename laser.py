import pygame
import random, math
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)

class Laser(pygame.sprite.Sprite):
    def __init__(self, color, x1, y1, x2, y2):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([math.fabs(x2-x1), math.fabs(y2-y1)])
        self.image.fill(white)
        self.image.set_colorkey(white)
        
        pygame.draw.line(self.image, white, (x1, y1), (x2,y2), 1)
        pygame.draw.line(screen, red, (x1, y1), (x2,y2), 1)     
        self.rect=self.image.get_rect()

#class represents the ball        
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    
    # laser angle
    angle = 0.1#random.randrange(360)
    rate = 0.01 #degrees per frame
    
    #speed of approach
    speed = 2.0
    
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
 
# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width=700
screen_height=400
screen=pygame.display.set_mode([screen_width,screen_height])
 
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'
block_list = pygame.sprite.RenderPlain()
 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.RenderPlain()
 
for i in range(20):
    # This represents a block
    block = Block(black, 20, 20)
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
     
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)
     
     
 
# Create a red player block
player = Block(red, 20, 20)
all_sprites_list.add(player)

#laser list
lasers=pygame.sprite.RenderPlain()


#Loop until the user clicks the close button.
done=False
 
# Used to manage how fast the screen updates
clock=pygame.time.Clock()
 
score = 0
 
# -------- Main Program Loop -----------
while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
    # Clear the screen
    screen.fill(white)
 
    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    pos = pygame.mouse.get_pos()
     
    # Fetch the x and y out of the list, 
       # just like we'd fetch letters out of a string.
    # Set the player object to the mouse location
    player.rect.x=pos[0]
    player.rect.y=pos[1]
    
    lasers.empty()
    for i in block_list:
        angle = math.atan2(-(i.rect.y - pos[1]), -(i.rect.x - pos[0]))
        i.rect.x += i.speed*math.cos(angle)
        i.rect.y += i.speed*math.sin(angle)
        print math.cos(angle)
        delta = angle-i.angle
        if delta <= 0:
            delta += math.pi*2
        
        if delta < math.pi:
            i.angle += i.rate*(delta+math.pi)
        else:
            i.angle -= i.rate*(delta)
         
        #bring i.angle to \/
        i.angle = math.atan2(math.sin(i.angle),math.cos(i.angle))
        #angle is -0 to -pi for 0 to 180 and 0 to pi for -0 to -180

        #print str(angle) +" "+str(i.angle)
        lasers.add(Laser(red, i.rect.x+10, i.rect.y+10, pos[0]+10+700*math.cos(i.angle), pos[1]+10+700*math.sin(i.angle)))
    
    
    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, (block_list), True)  
    
    #laser collision
    for i in lasers:
        #if distance is less then 5 units, laser has hit
        d = float(math.fabs(i.rect.width*(i.rect.y-pos[1])-(i.rect.x-pos[0])*(i.rect.height)))/(float(i.rect.width**2+i.rect.height**2))**0.5
        if d < 5 and pygame.sprite.collide_rect(player, i):
            #if player inside rectangle of laser
            #print "collided dude " + str(d)
            pass

    # Check the list of collisions.
    if len(blocks_hit_list) > 0:
        score +=len(blocks_hit_list)
        #print( score )
         
    # Draw all the spites
    all_sprites_list.draw(screen)
     
    # Limit to 20 frames per second
    clock.tick(20)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
pygame.quit()
