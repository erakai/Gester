from subprocess import Popen
import math
import pygame


"""
The main "launcher" for all other games in Gester.
"""

# Each tuple should be: (Name, Path to .py runner, Path to gallery image)
GAMES = [
    (
        "Box Stacker",
        "games/box-stacker/box_stacker.py",
        "games/assets/gallery-covers/box-stacker.jpeg",
    ),
    (
        "Pong",
        "games/pong/pong.py",
        "games/assets/gallery-covers/pong.jpeg",
    ),
    (
        "Casino",
        "games/slot-machine/slots.py",
        "games/assets/gallery-covers/casino.png",
    ),
    (
        "2048",
        "games/2048/2048.py",
        "games/assets/gallery-covers/2048.jpeg",
    ),
    (
        "Hand Visualization",
        "games/hand-visualizer/hand_visualization.py",
        "games/assets/gallery-covers/hand-visualizer.jpeg",
    ),
    (
        "Simon Says", 
        "games/SimonSays/SimonSays.py", 
        "games/assets/gallery-covers/SimonSays.png"
    ),
    (
        "Pikachu Tomodachi",
        "games/Tomodachi/Tomodachi.py",
        "games/assets/gallery-covers/Pikachu_cover.png"
    ),
    (
        "Drake Tomodachi",
        "games/Tomodachi/Drake.py",
        "games/assets/gallery-covers/drake_cover.png"
    )
]
COLUMN_COUNT = 5
COVER_SIZE_X = 250
COVER_SIZE_Y = 150
X_SPACING = 25
Y_SPACING = 55


def launch_game(index: int):
    Popen(["python3", GAMES[index][1]])


"""
====================================================
======================Pygame========================
====================================================
"""
pygame.init()

title_font = pygame.font.SysFont("Comic Sans MS", 40)
label_font = pygame.font.SysFont("Comic Sans MS", 20)

screen = pygame.display.set_mode(
    [
        (COVER_SIZE_X + X_SPACING) * COLUMN_COUNT + 40,
        (COVER_SIZE_Y + Y_SPACING) * math.ceil(len(GAMES) / COLUMN_COUNT) + 80 + 80,
    ]
)

cover_images = []
for game in GAMES:
    cover = pygame.image.load(game[2])
    cover = pygame.transform.scale(cover, (COVER_SIZE_X, COVER_SIZE_Y))
    cover_images.append(cover)

title_text = title_font.render("Games Gallery", False, (255, 255, 255))
labels = []
for game in GAMES:
    text = label_font.render(game[0], False, (255, 255, 255))
    labels.append(text)

game_rects = []
for i, game in enumerate(GAMES):
    x = 20 + (i % COLUMN_COUNT) * (COVER_SIZE_X + X_SPACING)
    y = 80 + 20 + ((i // COLUMN_COUNT) * (COVER_SIZE_Y + Y_SPACING))
    detect_rect = pygame.Rect(x, y, COVER_SIZE_X, COVER_SIZE_Y)
    game_rects.append((x, y, detect_rect))

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            for i, (x, y, rect) in enumerate(game_rects):
                if rect.collidepoint(pos):
                    launch_game(i)
                    break

    screen.fill((35, 62, 107))
    screen.blit(title_text, (20, 20))

    # Rendering
    for i, game in enumerate(GAMES):
        name = game[0]
        image = cover_images[i]

        x = game_rects[i][0]
        y = game_rects[i][1]
        screen.blit(image, (x, y))
        border_color = (3, 14, 38)
        if game_rects[i][2].collidepoint(mouse_pos):
            border_color = (255, 255, 255)
        for j in range(4):
            pygame.draw.rect(
                screen, border_color, (x - j, y - j, COVER_SIZE_X, COVER_SIZE_Y), 5
            )

        screen.blit(labels[i], (x + 1, y + COVER_SIZE_Y + 5))

    pygame.display.flip()


pygame.quit()
