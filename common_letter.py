import string

def common_letter():
    alpha = list(string.ascii_lowercase)
    #creating a map of all letters in the alphabet and initializing totals to 0
    alpha_map = {}
    for letter in alpha:
        alpha_map[letter] = 0
    #reading file in
    file = open('wordle.txt',"r")
    valid_words = (file.read()).lower()
    file.close()
    total = 0
    #counts each letter
    try:
        for word in valid_words:
            for pos in word:
                if pos != "\n":
                    alpha_map[pos] += 1
                    total += 1
    except(...):
        print("Something wrong with the mapping")
    #sorting map from greatest to least
    alpha_sorted = {k: v for k, v in sorted(alpha_map.items(), key=lambda item: item[1], reverse=True)}
    #making the value into a percentage of total letters, weighting vowels as more
    for key in alpha_sorted:
        alpha_sorted[key] /= total
        alpha_sorted[key] *= 100
    #alpha_count_sorted = []

    #finds the biggest number, indexes it, removes that item and adds to sorted list
    # for i in range(len(alpha)):
    #     current_max = alpha_count.index(max(alpha_count))
    #     alpha_sorted.append(alpha.pop(current_max))
    #     alpha_count_sorted.append(alpha_count.pop(current_max))

    
    return alpha_sorted
