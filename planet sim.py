import pygame
import math
pygame.init()

WIDTH, HEIGHT = 2000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("planet simulation")

# colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

class Planet:
    
    AU = 149.6e6 * 1000 # astrunamical unit (distance between sun and earth)
    G = 6.67428e-11 # gravitational constent (force of attraction between objects)
    SCALE = 250 / AU # 1AU = 100 pixels #if we want to change the scale of the system just modifye 250 to any number we want.
    TIMESTEP = 3600 * 24 # 1 day
    
    
    def __init__(self, x, y, radius, color, mass):
        """__init__ function """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, win): 
        """this function will draw planets and their orbit line"""
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
    def attraction(self, other):
        """this function will calcuate the attraction force between objects"""
        # calculating the distence between objects
        other_x, other_y = other.x, other.y 
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        # check that if the object is sun
        if other.sun:
            self.distance_to_sun = distance
        
        # calculating the force of the attraction    
        force = self.G * self.mass * other.mass / distance ** 2 # straght line force
        theta = math.atan2(distance_y, distance_x) # angel
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
        
    def update_position(self, planets):
        """this function will update position of planets in planets list"""
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel *self.TIMESTEP
        self.y += self.y_vel *self.TIMESTEP
        self.orbit.append((self.x, self.y))
    
def main():
    """this the main function for runing programm"""
    run = True
    Clock = pygame.time.Clock()
    
    # interstaller objects
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True
    
    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000
    
    marse = Planet(1.524 * Planet.AU, 0, 14, RED, 6.39 * 10**23)
    marse.y_vel = 24.077 * 1000
    
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 0.330 * 10**24)
    mercury.y_vel = 47.4 * 1000
    
    vinus = Planet(0.723 * Planet.AU, 0, 12, WHITE, 4.8685 * 10**24)
    vinus.y_vel = -35.02 * 1000
    
    planets = [sun, earth, marse, mercury, vinus]
    
    while run:
        Clock.tick(60)
        WIN.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()        
        
    pygame.quit()
    
main()