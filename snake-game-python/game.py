import pygame
from pygame.locals import *
import time, random

SIZE = 40
BACKGROUND_COLOR = ( 0, 0, 0 )

class Flower:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("snake-game-python/files/flower.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint( 1, 10 )*SIZE
        self.y = random.randint( 1, 10 )*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("snake-game-python/files/snake.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def crawl(self):
        
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game  , Exit => Escape, Play : up down right left")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((800, 600))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.flower = Flower(self.surface)
        self.flower.draw()

    def play_background_music(self):
        pygame.mixer.music.load('snake-game-python/files/bg_music.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("snake-game-python/files/crash.mp3")
        elif sound_name == 'score':
            sound = pygame.mixer.Sound("snake-game-python/files/score.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.flower = Flower(self.surface)

    def hit(self, x_snake, y_snake, x_flower, y_flower):
        if x_snake >= x_flower and x_snake < x_flower + SIZE:
            if y_snake >= y_flower and y_snake < y_flower + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("snake-game-python/files/background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.crawl()
        self.flower.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.hit(self.snake.x[0], self.snake.y[0], self.flower.x, self.flower.y):
            self.play_sound("score")
            self.snake.increase_length()
            self.flower.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.hit(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

    def display_score(self):
        font = pygame.font.SysFont('arial',25)
        score = font.render(f"YOUR SCORE: {self.snake.length - 1}",True,(200,200,200))
        self.surface.blit(score,(400,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over :(  SCORE : {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Play again => Enter,  Exit game -> Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep( 0.2 )

if __name__ == '__main__':
    game = Game()
    game.run()