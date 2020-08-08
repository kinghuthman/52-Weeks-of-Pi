#buttonInput.py
import RPi.GPIO as GPIO
import threading
import random
import os
import time
from subprocess import call


#set up numbering mode to use for channels
#BOARD - use pi board numbers
#BCM - use Broadcom GPIO OO..nn numbers
#GPIO.setmode(GPIO.BCM)

sleepTime = .1

# blue, yellow
LIGHTS = [4, 27]
RANDOMLIGHTS = [4, 23, 24, 27]
BUTTONS = [17, 22]

# values to adjust game play
speed = 0.25
use_sounds = False

# flags used to signal game status
is_displaying_pattern = False
is_won_current_level = False
is_game_over = True
reset_game = False
high_score = 0
previous_high_score = 0

# game state
current_level = 1
current_step_of_level = 0
pattern = []

def initialize_gpio():
    #GPIO.setmode(GPIO.BOARD)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RANDOMLIGHTS, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for i in range(2):
        GPIO.add_event_detect(BUTTONS[i], GPIO.FALLING, verify_player_selection, 400 if use_sounds else 250)
        
def reset_game_button(channel):
    reset_game = True
        
def verify_player_selection(channel):
    global current_step_of_level, current_level, is_won_current_level, is_game_over, reset_game
    if is_game_over:
            is_game_over = False
            time.sleep(2)
    if not is_displaying_pattern and not is_won_current_level and not is_game_over and not reset_game:
        #play_note(NOTES[BUTTONS.index(channel)])
        flash_led_for_button(channel)
        if channel == BUTTONS[pattern[current_step_of_level]]:
            current_step_of_level += 1
            if current_step_of_level >= current_level:
                current_level += 1
                is_won_current_level = True
        else:
            is_game_over = True
            
            #function for wrong color pressed
            
