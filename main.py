import numpy as np
import pygame
import sys
from world import World
from ant import Colony

class Simulator:
    def __init__(self,window_size, rect_size,evaporation_rate=0.05,hill_point=None,n_ants=10,n_iterations=100):
        self.window_size = window_size
        self.rect_size = rect_size
        self.food_size = np.array(rect_size) // 2
        self.hill_size = np.linalg.norm(self.rect_size) / 2
        world_size = np.array(window_size) // np.array(rect_size)
        self.world = World(world_size, evaporation_rate)

        if hill_point is None:
            hill_point = np.array(world_size) // 2

        self.colony = Colony(hill_point=hill_point,n_ants=n_ants,world=self.world)
        self.n_iterations = n_iterations
        pygame.init()
        pygame.display.set_caption('Ant Colony Optimization Algorithm - Arif ALTIOK')
        self.window = pygame.display.set_mode(self.window_size)
        self.font_size = int(np.linalg.norm(self.rect_size))
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.clock = pygame.time.Clock()
        self.pause = False
        self.epoch = 0
        self.infos = dict()

    def listen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
            elif event.type == pygame.MOUSEBUTTONDOWN:
                point = tuple(np.array(pygame.mouse.get_pos()) // self.rect_size)
                if event.button == 1:
                    self.world.add_food(point, 100)
                elif event.button == 3:
                    self.world.remove_food(point, 100)


    def render_text(self,text,number,color=(0,0,0)):
        return self.font.render(f"{text}: %d" % number,True,color)

    def draw_infos(self):
        for idx,info in enumerate(self.infos.values()):
            self.window.blit(info,(0,idx * self.font_size))

    def update(self):
        iteration = 0
        while iteration < self.n_iterations:
            self.listen()
            if not self.pause:
                self.draw_pheromones()
                self.draw_hill()
                self.draw_foods()
                self.draw_ants()
                self.infos["iteration_num"] = self.render_text("Iteration",iteration + 1)
                self.infos["ants_num"] = self.render_text("Ants",len(self.colony.ants))
                self.draw_infos()
                self.clock.tick(10)
                self.colony.run()
                self.world.step()
                self.world.evaporation()
                pygame.display.update()
                iteration += 1

    def run(self):
        while True:
            self.listen()
            if not self.pause:
                self.infos["epoch_num"] = self.render_text("Epoch",self.epoch + 1)
                self.update()
                self.colony.reset_ants()
                self.epoch += 1

    def calculate_on_windows_point(self, point):
        return point[0] * self.rect_size[0], point[1] * self.rect_size[1]

    def get_xywh(self,point):
        return [*self.calculate_on_windows_point(point),*self.rect_size]

    def draw_rect(self,color,point):
        pygame.draw.rect(self.window,color,self.get_xywh(point))

    def draw_pheromones(self):
        for j in range(self.world.world_size[1]):
            idx = [(i,j) for i in range(self.world.world_size[0])]
            pheromones = 10 * np.array(self.world.get_pheromones_from_list(idx))
            pheromones[pheromones > 255] = 255
            for i,p in enumerate(pheromones):
                self.draw_rect((255,255-p,255-p),(i,j))

    def draw_hill(self):
        pygame.draw.circle(self.window,(0,127,127),[*self.calculate_on_windows_point(self.colony.hill_point)],self.hill_size)

    def draw_ants(self):
        for ant in self.colony.ants:
            color = (0,0,0) if ant.forward else (0,255,0)
            self.draw_rect(color,ant.get_curr_point())

    def draw_foods(self):
        for point,food in self.world.foods.items():
            if food > 0:
                pygame.draw.ellipse(self.window,(255,127,0),self.get_xywh(point),int(1 + food // (np.mean(self.rect_size))))

if __name__ == '__main__':
    window_sizes = (1920,1000)
    rect_size = (25,25)
    evaporation_rate =.015
    hill_point = None
    n_ants = 100
    n_iterations = 100

    similator = Simulator(window_sizes,rect_size,evaporation_rate,hill_point,n_ants,n_iterations)
    similator.run()
