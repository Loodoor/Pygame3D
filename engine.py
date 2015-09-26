import pygame
from pygame.locals import *
import math
from random import randrange, randint
from operator import itemgetter


class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)


class Vector2:
    def __init__(self, *args):
        self.vector2 = tuple(args)
        self.size = self.vector2[0] if self.vector2[0] > self.vector2[1] else self.vector2[1]
    
    def rotate(self, **kwargs):
        if 'right' in kwargs.keys():
            if kwargs['right']:
                if self.vector2 == (0, self.size):
                    self.vector2 = (self.size, 0)
                elif self.vector2 == (self.size, 0):
                    self.vector2 = (0, -self.size)
                elif self.vector2 == (0, -self.size):
                    self.vector2 = (-self.size, 0)
                elif self.vector2 == (-self.size, 0):
                    self.vector2 = (0, self.size)
        if 'left' in kwargs.keys():
            if kwargs['left']:
                if self.vector2 == (0, self.size):
                    self.vector2 = (-self.size, 0)
                elif self.vector2 == (-self.size, 0):
                    self.vector2 = (0, -self.size)
                elif self.vector2 == (0, -self.size):
                    self.vector2 = (self.size, 0)
                elif self.vector2 == (self.size, 0):
                    self.vector2 = (0, self.size)
    
    def get(self):
        return self.vector2
    
    def addget(self, to_add):
        return self.vector2[0] + to_add[0], self.vector2[1] + to_add[1]
    
    def gresize(self, scale):
        return self.vector2[0] * scale, self.vector2[1] * scale
    
    def from_pos(self, pos):
        return self.vector2[0] + pos[0], self.vector2[1] + pos[1]


