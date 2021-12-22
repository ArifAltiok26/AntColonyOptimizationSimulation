import numpy as np

class World:
    def __init__(self,world_size,evaporation_rate=.01):
        self.world_size = world_size
        self.evaporation_rate = evaporation_rate
        self.pheromones = np.zeros(self.world_size)
        self.reset_delta_pheromones()
        self.connection = np.array([
            [-1, 0],[0,1],[1, 0],[0,-1],
            [-1,-1],[1,1],[-1,1],[1,-1]
        ])
        self.foods = dict()

    def reset_delta_pheromones(self):
        self.delta_pheromones = np.zeros(self.world_size)

    def release_pheromone(self,point,amount):
        self.pheromones[point] += amount

    def step(self):
        self.pheromones += self.delta_pheromones
        self.reset_delta_pheromones()

    def evaporation(self):
        self.pheromones *= (1-self.evaporation_rate)

    def get_pheromones_from_list(self,points):
        return [self.pheromones[point] for point in points]

    def get_candidate_points_for_move(self,point):
        return [(p[0],p[1]) for p in point + self.connection if p[0] >= 0 and p[0] < self.world_size[0] and p[1]>=0 and p[1] < self.world_size[1]]

    def has_food(self,point):
        try:
            retval = self.foods[point] > 0
            if retval == False:
                self.foods.pop(point)
            return retval
        except:
            return False

    def add_food(self,point,amount):
        if self.has_food(point):
            self.foods[point] += amount
        else:
            self.foods[point] = amount

    def remove_food(self,point,amount):
        if self.has_food(point):
            self.foods[point] -= amount
            self.has_food(point)

if __name__ == '__main__':
    world = World((50,50),.05)
    print(world.foods)

    world.add_food((1, 1), 5)
    print(world.foods)