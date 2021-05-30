import pygame
from pygame.locals import (
    KEYDOWN, KEYUP, K_SPACE, K_q, QUIT, K_r
)


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
        self.read_simulation_output()

    def read_simulation_output(self):
        txt_file = open("simulation.txt", "r")
        count = 0
        for _ in txt_file:
            count = count + 1
        self.data = [[0.0 for _ in range(4)] for _ in range(count - 1)]

        txt_file.close()
        txt_file = open("simulation.txt", "r")
        line = txt_file.readline()

        # ilk satırı dictionary ile istediğimiz veriye ulaşabilmek için böyle yaptım
        first_line = line
        first_line = first_line.split("__&__")
        self.values = {}

        for i in range(len(first_line)):
            splitting = first_line[i].split("=")
            if splitting[0] != "method":
                self.values[splitting[0]] = float(splitting[1])
            else:
                self.values[splitting[0]] = splitting[1]

        # burası diğer satırların two dimensional hali
        for i in range(count - 1):
            line = txt_file.readline()
            line = [float(x) for x in line.split("__&__")]
            self.data[i] = line

        # end of read_simulation_output //

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
        ball2_x = mid_x + points[2] * scale * -1
        ball2_y = mid_y + points[3] * scale * -1

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


if __name__ == '__main__':
    view = TwoBodyView()
    view.initialize_screen()
    view.play()

    # # Simple pygame program
    # # Import and initialize the pygame library
    # import pygame
    #
    # pygame.init()
    #
    # # Set up the drawing window
    # screen = pygame.display.set_mode([500, 500])
    #
    # # Run until the user asks to quit
    # running = True
    # while running:
    #
    #     # Did the user click the window close button?
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         if event.type == KEYDOWN:
    #             if event.key == K_SPACE:
    #                 print("space pressed")
    #
    #     # Fill the background with white
    #     screen.fill((255, 255, 255))
    #
    #     # Draw a solid blue circle in the center
    #     pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    #
    #     # Flip the display
    #     pygame.display.flip()
    #
    # # Done! Time to quit.
    # pygame.quit()
