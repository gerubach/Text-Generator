import random


def count_ngrams(string, n=1):
    """
    counts number of substrings with length n
    input: string called string, int length of substrings (n) with default value 1
    output: dictionary containing frequencies of each substring of s with length n
    """

    # create empty dictionary to be later populated with frequencies
    d = {}

    # loop through characters in string
    # stop at index len(string) - n because if the index is greater than
    # that, then the resulting substring will have length less than n
    for i in range(len(string) - n + 1):

        # get substring of length n that starts at position i
        temp = string[i:i + n]

        # if the substring already showed up once, add 1 to its value in d
        # otherwise, create a new key:value pair temp:1 in d
        if temp in d.keys():
            d[temp] += 1
        else:
            d[temp] = 1

    # after going through all possible substrings of length n, return d
    return d


def markov_text(string, n, length=100, seed="Emma Woodhouse"):
    """
    generates fake text of certain length based on sample text and given seed
    input: string of sample text (string), int order of model (n),
            int length of output (length) with default value 100, initial string (seed)
            with default value "Emma Woodhouse"
    output: generated fake text as a string
    """

    # count frequencies of each substring of s with length n+1
    # store results in n_plus_1_grams
    n_plus_1_grams = count_ngrams(string, n + 1)

    # set output string to seed
    output = seed

    # keep adding new characters using Markov model until output string reaches
    # specified length
    while len(output) < length:

        # get n+1-grams whose initial n characters are the same as the final n characters
        # of output. Store in list called options. Also get corresponding frequencies and
        # store in list called weights
        options = []
        weights = []
        for word, num in n_plus_1_grams.items():
            if word[:n] == output[-n:]:
                options.append(word)
                weights.append(num)

        # randomly make selection among entries in options, using entries of weights list
        # as corresponding weights. Take randomly chosen selection, and add its final
        # character to output
        output += random.choices(options, weights)[0][-1]

    # once output string has the correct length, return it
    return output


# open sample text and read to string
f = open("Emma.txt", "r", encoding="utf8")
s = f.read()

# clean sample text
s_cleaned = ""
j = 0
quote_counter = 0
roman_numerals = ["I", "V", "X"]
while j < len(s) - 1:
    # put spaces after periods
    if s[j] == "." and s[j + 1] != " " and s[j + 1] != '”':
        s_cleaned += ". "
        j += 1

    # put spaces after ending quotes
    elif s[j] == '”' and s[j + 1] != " ":
        s_cleaned += '" '
        j += 1

    # put spaces after commas
    elif s[j:j + 2] == "," and s[j + 1] != " ":
        s_cleaned += ", "
        j += 1

    # get rid of chapter labels
    elif s[j:j + 8] == "CHAPTER ":
        k = 8
        while s[j + k] in roman_numerals:
            k += 1
        j += k + 1
    else:
        s_cleaned += s[j]
        j += 1
s_cleaned += s[j]

# g = open("Emma_cleaned.txt", "w")
# g.write(s_cleaned)
l = input("Please enter number of characters you would like to generate (must be >14): ")
print(markov_text(s_cleaned, n=10, length=int(l), seed="Emma Woodhouse"))
f.close()
# g.close()