class Square:
    def __init__(self, color=(255, 255, 255), size1=256, size2=256, xpos=0, ypos=0, zpos=0):
        self.color = color
        self.size1 = size1
        self.size2 = size2
        self.points = [
            Point3D(0, 0, 0),
            Point3D(1, 0, 0),
            Point3D(1, 1, 0),
            Point3D(0, 1, 0)
        ]
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0
    
    def draw(self, screen, var=0):
        t = []
        for v in self.points:
            r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            p = r.project(screen.get_width(), screen.get_height(), (self.size1 + self.size2) // 2, 4 + self.zpos)
            if not var:
                screen.fill(self.color, (p.x + self.xpos, p.y + self.ypos, self.size, self.size))
            t.append(p)
        if var == 1:
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos), (t[1].x + self.xpos, t[1].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[1].x + self.xpos, t[1].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[2].x + self.xpos, t[2].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[3].x + self.xpos, t[3].y + self.ypos), (t[0].x + self.xpos, t[0].y + self.ypos))
        if var == 2:
            points = [
                (t[0].x + self.xpos, t[0].y + self.ypos),
                (t[1].x + self.xpos, t[1].y + self.ypos),
                (t[2].x + self.xpos, t[2].y + self.ypos),
                (t[3].x + self.xpos, t[3].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
    
    def rotateX(self, dir=1):
        self.angleX += dir
    
    def rotateY(self, dir=1):
        self.angleY += dir
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
    
    def moveX(self, dir=1):
        self.xpos += dir
    
    def moveY(self, dir=1):
        self.ypos += dir
    
    def moveZ(self, dir=1):
        self.zpos += dir


class Pyramide:
    def __init__(self, color=(255, 255, 255), pyra_size=256, xpos=0, ypos=0, zpos=0):
        self.vertices = [
            Point3D(0, 1, 0),
            Point3D(-1, -1, 1),
            Point3D(-1, -1, -1),
            Point3D(1, -1, 1),
            Point3D(1, -1, -1)
        ]
        
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.size = 2
        self.color = color
        self.pyra_size = pyra_size
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        
    def draw(self, screen, var=0):
        t = []
        for v in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            # Transform the point from 3D to 2D
            p = r.project(screen.get_width(), screen.get_height(), self.pyra_size, 4 + self.zpos)
            if not var:
                screen.fill(self.color, (p.x + self.xpos, p.y + self.ypos, self.size, self.size))
            t.append(p)
        if var == 1:
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos), (t[1].x + self.xpos, t[1].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos), (t[4].x + self.xpos, t[4].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[1].x + self.xpos, t[1].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[2].x + self.xpos, t[2].y + self.ypos), (t[4].x + self.xpos, t[4].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[3].x + self.xpos, t[3].y + self.ypos), (t[4].x + self.xpos, t[4].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[1].x + self.xpos, t[1].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos))
        if var == 2:
            points = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[1].x + self.xpos, t[1].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
            points = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos), (t[4].x + self.xpos, t[4].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
            points = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos), (t[4].x + self.xpos, t[4].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
            points = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[1].x + self.xpos, t[1].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
            points = [
                (t[1].x + self.xpos, t[1].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos),
                (t[4].x + self.xpos, t[4].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
        
    def rotateX(self, dir=1):
        self.angleX += dir
    
    def rotateY(self, dir=1):
        self.angleY += dir
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
    
    def moveX(self, dir=1):
        self.xpos += dir
    
    def moveY(self, dir=1):
        self.ypos += dir
    
    def moveZ(self, dir=1):
        self.zpos += dir


class Crate:
    def __init__(self, color=(255, 255, 255), crate_size=256, xpos=0, ypos=0, zpos=0):
        self.vertices = [
            Point3D(-1, 1, -1),
            Point3D(1, 1, -1),
            Point3D(1, -1, -1),
            Point3D(-1, -1, -1),
            Point3D(-1, 1, 1),
            Point3D(1, 1, 1),
            Point3D(1, -1, 1),
            Point3D(-1, -1, 1)
        ]
        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces = [
            (0, 1, 2, 3),
            (1, 5, 6, 2),
            (5, 4, 7, 6),
            (4, 0, 3, 7),
            (0, 4, 5, 1),
            (3, 2, 6, 7)
        ]
        
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.size = 2
        self.color = color
        self.crate_size = crate_size
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
    
    def draw(self, screen, var=0):
        t = []
        for v in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            # Transform the point from 3D to 2D
            p = r.project(screen.get_width(), screen.get_height(), self.crate_size, 4 + self.zpos)
            if not var:
                screen.fill(self.color, (p.x + self.xpos, p.y + self.ypos, self.size, self.size))
            t.append(p)
        if var == 1:
            for f in self.faces:
                pygame.draw.line(screen, self.color, (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos), (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos))
                pygame.draw.line(screen, self.color, (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos), (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos))
                pygame.draw.line(screen, self.color, (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos), (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos))
                pygame.draw.line(screen, self.color, (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos), (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos))
        if var == 2:
            avg_z = []
            i = 0
            for f in self.faces:
                z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
                avg_z.append([i, z])
                i += 1
            for tmp in sorted(avg_z, key=itemgetter(1), reverse=True):
                face_index = tmp[0]
                f = self.faces[face_index]
                points = [
                    (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos), (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos),
                    (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos), (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos),
                    (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos), (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos),
                    (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos), (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos)
                ]
                pygame.draw.polygon(screen, self.color, points)
    
    def rotateX(self, dir=1):
        self.angleX += dir
    
    def rotateY(self, dir=1):
        self.angleY += dir
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
    
    def moveX(self, dir=1):
        self.xpos += dir
    
    def moveY(self, dir=1):
        self.ypos += dir
    
    def moveZ(self, dir=1):
        self.zpos += dir


class Sphere:
    def __init__(self, color=(255, 255, 255), sphere_size=256, xpos=0, ypos=0, zpos=0, radius=2):
        self.center = Point3D(0, 0, 0)
        self.radius = radius
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.size = 2
        self.color = color
        self.sphere_size = sphere_size
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
    
    def draw(self, screen, var=0):
        p = self.center.project(screen.get_width(), screen.get_height(), self.sphere_size, 4 + self.zpos)
        radius = abs(-self.radius * (self.sphere_size / (4 - self.zpos)))
        if not var:
            screen.fill(self.color, (p.x + self.xpos, p.y + self.ypos, self.size, self.size))
        if var == 1:
            pygame.draw.circle(screen, self.color, (int(p.x) + self.xpos, int(p.y) + self.ypos), int(radius), 1)
        if var == 2:
            pygame.draw.circle(screen, self.color, (int(p.x) + self.xpos, int(p.y) + self.ypos), int(radius), 0)

    def rotateX(self, dir=1):
        self.angleX += dir
    
    def rotateY(self, dir=1):
        self.angleY += dir
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
    
    def moveX(self, dir=1):
        self.xpos += dir
    
    def moveY(self, dir=1):
        self.ypos += dir
    
    def moveZ(self, dir=1):
        self.zpos += dir


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 12)
        self.objects = []
        self.fps = 60
        self.clock = pygame.time.Clock()
    
    def create_squares(self):
        print("Creating squares ...")
        self.objects.append(Square(color=(150, 150, 255), size1=64, size2=128, ypos=-64))
    
    def create_crates(self):
        print("Creating crates ...")
        self.objects.append(Crate(crate_size=64, xpos=0, color=(255, 150, 255)))
    
    def create_pyramides(self):
        print("Creating pyramides ...")
        self.objects.append(Pyramide(pyra_size=64, xpos=64, color=(150, 255, 255)))
    
    def create_spheres(self):
        print("Creating spheres ...")
        self.objects.append(Sphere(sphere_size=64, ypos=64, color=(255, 255, 150)))
    
    def draw_objects(self):
        for obj in self.objects:
            obj.draw(self.screen, var=2)
    
    def rotate_objects(self):
        for i in range(len(self.objects)):
            self.objects[i].rotateX(1)
    
    def run(self):
        while 1:
            self.clock.tick(self.fps)
            
            event = pygame.event.poll()
            if event.type == QUIT:
                break
            
            self.screen.fill((0, 0, 0))
            self.draw_objects()
            self.rotate_objects()
            
            self.screen.blit(self.font.render("FPS:" + str(self.clock.get_fps()), 1, (180, 255, 255)), (0, 0))
            
            pygame.display.flip()


def main():
    import time
    print("Starting ...")
    start = time.time()
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((640, 640))
    game = Game(screen)
    game.create_squares()
    """game.create_pyramides()
    game.create_crates()
    game.create_spheres()"""
    print("Generation took %3f" % (time.time() - start))
    print("Running demo ...")
    game.run()
    pygame.quit()
    print("Exited cleanly")


if __name__ == '__main__':
    main()