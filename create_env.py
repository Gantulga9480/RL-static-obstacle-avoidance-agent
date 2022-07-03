from Game.base import Game
from Game.graphic import CartesianPlane
from Game.physics import (object_body,
                          StaticRectangleBody,
                          StaticPolygonBody,
                          DynamicPolygonBody)
import pygame as pg
import math
import json


class Test(Game):

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = 1920,
                 height: int = 1080,
                 fps: int = 60,
                 flags: int = pg.FULLSCREEN | pg.HWSURFACE,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, flags, render)

        self.plane = CartesianPlane(self.window, (width, height),
                                    unit_length=1)
        self.frames: list[object_body] = []
        self.bodies = []

        y = height / 2
        for i in range(28):
            vec = self.plane.createVector(-width/2, y)
            self.frames.append(
                StaticRectangleBody(1,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            vec = self.plane.createVector(width/2, y)
            self.frames.append(
                StaticRectangleBody(1,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            y -= 40

        x = -width/2 + 40
        for i in range(47):
            vec = self.plane.createVector(x, height / 2)
            self.frames.append(
                StaticRectangleBody(1,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            vec = self.plane.createVector(x, -height / 2)
            self.frames.append(
                StaticRectangleBody(1,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            x += 40

        self.shape_size = 40
        self.shape_vertex = 4
        self.type = 0
        self.shape_dir = math.pi/4
        self.create_shape()

    def USR_eventHandler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_c:
                self.create_shape()
            elif event.key == pg.K_d:
                if self.bodies.__len__() > 0:
                    self.bodies.pop()
            elif event.key == pg.K_s:
                self.bodies.append([self.current_shape,
                                    self.shape_size,
                                    self.shape_vertex,
                                    self.shape_dir,
                                    self.current_vec.x,
                                    self.current_vec.y])
                self.create_shape()
            elif event.key == pg.K_UP:
                self.shape_size *= 1.1
                self.current_shape.scale(1.1)
            elif event.key == pg.K_DOWN:
                self.shape_size *= 1/1.1
                self.current_shape.scale(1/1.1)
            elif event.key == pg.K_RIGHT:
                self.shape_dir += -0.1
                self.current_shape.rotate(-0.1)
            elif event.key == pg.K_LEFT:
                self.shape_dir += 0.1
                self.current_shape.rotate(0.1)
            elif event.key == pg.K_q:
                if self.shape_vertex > 3:
                    self.shape_vertex -= 1
                    self.create_shape()
            elif event.key == pg.K_e:
                self.shape_vertex += 1
                self.create_shape()
            elif event.key == pg.K_1:
                self.type = 1
                self.create_shape()
            elif event.key == pg.K_0:
                self.type = 0
                self.create_shape()
            elif event.key == pg.K_f:
                d = dict()
                a = []
                for body in self.bodies:
                    c = dict()
                    c['type'] = body[0].type
                    c['size'] = body[1]
                    c['shape'] = body[2]
                    c['dir'] = body[3]
                    c['x'] = body[4]
                    c['y'] = body[5]
                    a.append(c)
                d['bodies'] = a
                with open('test_env.json', 'w') as f:
                    json.dump(d, f)
                self.running = False

    def USR_loop(self):
        self.current_vec.x = self.plane.to_x(self.mouse_x)
        self.current_vec.y = self.plane.to_y(self.mouse_y)

    def USR_render(self):
        if self.current_shape.type == 1:
            self.current_shape.shape.color = (0, 0, 255)
            self.current_shape.show()
        else:
            self.current_shape.shape.color = (255, 0, 0)
            self.current_shape.show()
        for frame in self.frames:
            frame.show(True)
        for body in self.bodies:
            body[0].shape.color = (255, 0, 0)
            body[0].show((255, 0, 0))
        self.set_title(f'fps {round(self.clock.get_fps())}')

    def create_shape(self):
        self.current_vec = self.plane.createVector(0, 0)
        size = tuple([self.shape_size for _ in range(self.shape_vertex)])
        if self.type == 1:
            self.current_shape = DynamicPolygonBody(
                0, CartesianPlane(
                    self.window, (40, 40), self.current_vec),
                size)
        else:
            self.current_shape = StaticPolygonBody(
                0, CartesianPlane(
                    self.window, (40, 40), self.current_vec),
                size)
        self.current_shape.rotate(self.shape_dir)


Test().mainloop()
