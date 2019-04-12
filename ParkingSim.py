import pygame, math

#COLORS
GREEN = (76, 175, 80)
GREY = (158, 158, 158)
acc = 0.2
turn = 0.06
class Car(pygame.sprite.Sprite):
    # -- Methods
    # Constructor function
    def __init__(self, pos,r,img):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.image.load(img), r)
        self.tirech = 0
        self.tire = 0
        self.rochange = 0
        self.rotation = r
        self.a = 0
        self.v = 0
        self.x = pos[0]
        self.y = pos[1]
# Function to rotate an image around its center
def rot_center( image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

pygame.init()

# Set up Window
grass = pygame.display.set_mode([500,500])
pygame.display.set_caption("Parking Simulator")

x = 150
y = 150
car = Car([x, y],0, "CarT.png")
red_car = pygame.image.load("Car.png")
yellow_car = pygame.image.load("Car4.png")
clock = pygame.time.Clock()
done = False
while not done:
    # Checks each event in the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car.tirech = turn
            if event.key == pygame.K_RIGHT:
                car.tirech = -1 * turn
            if event.key == pygame.K_UP:
                car.a = acc
            if event.key == pygame.K_DOWN:
                car.a = -2 * acc / 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                car.a = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                car.tirech = 0
    # Doesn't let car tires turn past 2
    if abs(car.tire + car.tirech) > 19 * turn:
        pass
    else:
        car.tire += car.tirech
    # Friction and slowdown
    if car.v != 0:
        if car.v > 0:
            car.v -= acc / 5
        if car.v < 0:
            car.v += acc / 5
        if abs(car.v) < acc / 5:
            car.v = 0
        #Tires move slowly back to straight forwards
        if car.tire > 0:
            car.tire -= turn / 4
        if car.tire < 0:
            car.tire += turn / 4
        if abs(car.tire) < turn / 4:
            car.tire = 0
    car.rotation += car.tire * car.v
    # Calculate speed and direction
    if abs(car.v + car.a) > 15 * acc:
        pass
    else:
        car.v = car.v + car.a
    car.x += car.v * math.cos(-1 * car.rotation * math.pi / 180)
    car.y += car.v * math.sin(-1 * car.rotation * math.pi / 180)

    # if the car goes out of bounds
    if not 0 < car.x < 500 or not 0 < car.y < 500:
        car.a = 0
        car.v = 0
        car.x = 150
        car.y = 150
        car.tire = 0

    # Draw Everything

    # Fill in Background
    grass.fill(GREEN)
    # Parking Spot
    pygame.draw.lines(grass, GREY, False, [[190, 80], [190, 8], [250, 8], [250, 80]], 5)
    # Draw the player's Car
    car.image = rot_center(pygame.image.load("CarT.png"), car.rotation)
    grass.blit(car.image, [car.x, car.y])
    # Parallel Parking
    grass.blit(red_car, [390, 120])
    grass.blit(yellow_car, [390, 250])

    # Update Display
    pygame.display.flip()
    clock.tick(50)

pygame.quit()