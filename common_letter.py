import string

alpha = list(string.ascii_lowercase)
alpha_count = [0]*len(alpha)

file = open('wordle.txt',"r")
valid_words = (file.read()).lower()
file.close()

#counts each letter
for letter in range(len(alpha)):
    for word in valid_words:
        for pos in word:
            if alpha[letter] == pos:
                alpha_count[letter] += 1

alpha_sorted = []
alpha_count_sorted = []

#finds the biggest number, indexes it, removes that item and adds to sorted list
for i in range(len(alpha)):
    current_max = alpha_count.index(max(alpha_count))
    alpha_sorted.append(alpha.pop(current_max))
    alpha_count_sorted.append(alpha_count.pop(current_max))

print(alpha_sorted)
