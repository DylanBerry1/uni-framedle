import pandas as pd
import random
import numpy as np
import math
import re

move_df = pd.read_csv('data/uni2_moves_all.csv')

def get_move(character, move) -> pd.DataFrame():
    return move_df[(move_df.chara == character) & (move_df.input == move)].iloc[0]

def get_index(i) -> pd.DataFrame():
    return move_df.iloc[i]

def generate_move() -> pd.DataFrame():
    r = random.randrange(0, 1557)
    return get_index(r)

def handle_adv_frames(adv) -> str:
    if (isinstance(adv, float) and math.isnan(adv)) or (adv == '-') or (adv == None):
        return "NA"
    if adv.lower() == "varies":
        return "Variable"
    if '~' in adv:
        return handle_adv_frames(adv.split('~')[0]), \
                handle_adv_frames(adv.split('~')[1])
    elif ' to ' in adv:
        return handle_adv_frames(adv.split(' to ')[0]), \
                handle_adv_frames(adv.split(' to ')[1])
    else:
        if '+' in adv:
            return int(re.search('\\d+', adv.split('+')[1]).group(0))
        else:
            return int(re.search('-\\d+', adv).group(0))

def handle_startup(su) -> int:
    return int(re.search('\\d+', su).group(0))

def high_low(num, target):
    if num == target:
        return "spot on!"
    elif num > target:
        return "too high!"
    else:
        return "too low!"
    

def main() -> None:
    move_choice = generate_move()
    
    count = 0
    
    print("Hello! Today, you shall be playing a wordle-like for the frame data of character's moves from Under Night In Birth 2: [sys-celes].")
    print("\n For the rules, you will guess the startup and advantage of moves. For every number you guess, it will tell you higher or lower until you have gotten all of them on the money.")
    print("\nYou will be given the character and the input for the move. Also, moves w/ variable advantage will have you guess the minimum and maximum advantage. Learn them all!!")
    
    guess_startup = -1
    guess_adv_min, guess_adv_max = -999, -999
    
    target_startup = handle_startup(move_choice.startup)
    processed_adv = handle_adv_frames(move_choice.frameAdv)
    target_guess_min, target_guess_max = -999, -999
    
    if not isinstance(processed_adv, int) and len(processed_adv) == 2:
        target_guess_min, target_guess_max = sorted(handle_adv_frames(move_choice.frameAdv))
    else:
        target_guess_min = handle_adv_frames(move_choice.frameAdv)
    
    while True:
        count += 1
        print(f"Move to guess: {move_choice.chara}, {move_choice.input}")
        
        print("Guess for startup:")
        inp = input()
        guess_startup = re.search('\\d+', inp).group(0)
        
        guess_string = ""
        result_string = ""
        
        if target_guess_max != -999:
            print("\nGuess for minimum advantage:")
            inp = input()
            guess_adv_min = re.search('-\\d+|\\d+', inp).group(0)
            
            print("\nGuess for maximum advantage:")
            inp = input()
            guess_adv_max = re.search('-\\d+|\\d+', inp).group(0)
            guess_string = f"{guess_adv_min} to {guess_adv_max}"
            result_string = f"The minimum advantage is {high_low(int(guess_adv_min), target_guess_min)} The max advantage is {high_low(int(guess_adv_max), target_guess_max)}"
        else:
            print("\nGuess for advantage:")
            inp = input()
            guess_adv_min = re.search('-\\d+|\\d+', inp).group(0)
            guess_string = f"{guess_adv_min}"
            result_string = f"The advantage you have guessed is {high_low(int(guess_adv_min), target_guess_min)}"
            
        print(f"Recap: You guessed that the startup of {move_choice.chara}'s {move_choice.input} is {guess_startup}, and that the advantage is {guess_string}.")
        
        print(f"For the startup, your guess is {high_low(int(guess_startup), target_startup)} {result_string}")
        
        if high_low(int(guess_startup), target_startup) == 'spot on!' and high_low(int(guess_adv_min), target_guess_min) == 'spot on!' and high_low(int(guess_adv_max), target_guess_max) == 'spot on!':
            break

    print(f"Congratulations! You got it in {count}!")
        