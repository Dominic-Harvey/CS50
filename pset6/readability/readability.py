from cs50 import get_string

def main():
    text = get_string("Text: ")
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)
    index = 0.0588 * (letters/words*100) - 0.296 * (sentences/words*100) - 15.8
    grade = round(index)
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {grade}")

def count_letters(text):
    letters = 0
    for i in range(len(text)):
        if text[i].isalpha():
            letters = letters + 1
    return letters

def count_words(text):
    words = 1
    for i in range(len(text)):
        if text[i] == ' ':
            words = words + 1
    return words

def count_sentences(text):
    sentences = 0
    for i in range(len(text)):
        if text[i] == '.' or text[i] == '!' or text[i] == '?':
            sentences = sentences + 1
    return sentences

main()