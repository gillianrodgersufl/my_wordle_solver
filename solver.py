import common_letter
import numpy as np
import csv

def generate_csv():
    #load in file
    wordle_data = np.loadtxt("wordle.txt", dtype='str')
    with open("./word_ranks.csv", 'w') as file:
        ranked_words = rank_words(wordle_data, '')
        #write as dict to csv
        for key, value in ranked_words.items():
            file.write(f"{key}: {value}\n")
    


def generate_guess(current_guess, guess_array, first):
    #if this is the first guess, regenerate list
    if first:
        generate_csv()
    #read data into dict
    wordle_data = np.loadtxt("wordle.txt", dtype='str')
    with open("word_ranks.csv", 'r') as file:
        reader = csv.DictReader(file)
        ranked_words = {}
        for row in file:
            key, value = row.strip().split(':')
            ranked_words[key.strip()] = value.strip()
    #filtering guesses down based on previous guess
    result_words = filter_words(ranked_words, current_guess, guess_array)
    #taking top guess
    if len(result_words) > 0:
        new_guess = next(iter(result_words))
    #ensuring no repeated guesses
    if new_guess == current_guess:
        if len(result_words) > 1:
            new_guess = next(next(iter(result_words)))
    #writing to the csv to make sure progress from this guess is saved
    with open("./word_ranks.csv", 'w') as file:
        for key, value in result_words.items():
            file.write(f"{key}: {value}\n")

    return new_guess

def filter_words(word_dict, guess, guess_array):
    #g = gray, r = green, y = yellow
    filtered_dict = {}
    #iterating over letters in the guess
    for i, letter in enumerate(guess):
        #if letter is gray
        if guess_array[i] == 'g':
            #keep all words that do not have the letter in it
            for key, value in word_dict.items():
                if letter not in key:
                    filtered_dict[key] = value
            #set new word dict as filtered dict and empty filtered dict
            word_dict = filtered_dict
            filtered_dict = {}
        #if letter is yellow
        elif guess_array[i] == 'y':
            #find all words with letter in them
            for key, value in word_dict.items():
                if letter in key:
                    filtered_dict[key] = value
            word_dict = filtered_dict.copy()
            #subtract out all words with letter in the same index
            for key, value in word_dict.items():
                if key[i] == letter:
                    filtered_dict.pop(key)
            word_dict = filtered_dict
            filtered_dict = {}
        #if letter is green
        elif guess_array[i] == 'r':
            #keep all words with letter in the same index
            for key, value in word_dict.items():
                if key[i] == letter:
                    filtered_dict[key] = value
            word_dict = filtered_dict
            filtered_dict = {}
    #return finalized list
    return word_dict

def rank_words(word_list):
    words = {}
    #generating weights of each letter
    letter_map = common_letter.common_letter()
    #iterating over each word and calculating rank
    for word in word_list:
        words[word] = word_rank(word, letter_map)
    #sorting by value to get greatest to least rank
    ranked_words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1], reverse=True)}
    return ranked_words

def word_rank(word, letter_map):
    rank = 0
    used_letters = []
    #iterating over word
    for letter in word:
        #weighting repeated letters less to keep from skewing towards many highly ranked letters
        if letter in used_letters:
            rank += letter_map[letter] / 2
        else:
            rank += letter_map[letter]
        used_letters.append(letter)
    return rank
