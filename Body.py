class Body:
    def __init__(self, mass, heat_capacity, temperature):
        if mass <= 0:
            raise ValueError("Mass must be greater than 0")
        if heat_capacity <= 0:
            raise ValueError("Heat capacity must be greater than 0")
        if temperature < 0:
            raise ValueError("Temperature must be 0 or higher")

        self.mass = mass
        self.heat_capacity = heat_capacity
        self.temperature = temperature

    def add_heat(self, heat):
        delta_t = heat / (self.mass * self.heat_capacity)
        self.temperature += delta_t
        return self.temperature


if __name__ == "__main__":
    b = Body(100, 0.15, 200)

    t1 = b.add_heat(20)
    print(t1)

    t2 = b.add_heat(-40)
    print(t2)