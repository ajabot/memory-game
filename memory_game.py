#!/usr/bin/python

from gpiozero import LED
from gpiozero import Button
import time
import random

red_led = LED(5)
green_led = LED(6)
yellow_led = LED(13)
blue_led = LED(19)
success_led = LED(22)
error_led = LED(27)

red_button = Button(21, False)
green_button = Button(20, False)
yellow_button = Button(16, False)
blue_button = Button(12, False)

print("Memory game")
leds_out = {
    "r": red_led,
    "g": green_led,
    "y": yellow_led,
    "b": blue_led,
    "success": success_led,
    "error": error_led
}

leds_choices = 'rgyb'
memory_chain = ''.join(random.choice(leds_choices) for i in range(3))

def blink_all_leds(nb_blinks):
    leds_out['r'].blink(0.5, 0.5, nb_blinks)
    leds_out['g'].blink(0.5, 0.5, nb_blinks)
    leds_out['y'].blink(0.5, 0.5, nb_blinks)
    leds_out['b'].blink(0.5, 0.5, nb_blinks)

    time.sleep(3)

def flash_led(led):
    leds_out[led].on()
    time.sleep(1)  
    leds_out[led].off()
    time.sleep(0.3)

def display_chain(memory_chain):
    print(memory_chain)
    for led in memory_chain:
        flash_led(led)

blink_all_leds(3)

user_chain = ''

def check_user_input():
    global user_chain
    global memory_chain
    global user_input
    global over

    for index, letter in enumerate(user_chain):
        if letter != memory_chain[index]:
            #if there is an error, the game is over
            flash_led("error")
            user_input = False
            over = True
    
    if len(user_chain) == len(memory_chain):
        #if the input is the same length as the memory chain
        # then the turn is over 
        flash_led("success")
        user_input = False

def input_button(button):
    global user_chain
    global user_input
    global user_timer

    if user_input:
        user_chain += button
        #check the input
        check_user_input()
        #we reset the user timer each time a button is pressed
        user_timer = time.time()

def when_red_released():
    input_button('r')

def when_green_released():
    input_button('g')

def when_yellow_released():
    input_button('y')

def when_blue_released():
    input_button('b')

def activate_buttons():
    red_button.when_released = when_red_released
    green_button.when_released = when_green_released
    yellow_button.when_released = when_yellow_released
    blue_button.when_released = when_blue_released

def deactivate_buttons():
    red_button.when_released = None
    green_button.when_released = None
    yellow_button.when_released = None
    blue_button.when_released = None

user_input = False
over = False
level = 1

while not over:
    print("Level " + str(level) + ":")
    print("Computer turn")
    display_chain(memory_chain)
    user_input = True
    user_timer = time.time()
    user_chain = ''
    print("User turn")
    activate_buttons()
    while user_input:
        now = time.time()
        #10 seconds without input ends users turn
        if now - user_timer >= 10:
            print("End Turn")
            user_input = False
        #little break to avoid issue with input
        time.sleep(0.1)
    print(user_chain)
    #buttons are "deactivated" to avoid unwanted input (sometimes from turning on led) when it's computer turn 
    deactivate_buttons()
    level += 1
    memory_chain += random.choice(leds_choices)

print("Game over")