class Moon:

    def __init__(self, position, velocity=(0, 0, 0)):
        self.position = position
        self.velocity = velocity

    def get_next_velocity(self, moons):
        new_velocity = list(self.velocity)
        for moon in moons:
            for axis in range(3):
                if self.position[axis] < moon.position[axis]:
                    new_velocity[axis] += 1
                elif self.position[axis] > moon.position[axis]:
                    new_velocity[axis] -= 1
        self.velocity = tuple(new_velocity)

    def get_next_position(self):
        self.position = tuple([velocity + position for velocity, position in zip(self.position, self.velocity)])

    def get_total_energy(self):
        potential_energy = sum([abs(element) for element in self.position])
        kinetic_energy = sum([abs(element) for element in self.velocity])
        return potential_energy * kinetic_energy

    def get_position_hash(self):
        return hash(self.position)