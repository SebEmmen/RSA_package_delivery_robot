import os
import pygame
import numpy as np
from math import sin, cos, radians, degrees, copysign
from pygame.math import Vector2



class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=70, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 5
        self.acceleration_scaling = 10

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        #if self.steering:
            #turning_radius = self.length / sin(radians(self.steering))
            #angular_velocity = self.velocity.x / turning_radius
        #else:
        #    angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += self.steering
        #self.angle += degrees(angular_velocity) * dt

class Map:
    def __init__(self):
        #list of coordinates, dimensions and the color of the obstacles
        self.xposition = [1000, 650, 500, 650]
        self.yposition = [100, 600, 200, 300]
        self.dimensions = [[30, 500], [500, 30], [500, 30], [30, 300]]
        self.color = [255, 0, 0]
    def give_obstacles(self, surface):

        # Returns a list of obstacle rects
        rectlist = []
        for i in range(len(self.xposition)):
            rect = pygame.Rect(self.xposition[i],self.yposition[i], self.dimensions[i][0], self.dimensions[i][1])
            rectlist.append(rect)
            pygame.draw.rect(surface, self.color, rect)
        return rectlist

    def obstacle_collision(self, width, height, ppu, obstacle_list, position, angle):

        # Function first calculates the coordinates of the corners of the car and if they are inside obstacles returns true
        l = width * 1
        w = height * 1
        x = position[0] * ppu
        y = position[1] * ppu
        alpha = radians(angle)

        # Base vectors for calculating corners
        v1 = np.array([w/2 * sin(alpha), w/2 * cos(alpha)])
        v2 = np.array([l/2 * cos(alpha), - l/2 * sin(alpha)])
        posvector = np.array([x, y])

        # Car corners
        c1 = v1 + v2 + posvector
        c2 = - v1 + v2 + posvector
        c3 = - v1 - v2 + posvector
        c4 = v1 - v2 + posvector

        collision = False
        front = False
        for i in obstacle_list:

            if pygame.Rect.collidepoint(i, c1):
                collision = True
                front = True
            elif pygame.Rect.collidepoint(i, c2):
                collision = True
                front = True
            elif pygame.Rect.collidepoint(i, c3):
                collision = True
                front = False
            elif pygame.Rect.collidepoint(i, c4):
                collision = True
                front = False
        return collision, front

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
        car = Car(0, 0)

        map = Map()
        ppu = 32


        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += car.acceleration_scaling * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= car.acceleration_scaling * dt
            elif pressed[pygame.K_SPACE]:
                if abs(car.velocity.x) > dt * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / dt
            else:
                if abs(car.velocity.x) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                car.steering -= 10 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 10 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            # Logic
            car.update(dt)

            # Drawing
            self.screen.fill((0, 0, 0))
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()

            # Calls obstacle list
            obstacle_list = map.give_obstacles(self.screen)

            # Checks if there is a collision and if so, front or back
            collision, front = map.obstacle_collision(rect.width, rect.height, ppu, obstacle_list, car.position, car.angle)
            if collision and front:
                print(" front collision")
            elif collision:
                print("back collision")
                #car.velocity[0] = 0

            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()