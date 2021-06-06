import math

sep = "__&__"


class TwoBodyModel:
    def __init__(self):
        # First two elements are x and y positions, and second two are x and y components of velocity
        self.u = [0.0, 0.0, 0.0, 0.0]
        self.masses = {
            'q': 0.0,  # Current mass ratio m2 / m1
            'm1': 1.0,
            'm2': 0.0,  # Will be set to q
            'm12': 0.0  # Will be set to m1 + m2
        }
        self.eccentricity = 0.0
        self.positions = [[0.0, 0.0], [0.0, 0.0]]

    def __str__(self):
        output = ""
        for i in range(2):  # number of bodies
            for j in range(2):  # number of coordinates
                output += "{:.6f}".format(self.positions[i][j]) + (sep if (i * j != 1) else "\n")
        return output


def euler_calculate(h: float, u: list, derivative):
    # h: time_step
    # u: variables
    # derivative: function that calculates the derivatives
    dimension = len(u)
    du = derivative()

    for i in range(dimension):
        u[i] = u[i] + h * du[i]


def runge_kutta_calculate(h: float, u: list, derivative):
    """Runge-Kutta numerical integration"""
    # h: time_step
    # u: variables
    # derivative: function that calculates the derivatives
    a = [h / 2, h / 2, h, 0]
    b = [h / 6, h / 3, h / 3, h / 6]
    dimension = len(u)
    u0 = list(u)  # copy of that list
    ut = [0.0 for _ in range(dimension)]

    for j in range(dimension):
        du = derivative()

        for i in range(dimension):
            u[i] = u0[i] + a[j] * du[i]
            ut[i] = ut[i] + b[j] * du[i]

    for i in range(dimension):
        u[i] = u0[i] + ut[i]


class TwoBodyController:
    def __init__(self):
        self.T = 0
        self.dt = 0
        self.q = 0
        self.eccentricity = 0
        self.method = "runge-kutta"
        self.velocity = 0
        self.model = TwoBodyModel()
        self.file = None

    def derivative(self):
        du = [0.0 for _ in range(len(self.model.u))]

        # x and y coordinates
        r = self.model.u[0:2]

        # Distance between bodies
        rr = math.sqrt(pow(r[0], 2) + pow(r[1], 2))

        for i in range(2):
            du[i] = self.model.u[i + 2]
            du[i + 2] = -(1 + self.model.masses['q']) * r[i] / pow(rr, 3)

        return du

    def update_position(self):
        if self.method == 'runge-kutta':
            runge_kutta_calculate(self.dt, self.model.u, self.derivative)
        if self.method == 'euler':
            euler_calculate(self.dt, self.model.u, self.derivative)
        self.calculate_new_position()

    def calculate_new_position(self):
        r = 1
        a1 = (self.model.masses['m2'] / self.model.masses['m12'] * r)
        a2 = (self.model.masses['m1'] / self.model.masses['m12'] * r)

        self.model.positions = [
            [
                -a2 * self.model.u[0],
                -a2 * self.model.u[1],
            ],
            [
                a1 * self.model.u[0],
                a1 * self.model.u[1],
            ],
        ]

    def take_user_input(self):
        self.T = int(input("T (e.g. 120): "))
        self.dt = float(input("δt (e.g. 0.01): "))
        self.q = float(input("mass ratio (e.g. 0.5): "))
        self.eccentricity = float(input("eccentricity (e.g. 0.7): "))
        self.method = input("method (e.g. runge-kutta/euler): ")

        """Stable orbit reset"""
        self.model.u[0] = 1
        self.model.u[1] = 0
        self.model.u[2] = 0
        self.model.u[3] = math.sqrt((1 + self.q) * (1 + self.eccentricity))

        """Update masses"""
        self.model.masses['q'] = self.q
        self.model.masses['m1'] = 1
        self.model.masses['m2'] = self.q  # since m1 is 1 then m2 should be q cuz q= m2 / m1
        self.model.masses['m12'] = 1 + self.q

    def print_step(self):
        if self.file is None:
            file = open("simulation.txt", "w")
            first_line = ""
            arr = [
                "T={}".format(self.T),
                "dt={:.2f}".format(self.dt),
                "q={:.2f}".format(self.q),
                "eccentricity={:.2f}".format(self.eccentricity),
                "method={}".format(self.method),
                "m1={}".format(self.model.masses['m1']),
                "m2={}".format(self.model.masses['m2']),
            ]
            for i in range(len(arr)):
                first_line += str(arr[i]) + (sep if i != len(arr) - 1 else "\n")
            file.write(first_line)
            self.file = file

        self.file.write(str(self.model))

    def start_simulation(self):
        time_left = self.T
        while time_left > 0:
            self.update_position()
            self.print_step()
            time_left -= self.dt
        self.file.close()
        print("Done!")


def app():
    controller = TwoBodyController()
    controller.take_user_input()
    controller.start_simulation()


if __name__ == '__main__':
    app()
