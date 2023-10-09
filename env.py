from pygw import Game
from pygw.graphic import CartesianPlane
from pygw.physics import (Body,
                          DynamicPolygonBody,
                          StaticPolygonBody,
                          StaticRectangleBody,
                          FreePolygonBody,
                          Ray)
from pygw.physics import EnginePolygon as Engine
import pygame as pg
import numpy as np
import json
import math


WALL_ID = 0
AGENT_ID = 1
SENSOR_ID = 1

FORWARD = 0
RIGHT = 1
BREAK = 2
LEFT = 3

FPS = 60
MAX_SPEED = 300
SPEED_RATE = 10
ROT_SPEED = 2
SENSOR_RADIUS = 200
SENSOR_COUNT = 20
DRAG_COEF = 0.01
FRIC_COEF = 0.3

STATE_SPACE_SIZE = SENSOR_COUNT + 1
ACTION_SPACE_SIZE = 4


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
            r.shape.vertices[0].rotate(np.pi / 2 + 2 * np.pi / ray_count * i)
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
        super().__init__()
        self.title = 'Test environment'
        self.size = (self.WIDTH, self.HEIGHT)
        self.fps = FPS
        self.window_flags = pg.FULLSCREEN | pg.HWSURFACE
        self.set_window()

        self.plane = CartesianPlane(self.window, self.size, frame_rate=self.fps, unit_length=1)
        self.bodies: list[Body] = []
        self.create_wall()
        self.load_env(path)

        self.agent: DynamicPolygonBody = self.bodies[-1]
        self.sensor = Sensor(SENSOR_ID, self.plane.createPlane(), SENSOR_COUNT, SENSOR_RADIUS)
        for r in self.sensor.rays:
            self.agent.attach(r, True)
        # Agent dir indicator
        a = FreePolygonBody(AGENT_ID, self.plane.createPlane(), (17, 5, 5))
        a.shape.color = (0, 0, 255)
        self.agent.attach(a, True)

        self.bodies.extend(self.sensor.rays)
        self.bodies.append(a)

        self.engine = Engine(self.plane, np.array(self.bodies, dtype=Body))

        self.over = False
        self.last_sensor_state = []

    def step(self, action):
        if action == FORWARD:
            self.agent.accelerate(SPEED_RATE)
        elif action == BREAK:
            self.agent.accelerate(-SPEED_RATE)
        elif action == LEFT:
            self.agent.rotate(ROT_SPEED)
        elif action == RIGHT:
            self.agent.rotate(-ROT_SPEED)
        else:
            raise ValueError('Unknown action')
        self.loop_once()
        return self.get_reward(), self.get_state()

    def loop(self):
        # First apply control ...
        if __name__ == '__main__':
            self.manual_control()
        # ... then let the game engine do it's job
        self.engine.step()
        # Save sensor values before render phase, because they will be lost forever
        self.last_sensor_state = self.sensor.state()

    def reset(self):
        self.over = False
        unit_vec = self.agent.velocity.unit(vector=False)
        self.agent_vec.head = self.agent_initial_pos
        # TODO fix
        self.agent.velocity.head = self.agent.shape.plane.createVector(unit_vec[0],
                                                                  unit_vec[1],
                                                                  MAX_SPEED, 1).head
        # Run one iter after reset to apply the change
        self.loop_once()
        return self.get_state()

    def onEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                self.over = True
                self.running = False
            elif event.key == pg.K_r:
                self.over = True

    def onRender(self):
        self.window.fill((255, 255, 255))
        for b in self.bodies:
            b.show()

    def get_reward(self):
        s = self.agent.speed()
        r = s / MAX_SPEED if s > 0 else -1
        # r += ((st[0] - SENSOR_RADIUS) / (SENSOR_RADIUS * 2)
        #       if st[0] < SENSOR_RADIUS
        #       else 0.5)
        return r

    def get_state(self):
        state = self.last_sensor_state.copy()
        state.append(self.agent.speed())
        return state

    def manual_control(self):
        """Manual control"""
        if self.keys[pg.K_UP]:
            self.agent.accelerate(SPEED_RATE)
        elif self.keys[pg.K_DOWN]:
            self.agent.accelerate(-SPEED_RATE)
        if self.keys[pg.K_LEFT]:
            self.agent.rotate(ROT_SPEED)
        elif self.keys[pg.K_RIGHT]:
            self.agent.rotate(-ROT_SPEED)

    def load_env(self, path):
        with open(path) as f:
            self.objects = json.load(f)

        for body in self.objects['bodies']:
            vec = self.plane.createVector(body['x'], body['y'])
            size = tuple([body['size'] for _ in range(body['shape'])])
            if body['type'] == 1:
                self.agent_vec = vec
                self.agent_initial_pos = (body['x'], body['y'])
                p = DynamicPolygonBody(
                    AGENT_ID, CartesianPlane(self.window, (40, 40), vec, frame_rate=self.fps),
                    size, MAX_SPEED, drag_coef=DRAG_COEF, friction_coef=FRIC_COEF)
                p.shape.color = (255, 0, 255)
            else:
                p = StaticPolygonBody(
                    WALL_ID, CartesianPlane(self.window, (40, 40), vec, frame_rate=self.fps), size)
            p.rotate(body['dir'])
            self.bodies.append(p)

    def create_wall(self):
        y = self.size[1] / 2
        for _ in range(28):
            vec = self.plane.createVector(-self.size[0] / 2, y)
            self.bodies.append(
                StaticRectangleBody(WALL_ID,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            vec = self.plane.createVector(self.size[0] / 2, y)
            self.bodies.append(
                StaticRectangleBody(WALL_ID,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            y -= 40

        x = -self.size[0] / 2 + 40
        for _ in range(47):
            vec = self.plane.createVector(x, self.size[1] / 2)
            self.bodies.append(
                StaticRectangleBody(WALL_ID,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            vec = self.plane.createVector(x, -self.size[1] / 2)
            self.bodies.append(
                StaticRectangleBody(WALL_ID,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            x += 40


if __name__ == '__main__':
    env = Environment('test_env.json')

    while env.running:
        env.loop_once()
