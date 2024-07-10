from curses.textpad import rectangle
import pygame, random

# Initialize Pygame
pygame.init()

# Set up display
WINDOW_SIZE = 800
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Sorting Algorithm Visualization')

# Define colors
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTBLUE = (0, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (211, 211, 211)

# Variables
BAR_WIDTH = 20
clock = pygame.time.Clock()
FPS = 20

# Bar class definition
class Bar:
    def __init__(self, x, height, color):
        self.color = color
        self.x = x
        self.width = BAR_WIDTH
        self.height = height

    def select(self):
        self.color = BLUE

    def unselect(self):
        self.color = PURPLE

    def set_smallest(self):
        self.color = LIGHTBLUE

    def set_sorted(self):
        self.color = GREEN

# Function to create bars
def create_bars():
    num_bars = WINDOW_SIZE // BAR_WIDTH - 5
    bars = []
    heights = []

    for i in range(5, num_bars):
        height = random.randint(10, WINDOW_SIZE)
        while height in heights:
            height = random.randint(10, WINDOW_SIZE)

        heights.append(height)
        bar = Bar(i * BAR_WIDTH, height, PURPLE)
        bars.append(bar)

    return bars

# Function to draw bars
def draw_bars(bars):
    WINDOW.fill(LIGHTGREY)

    for bar in bars:
        pygame.draw.rect(WINDOW, bar.color, (bar.x, WINDOW_SIZE - bar.height, bar.width, bar.height))
        pygame.draw.line(WINDOW, (255, 255, 255), (bar.x, WINDOW_SIZE), (bar.x, WINDOW_SIZE - bar.height), 1)
        pygame.draw.line(WINDOW, (255, 255, 255), (bar.x + bar.width, WINDOW_SIZE), (bar.x + bar.width, WINDOW_SIZE - bar.height), 1)
        pygame.draw.line(WINDOW, (255, 255, 255), (bar.x, WINDOW_SIZE - bar.height), (bar.x + bar.width, WINDOW_SIZE - bar.height), 1)

# Selection sort algorithm
def selection_sort(bars):
    for i in range(len(bars)):
        min_idx = i
        bars[i].set_smallest()

        for j in range(i + 1, len(bars)):
            bars[j].select()
            draw_bars(bars)
            pygame.display.update()

            if bars[j].height < bars[min_idx].height:
                bars[min_idx].unselect()
                min_idx = j

            bars[min_idx].set_smallest()
            draw_bars(bars)
            pygame.display.update()
            bars[j].unselect()

            yield

        bars[i].x, bars[min_idx].x = bars[min_idx].x, bars[i].x
        bars[i], bars[min_idx] = bars[min_idx], bars[i]

        bars[min_idx].unselect()
        bars[i].set_sorted()

        draw_bars(bars)

# Function to display text
def display_text(txt, x, y, size, color):
    FONT = pygame.font.SysFont('Arial', size)
    text = FONT.render(txt, True, color)
    text_rect = text.get_rect(center=(x, y))
    WINDOW.blit(text, text_rect)

# Main function
def main():
    bars = create_bars()
    draw_bars(bars)
    sorting_generator = selection_sort(bars)

    run = True
    sorting = False
    while run:
        clock.tick(FPS)
        draw_bars(bars)

        if sorting:
            try:
                next(sorting_generator)
            except StopIteration:
                sorting = False
        else:
            draw_bars(bars)

        display_text("Selection Sort", WINDOW_SIZE / 2, 20, 40, BLACK)
        display_text("Press SPACE to start sorting or Press R to reset", WINDOW_SIZE / 2, 60, 30, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sorting = not sorting
                if event.key == pygame.K_r:
                    bars = create_bars()
                    sorting_generator = selection_sort(bars)
                    sorting = False

        pygame.display.update()

    pygame.quit()

# Entry point
if __name__ == "__main__":
    main()
