from Game.base import Game
from Game.graphic import CartesianPlane
from Game.physics import (object_body,
                          DynamicPolygonBody,
                          StaticPolygonBody,
                          StaticRectangleBody,
                          FreePolygonBody,
                          Ray)
from Game.physics import Engine
import pygame as pg
import numpy as np
import json
import math


def dist(point_a, point_b):
    x1, y1 = point_a
    x2, y2 = point_b
    return math.hypot(x1-x2, y1-y2)


FORWARD = 0
RIGHT = 1
BREAK = 2
LEFT = 3

MAX_SPEED = 7
SENSOR_RADIUS = 200
SENSOR_COUNT = 20


class Sensor:

    def __init__(self,
                 id: int,
                 plane: CartesianPlane,
                 ray_count: int,
                 radius: float) -> None:
        self.rays: list[Ray] = []
        for i in range(ray_count):
            r = Ray(id, plane, radius)
            r.shape.color = (230, 230, 230)
            r.shape.vertices[0].rotate(np.pi/2 + 2*np.pi/ray_count * i)
            self.rays.append(r)

    def state(self):
        s = []
        for ray in self.rays:
            d = math.hypot(ray.x, ray.y)
            if d == 0:
                s.append(ray.radius)
            else:
                s.append(d)
        return s

    def reset(self):
        for ray in self.rays:
            ray.reset()


class Environment(Game):

    WIDTH = 1920
    HEIGHT = 1080

    def __init__(self, path: str) -> None:
        super().__init__('Test environment',
                         self.WIDTH, self.HEIGHT, 60,
                         pg.FULLSCREEN | pg.HWSURFACE, True)
        self.plane = CartesianPlane(self.window, (self.width, self.height),
                                    unit_length=1)
        self.bodies: list[object_body] = []

        self.over = False

        y = self.height / 2
        for _ in range(28):
            vec = self.plane.createVector(-self.width/2, y)
            self.bodies.append(
                StaticRectangleBody(0,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            vec = self.plane.createVector(self.width/2, y)
            self.bodies.append(
                StaticRectangleBody(0,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            y -= 40

        x = -self.width/2 + 40
        for _ in range(47):
            vec = self.plane.createVector(x, self.height / 2)
            self.bodies.append(
                StaticRectangleBody(0,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            vec = self.plane.createVector(x, -self.height / 2)
            self.bodies.append(
                StaticRectangleBody(0,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            x += 40

        self.objects = dict()
        self.agent_vec = None
        self.agent_initial_pos = None

        with open(path) as f:
            self.objects = json.load(f)

        for body in self.objects['bodies']:
            vec = self.plane.createVector(body['x'], body['y'])
            size = tuple([body['size'] for _ in range(body['shape'])])
            if body['type'] == 1:
                self.agent_vec = vec
                self.agent_initial_pos = (body['x'], body['y'])
                p = DynamicPolygonBody(
                    1, CartesianPlane(self.window, (40, 40), vec),
                    size, MAX_SPEED)
                p.shape.color = (255, 0, 255)
            else:
                p = StaticPolygonBody(
                    0, CartesianPlane(self.window, (40, 40), vec), size)
            p.rotate(body['dir'])
            self.bodies.append(p)

        self.agent: DynamicPolygonBody = self.bodies[-1]
        self.sensor = Sensor(1, self.plane.createPlane(),
                             SENSOR_COUNT, SENSOR_RADIUS)
        a = FreePolygonBody(1, self.plane.createPlane(), (17, 5, 5))
        a.shape.color = (0, 0, 255)
        self.agent.attach(a, True)
        for r in self.sensor.rays:
            self.agent.attach(r, True)

        self.bodies.extend(self.sensor.rays)
        self.bodies.append(a)

        self.engine = Engine(self.plane,
                             np.array(self.bodies, dtype=object_body))

    def step(self, action):
        if action == FORWARD:
            self.agent.Accelerate(0.15)
        elif action == BREAK:
            self.agent.Accelerate(-0.15)
        elif action == LEFT:
            self.agent.rotate(0.06)
        elif action == RIGHT:
            self.agent.rotate(-0.06)
        else:
            raise ValueError('Unknown action')
        self.loop_once()
        return self.get_reward(), self.get_state()

    def reset(self):
        self.over = False
        unit_vec = self.agent.velocity.unit(vector=False)
        self.agent_vec.head = self.agent_initial_pos
        self.agent.velocity = self.agent.shape.plane.createVector(unit_vec[0],
                                                                  unit_vec[1],
                                                                  MAX_SPEED, 1)
        self.loop_once()
        return self.get_state()

    def get_reward(self):
        st = self.sensor.state()
        s = self.agent.speed()
        r = s / (MAX_SPEED/2) if s >= 0.1 else -1
        r += ((st[0] - SENSOR_RADIUS) / SENSOR_RADIUS
              if st[0] < SENSOR_RADIUS
              else 0.5)
        # r += ((st[1] - SENSOR_RADIUS/2) / SENSOR_RADIUS
        #       if st[1] < SENSOR_RADIUS/2
        #       else 0.2)
        # r += ((st[-1] - SENSOR_RADIUS/2) / SENSOR_RADIUS
        #       if st[-1] < SENSOR_RADIUS/2
        #       else 0.2)
        # r += ((st[2] - SENSOR_RADIUS/3) / SENSOR_RADIUS
        #       if st[2] < SENSOR_RADIUS/3
        #       else 0.1)
        # r += ((st[-2] - SENSOR_RADIUS/3) / SENSOR_RADIUS
        #       if st[-2] < SENSOR_RADIUS/3
        #       else 0.1)
        return r

    def get_state(self):
        state = self.sensor.state()
        state.append(self.agent.speed())
        return state

    def USR_eventHandler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                self.over = True
                self.running = False
            elif event.key == pg.K_r:
                self.over = True

    # def USR_loop(self):
    #     if self.keys[pg.K_UP]:
    #         self.agent.Accelerate(0.15)
    #     elif self.keys[pg.K_DOWN]:
    #         self.agent.Accelerate(-0.15)
    #     if self.keys[pg.K_LEFT]:
    #         self.agent.rotate(0.05)
    #     elif self.keys[pg.K_RIGHT]:
    #         self.agent.rotate(-0.05)

    def USR_render(self):
        self.sensor.reset()
        self.engine.update()


if __name__ == '__main__':
    env = Environment()

    while env.running:
        env.loop_once()
        print(env.sensor.state())
