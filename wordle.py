# pip install termcolor

def print_instructions():
    '''
        welcome instructions
    '''
    cprint("Welcome to the Word Guessing Game!", 'cyan')
    print("Guess the 5-letter word within 6 attempts.")
    print("After each guess, you'll see feedback in colors:")
    colour_refernce_instructions()
    print("\nif you need help, type 'help'")
    print("Good luck and have fun!")

def colour_refernce_instructions():
    '''
        colours instructions for print_instructions()
    '''
    colour_references = [
        ["Green", "= correct, "],
        ["Yellow", "= wrong position, "],
        ["Red", "= not in word."]
    ]
        
    for reference in colour_references:
        cprint(reference[0] + " " + reference[1], reference[0].lower(), end=" ")

def get_and_validate_guess(guess_count):
    '''
        ask for guess and confirm it is a validate word
    '''
    while True:
        print("---------------")
        guess_word = input("(" + str(guess_count) + "/6) Enter a Guess: ").strip(" ").lower()
        print("---------------")
        print()

        if guess_word in all_words():
            guess_count += 1
            return guess_word, guess_count
        elif guess_word == "help":
            print_instructions()
        elif len(guess_word) <= 4:
            print("word is too short please enter a 5 letter word")
        elif len(guess_word) >= 6:
            print("word is too long please enter a 5 letter word")
        else:
            print("not a word")

def convert_guess_to_numbers(target_word, guess_word):
    target_word_list = list(target_word)
    guess_word_list = list(guess_word)

    '''
        itemizes guessed word into numbers
        0 = not in tar word
        1 = not in correct pos but is in word
        2 = in word & in correct pos
    '''
    letter_position=0
    latest_guess = []
    while letter_position < 5:
        if target_word_list[letter_position] == guess_word_list[letter_position]:
            latest_guess.append(2)
        elif guess_word_list[letter_position] in target_word:
            latest_guess.append(1)
        else:
            latest_guess.append(0)
        letter_position+=1
    return target_word_list, guess_word_list, latest_guess

def adjust_guess_for_duplicates(guess_word_list, target_word, target_word_list, latest_guess):
    '''
        if the letter is in the correct position and there is no duplicate in the target word of this letter.
        check the guess list for if it contains this letter target_word_fileice if so AND one is in the correect position assigned 2 assign the other to 0 else assign both to 1
        e.g. 
            moist = 0,1,1,1,1
            stoat = 2,2,2,0,0
        word in senario == stoic
    '''
    # Adjust latest_guess for duplicate letters in the guessed word
    for unused_value, letter in enumerate(guess_word_list):
        # If the guessed letter appears more than once
        if guess_word_list.count(letter) > 1:
            # Count occurrences of the letter in the target word
            target_letter_count = target_word.count(letter)
            guess_letter_positions = [index for index, guessed_letter in enumerate(guess_word_list) if guessed_letter == letter]

            # Track how many correct and incorrect positions we've assigned
            correct_positions = 0
            incorrect_positions = 0

            # First, mark correct positions as `2`
            for position in guess_letter_positions:
                if target_word_list[position] == letter:
                    latest_guess[position] = 2
                    correct_positions += 1

            # Then, mark incorrect positions as `1` if the target word has extra instances
            for position in guess_letter_positions:
                if latest_guess[position] != 2:
                    if correct_positions + incorrect_positions < target_letter_count:
                        latest_guess[position] = 1
                        incorrect_positions += 1
                    else:
                        latest_guess[position] = 0  # Mark extra instances as `0` if target letter count is met

def convert_number_letter_values_to_colours(guess_word_list, latest_guess, past_guesses):
    '''
        colours current word using itemised word and guessword list
    '''
    current_col_guess = []
    for index in range(5):
        if latest_guess[index] == 2:
            current_col_guess.append((guess_word_list[index], 'green'))
        elif latest_guess[index] == 1:
            current_col_guess.append((guess_word_list[index], 'yellow'))
        else:
            current_col_guess.append((guess_word_list[index], 'red'))

    past_guesses.append(current_col_guess)
    return past_guesses

def print_list_of_past_words_coloured(past_guesses):
    # prints list of past words
    for guess in past_guesses:
        for letter, color in guess:
            cprint(letter, color, end=" ")
        print()

def check_for_end_condition(latest_guess, guess_count, target_word):
    # checks for correct word or maxed guesses
    if latest_guess == [2, 2, 2, 2, 2]:
        print("Well Done!")
    elif guess_count == 6:
        print("Nice try, The word was " + str(target_word))
    else:
        return False
    
def target_word():
    #get random target word function
    target_word_file = open("target_words.txt", "r")
    return choice(target_word_file.readlines())

def total_guesses_to_file(guess_count, target_word):
    '''
        writes total guesses to file
    '''
    wordle_guesses = open("wordle_guesses.txt", "a")
    wordle_guesses.writelines("It took " + str(guess_count) + " guesses to guess the word " + target_word + "\n")
    wordle_guesses.close()

def all_words():
    all_words_file = open("all_words.txt", "r")
    all_words = all_words_file.read().split("\n")
    all_words_file.close()
    return all_words

def main(target_word):
    guess_count = 0
    past_guesses = []
    end_condition = False
    print_instructions()

    while end_condition == False:
        #guessing mechanics
        guess_word, guess_count = get_and_validate_guess(guess_count)

        # main logic
        target_word_list, guess_word_list, latest_guess = convert_guess_to_numbers(target_word, guess_word)
        adjust_guess_for_duplicates(guess_word_list, target_word, target_word_list, latest_guess)
        convert_number_letter_values_to_colours(guess_word_list, latest_guess, past_guesses)

        print_list_of_past_words_coloured(past_guesses)

        end_condition = check_for_end_condition(latest_guess, guess_count, target_word)
    total_guesses_to_file(guess_count, target_word)

from random import choice
from termcolor import cprint
main(target_word())