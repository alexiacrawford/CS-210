'''
jumbler:  List dictionary words that match an anagram.
2022-06-25 by Alexia Crawford
Credits: Sam Spurlock - worked on code together
'''

#DICT = "shortdict.txt"    # Short version for testing & debugging
DICT = "dict.txt"       # Full dictionary word list
dict_file = open(DICT, "r")

def normalize(word: str) -> list[str]:
    '''
    returns word in an alphabetically sorted list and all lowercase
    >>> normalize("MAGMA")
    ['a', 'a', 'g', 'm', 'm']
    >>> normalize("norac")
    ['a', 'c', 'n', 'o', 'r']
    '''
    word = word.lower()
    sorted_word = sorted(word)
    return sorted_word

def find(anagram: str):
    '''
    calls normalize to find word in DICT and prints it
    >>> find("Alpha")
    alpha
    >>> find("jfkajsk")
    
    >>> find("norac")
    acorn
    '''
    dict_file = open(DICT, "r") 
    for line in dict_file:
        word = line.strip()
        if normalize(word) == normalize(anagram):
            print(word)
        
def main():
    '''
    inputs inststructions to enter an anagram and unscrambles the anagram and prints
    final result
    '''
    anagram = input("Anagram to find> ")
    find(anagram)
    return
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Doctests complete!")
    
main()