def flash_led_for_button(button_channel):
    led = LIGHTS[BUTTONS.index(button_channel)]
    GPIO.output(led, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(led, GPIO.LOW)
    
def add_new_color_to_pattern():
    global is_won_current_level, current_step_of_level
    is_won_current_level = False
    current_step_of_level = 0
    next_color = random.randint(0, 1)
    pattern.append(next_color)
    
def display_pattern_to_player():
    global is_displaying_pattern
    is_displaying_pattern = True
    GPIO.output(LIGHTS, GPIO.LOW)
    for i in range(current_level):
        #play_note(NOTES[pattern[i]])
        GPIO.output(LIGHTS[pattern[i]], GPIO.HIGH)
        time.sleep(speed)
        GPIO.output(LIGHTS[pattern[i]], GPIO.LOW)
        time.sleep(speed)
    is_displaying_pattern = False
    
def wait_for_player_to_repeat_pattern():
    while not is_won_current_level and not is_game_over:
        time.sleep(0.3)
        
def wait_for_reset():
    #global reset_game
    #if reset_game:
    #    reset_board_for_new_game()
    #else:
    game_over()
        
        
def reset_board_for_new_game():
    global is_displaying_pattern, is_won_current_level, is_game_over
    global current_level, current_step_of_level, pattern
    is_displaying_pattern = False
    is_won_current_level = False
    is_game_over = False
    current_level = 1
    current_step_of_level = 0
    pattern = []
    GPIO.output(LIGHTS, GPIO.LOW)
    
def wrong_score():
    time.sleep(.5) 
    GPIO.output(24, True)
    time.sleep(.3) 
    GPIO.output(24, False)
    time.sleep(.3) 
    GPIO.output(24, True)
    time.sleep(.3) 
    GPIO.output(24, False)
    time.sleep(.3) 
    GPIO.output(24, True)
    time.sleep(.3) 
    GPIO.output(24, False)

def calculating_score():
    time.sleep(.5)
    GPIO.output(24, True)
    time.sleep(.1) 
    GPIO.output(24, False)
    time.sleep(.1) 
    GPIO.output(4, True)
    time.sleep(.1) 
    GPIO.output(4, False)
    time.sleep(.1) 
    GPIO.output(27, True)
    time.sleep(.1) 
    GPIO.output(27, False)
    time.sleep(.1) 
    GPIO.output(23, True)
    time.sleep(.1) 
    GPIO.output(23, False)
    time.sleep(.1) 
    GPIO.output(27, True)
    time.sleep(.1) 
    GPIO.output(27, False)
    time.sleep(.1) 
    GPIO.output(4, True)
    time.sleep(.1) 
    GPIO.output(4, False)
    time.sleep(.1)
    GPIO.output(24, True)
    time.sleep(.1) 
    GPIO.output(24, False)
    time.sleep(.1) 
    GPIO.output(4, True)
    time.sleep(.1) 
    GPIO.output(4, False)
    time.sleep(.1) 
    GPIO.output(27, True)
    time.sleep(.1) 
    GPIO.output(27, False)
    time.sleep(.1) 
    GPIO.output(23, True)
    time.sleep(.1) 
    GPIO.output(23, False)
    time.sleep(.1) 
    GPIO.output(27, True)
    time.sleep(.1) 
    GPIO.output(27, False)
    time.sleep(.1) 
    GPIO.output(4, True)
    time.sleep(.1) 
    GPIO.output(4, False)
    time.sleep(.1)
    GPIO.output(24, True)
    time.sleep(.1) 
    GPIO.output(24, False)
    time.sleep(.1) 
    GPIO.output(4, True)
    time.sleep(.1) 
    GPIO.output(4, False)
    time.sleep(.1) 
    GPIO.output(27, True)
    time.sleep(.1) 
    GPIO.output(27, False)
    time.sleep(.1) 
    GPIO.output(23, True)
    time.sleep(.1) 
    GPIO.output(23, False)
    time.sleep(.1) 
    GPIO.output(27, True)
    time.sleep(.1) 
    GPIO.output(27, False)
    time.sleep(.1) 
    GPIO.output(4, True)
    time.sleep(.1) 
    GPIO.output(4, False)
    time.sleep(.1)
    GPIO.output(24, True)
    time.sleep(.1) 
    GPIO.output(24, False)
    
# red is 24, green is 23, yello is 27, blue is 4
    
def total_score():
    global high_score, previous_high_score
    time.sleep(1.5)
    if (current_level - 1) > high_score:
        previous_high_score = high_score
        high_score = current_level - 1
        new_high_score()
        for i in range(previous_high_score):
            time.sleep(.2)
            GPIO.output(24, True)
            time.sleep(.6)
            GPIO.output(24, False)
            time.sleep(.4)
        time.sleep(1)
        for i in range(high_score):
            time.sleep(.4) 
            GPIO.output(23, True)
            time.sleep(1) 
            GPIO.output(23, False)
            time.sleep(.7)    
        
    else:
        for x in range(current_level - 1):
            time.sleep(.4)
            GPIO.output(24, True)
            time.sleep(1)
            GPIO.output(24, False)
            time.sleep(.4)
        time.sleep(1)
        for i in range(high_score):
                time.sleep(.2) 
                GPIO.output(23, True)
                time.sleep(.6) 
                GPIO.output(23, False)
                time.sleep(.4)
    calculating_score()
    time.sleep(1.5)

def new_high_score():
    GPIO.output(4, True)
    time.sleep(.1) 
    GPIO.output(4, False)
    time.sleep(.1)
    GPIO.output(27, True) 
    time.sleep(.1) 
    GPIO.output(27, False) 
    time.sleep(.1)
    GPIO.output(4, True) 
    time.sleep(.1)
    GPIO.output(4, False)
    time.sleep(.1)
    GPIO.output(27, True) 
    time.sleep(.1)
    GPIO.output(27, False)
    time.sleep(.1)
    GPIO.output(4, True)
    time.sleep(.1) 
    GPIO.output(4, False)
    time.sleep(.1)
    GPIO.output(27, True) 
    time.sleep(.1) 
    GPIO.output(27, False) 
    time.sleep(.1)
    GPIO.output(4, True) 
    time.sleep(.1)
    GPIO.output(4, False)
    time.sleep(.1)
    GPIO.output(27, True) 
    time.sleep(.1)
    GPIO.output(27, False)
    time.sleep(.1)
    GPIO.output(4, True)
    time.sleep(.1) 
    GPIO.output(4, False)
    time.sleep(.1)
    GPIO.output(27, True) 
    time.sleep(.1) 
    GPIO.output(27, False) 
    time.sleep(.1)
    GPIO.output(4, True) 
    time.sleep(.1)
    GPIO.output(4, False)
    time.sleep(.1)
    GPIO.output(27, True) 
    time.sleep(.1)
    GPIO.output(27, False)
    time.sleep(.1)
    GPIO.output(4, True)
    time.sleep(.1) 
    GPIO.output(4, False)
    time.sleep(.1)
    GPIO.output(27, True) 
    time.sleep(.1) 
    GPIO.output(27, False) 
    time.sleep(.1)
    GPIO.output(4, True) 
    time.sleep(.1)
    GPIO.output(4, False)
    time.sleep(.1)
    GPIO.output(27, True) 
    time.sleep(.1)
    GPIO.output(27, False)
    time.sleep(1)

    
    
def game_over():
    global reset_game
    
    while is_game_over:
        for i in range(1):
            x = random.randint(0, 3)
            time.sleep(.5) 
            GPIO.output(RANDOMLIGHTS[x], True)
            time.sleep(.1) 
            GPIO.output(RANDOMLIGHTS[x], False)
    reset_board_for_new_game()
    time.sleep(.5)
    calculating_score()
    start_game()
        
def start_game():

    time.sleep(2)
    # method to wait for player input to start game, set reference to true, light stays green
    #while "reference" ...etc
    if is_game_over:
        wait_for_reset()
    while True:
        add_new_color_to_pattern()
        display_pattern_to_player()
        wait_for_player_to_repeat_pattern()
        if is_game_over:
            # function to display score counter, use current_level - 1
            print("Game Over! Your max score was {} colors!\n".format(current_level-1))
#             wrong_score()
            calculating_score()
            total_score()
            wait_for_reset()
            play_again = input("Enter 'Y' to play again, or just press [ENTER] to exit.\n")
            if play_again == "Y" or play_again == "y":
                reset_board_for_new_game()
                print("Begin new round!\n")
            else:
                print("Thanks for playing!\n")
                break
        time.sleep(2)
        
def start_game_monitor():
    t = threading.Thread(target=start_game)
    t.daemon = True
    t.start()
    t.join()
    
def main():
    try:
        #call(["sonic_pi", "set_sched_ahead_time! 0"])
        #call(["sonic_pi", "use_debug false"])
        #call(["sonic_pi", "use_synth :pulse"])
        #call(["sonic_pi", "use_bpm 100"])
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Begin new round!\n")
        initialize_gpio()
        start_game_monitor()
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()

#Simon Says

#pseudocode
#While gameOver is False
#     Add a new colour to the sequence.
#     display light sequence
#     For tries in length of sequence
#          get the user button press
#          if the button is incorrect
#                mark as incorrect
#                break
#         else
#                mark as correct
#     If user was correct
#         give user an extra point
#         continue
#     else
#          gameOver = True


#### led blinks on button press
#GPIO 4 aka pin 7
#blueLed = 4
#GPIO 17 aka pin 11
#blueButton = 17
#GPIO 27 aka pin 13
#yellowLed = 27
#GPIO 22 aka pin 15
#yellowButton = 22