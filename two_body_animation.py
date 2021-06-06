import pygame
from pygame.locals import (
    KEYDOWN, KEYUP, K_SPACE, K_q, QUIT, K_r
)


def get_simulation_output_data():
    txt_file = open("simulation.txt", "r")
    count = 0
    for _ in txt_file:
        count = count + 1
    data = [[0.0 for _ in range(4)] for _ in range(count - 1)]

    txt_file.close()
    txt_file = open("simulation.txt", "r")
    line = txt_file.readline()

    first_line = line
    first_line = first_line.split("__&__")
    values = {}

    for i in range(len(first_line)):
        splitting = first_line[i].split("=")
        if splitting[0] != "method":
            values[splitting[0]] = float(splitting[1])
        else:
            values[splitting[0]] = splitting[1]

    for i in range(count - 1):
        line = txt_file.readline()
        line = [float(x) for x in line.split("__&__")]
        data[i] = line

    return values, data
    # end of read_simulation_output //


class TwoBodyView:
    def __init__(self):
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 1000
        self.screen = None
        # states; -1 = not initialized | 0 = stopped | 1 = playing
        self.state = -1
        self.step = 0
        self.values = {}
        self.data = []
        self.path1 = []
        self.path2 = []

    def initialize_screen(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        self.state = 0

    def play(self):
        self.state = 1
        while self.state != -1:
            self.key_board_listener(pygame.event.get())
            self.draw_scene()
            if self.state == 1:
                self.step += 1

    def draw_scene(self):
        if self.state == -1:
            return
        if self.step == len(self.data):
            return self.quit()

        """Draw Scene"""
        self.screen.fill((0, 0, 0))
        points = self.data[self.step]
        scale = 100
        mid_x = self.SCREEN_WIDTH / 2
        mid_y = self.SCREEN_HEIGHT / 2
        ball2 = [(255, 0, 0), 10]
        ball1 = [(0, 255, 255), 10 * self.values['q']]

        ball1_x = mid_x + points[0] * scale
        ball1_y = mid_y + points[1] * scale
        ball2_x = mid_x + points[2] * scale
        ball2_y = mid_y + points[3] * scale

        if self.state == 1:
            self.path1.append([ball1_x, ball1_y])
            self.path2.append([ball2_x, ball2_y])

        if len(self.path1) > 1:
            pygame.draw.lines(self.screen, ball1[0], False, self.path1)
        if len(self.path2) > 1:
            pygame.draw.lines(self.screen, ball2[0], False, self.path2)

        pygame.draw.circle(self.screen, ball1[0], (ball1_x, ball1_y), ball1[1])
        pygame.draw.circle(self.screen, ball2[0], (ball2_x, ball2_y), ball2[1])
        pygame.display.flip()

    def stop(self):
        self.state = 0

    def replay(self):
        self.state = 0
        self.step = 0
        self.path1 = []
        self.path2 = []
        self.play()

    def quit(self):
        self.state = -1
        self.screen = None
        pygame.quit()

    def key_board_listener(self, events):
        for event in events:
            if event.type == QUIT:
                return self.quit()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    return self.quit()
                if event.key == K_SPACE:
                    if self.state == 1:
                        self.state = 0
                        return
                    self.state = 1
                if event.key == K_r:
                    self.replay()


def app():
    values, data = get_simulation_output_data()
    view = TwoBodyView()
    view.values = values
    view.data = data
    view.initialize_screen()
    view.play()


if __name__ == '__main__':
    app()
