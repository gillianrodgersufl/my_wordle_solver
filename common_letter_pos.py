import string

alpha = list(string.ascii_lowercase)


file = open('wordle.txt',"r")
valid_words = (file.read()).lower()
valid_words = valid_words.split('\n')
file.close()

alpha_count_list = []

#counts each letter

for position in range(5):
    alpha_count = [0]*len(alpha)
    alpha_count_list.append(alpha_count)
    for letter in range(len(alpha)):
        for word in valid_words:
            if alpha[letter] == word[position]:
                alpha_count[letter] += 1

        

def sorted_alpha_counts(alpha_count,alpha):
    alpha_sorted = []
    alpha_count_sorted = []

    #finds the biggest number, indexes it, removes that item and adds to sorted list
    for i in range(len(alpha)):
        current_max = alpha_count.index(max(alpha_count))
        alpha_sorted.append(alpha.pop(current_max))
        alpha_count_sorted.append(alpha_count.pop(current_max))

    print(alpha_sorted)
    print(alpha_count_sorted)

for i in range(len(alpha_count_list)):
    alpha = list(string.ascii_lowercase)
    sorted_alpha_counts(alpha_count_list[i],alpha)