import pygame

import mediapipe as mp

import time

import random

# Initialize Pygame

pygame.init()

# Define colors

BLACK = (0, 0, 0)

WHITE = (255, 255, 255)

PINK = (255, 0, 255)

# Set up the window

screen_width = 1280

screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Rock Paper Scissors")

# Load the background image

bg_image = pygame.image.load('Resources/BG.png').convert()

# Load the hand images

hand_images = [

    pygame.image.load('Resources/1.png').convert_alpha(),

    pygame.image.load('Resources/2.png').convert_alpha(),

    pygame.image.load('Resources/3.png').convert_alpha(),

]

# Set up the hand detector

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(max_num_hands=1)

# Set up the game variables

timer = 0

stateResult = False

startGame = False

scores = [0, 0]

while True:

    # Handle events

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            quit()

    # Capture the webcam image

    ret, frame = cv2.VideoCapture(0).read()

    frame = cv2.flip(frame, 1)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect the hand

    results = hands.process(frame)

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        fingers = [1 if lm.tip_position.y < hand.landmark[0].y else 0 for lm in hand.landmark[1:]]

        if fingers == [0, 0, 0, 0, 0]:

            playerMove = 1

        elif fingers == [1, 1, 1, 1, 1]:

            playerMove = 2

        elif fingers == [0, 1, 1, 0, 0]:

            playerMove = 3

        else:

            playerMove = None

    else:

        playerMove = None

    # Start the game

    if startGame:

        if stateResult is False:

            timer = time.time() - initialTime

            if timer > 3:

                stateResult = True

                timer = 0

                randomNumber = random.randint(1, 3)

                # Display the AI's move

                ai_image = hand_images[randomNumber - 1]

                ai_rect = ai_image.get_rect(center=(screen_width // 2, screen_height // 2))

                screen.blit(ai_image, ai_rect)

                # Determine the winner

                if (playerMove == 1 and randomNumber == 3) or \

                    (playerMove == 2 and randomNumber == 1) or \

                    (playerMove == 3 and randomNumber == 2):

                    scores[1] += 1

                elif (playerMove == 3 and randomNumber == 1) or \

                    (playerMove == 1 and randomNumber == 2) or \

                    (playerMove == 2 and randomNumber == 3):

                    scores[0] += 1

    # Display the webcam image and the game UI

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    frame = cv2.flip(frame, 1)

    frame = cv2.resize(frame, (

screen_width, screen_height))
    # Display the player's move

if playerMove is not None:

    player_image = hand_images[playerMove - 1]

    player_rect = player_image.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

    screen.blit(player_image, player_rect)

# Display the scores

font = pygame.font.SysFont('arial', 50)

player_score = font.render('Player: ' + str(scores[0]), True, WHITE)

ai_score = font.render('AI: ' + str(scores[1]), True, WHITE)

screen.blit(player_score, (50, 50))

screen.blit(ai_score, (screen_width - ai_score.get_width() - 50, 50))

# Display the timer

if stateResult is False and startGame is True:

    font = pygame.font.SysFont('arial', 100)

    timer_text = font.render(str(int(3 - timer)), True, PINK)

    timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

    screen.blit(timer_text, timer_rect)

# Start the game with a hand gesture

if playerMove is not None and startGame is False:

    initialTime = time.time()

    startGame = True

# Reset the game after a result

if stateResult is True:

    if timer > 2:

        stateResult = False

        startGame = False

        timer = 0

# Update the display

pygame.display.update()

frame = pygame.surfarray.make_surface(frame)

screen.blit(frame, (0, 0))

screen.blit(bg_image, (0, 0))
