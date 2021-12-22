import numpy as np
class Ant:
    def __init__(self,hill_point,world):
        self.hill_point = hill_point
        self.world = world
        self.reset_memory()

    def reset_memory(self):
        self.stack = list()
        self.move(self.hill_point)
        self.forward = True

    def move(self,point):
        self.stack.append(tuple(point))

    def get_curr_point(self):
        return self.stack[-1]

    def release_pheromone(self):
        point = self.get_curr_point()
        self.world.release_pheromone(point,2)

    def decision_next_point_for_move(self,points):
        if len(points) > 0:
            pheromones = self.world.get_pheromones_from_list(points)
            prop_points = np.exp(pheromones) / np.exp(pheromones).sum()
            choice_index = np.random.choice(range(len(points)),p=prop_points)
            return points[choice_index]
        return None

    def remove_visited_points(self,points):
        return [point for point in points if point not in self.stack]

    def run(self):
        if self.forward:
            point = self.get_curr_point()
            candidate_points = self.world.get_candidate_points_for_move(point)
            candidate_points = self.remove_visited_points(candidate_points)
            next_point = self.decision_next_point_for_move(candidate_points)
            if next_point is not None:
                self.move(next_point)
                if self.world.has_food(next_point):
                    self.world.remove_food(next_point,1)
                    self.forward = False
        else:
            if len(self.stack) > 1:
                self.release_pheromone()
                self.stack.pop()
            else:
                self.reset_memory()

class Colony:
    def __init__(self,hill_point, n_ants,world):
        self.hill_point = hill_point
        self.n_ants = n_ants
        self.ants = [Ant(self.hill_point,world) for i in range(n_ants)]
        self.reset_ants()

    def reset_ants(self):
        for ant in self.ants:
            ant.reset_memory()

    def run(self):
        for ant in self.ants:
            ant.run()