from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file,read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    # remove duplicates from the dictionary
    dictionary_set = set(dictionary)

    deciphered_text : str
    min_number_of_words : int
    shift : int

    for i in range(26):
        shifted_text = ''.join(chr((ord(char) - 97 - i) % 26 + 97) if char != ' ' else ' ' for char in ciphered)
        number_of_words = sum([1 for word in shifted_text.split() if word not in dictionary_set])
        
        if i == 0:
            deciphered_text = shifted_text
            min_number_of_words = number_of_words
        else:
            if number_of_words < min_number_of_words:
                min_number_of_words = number_of_words
                deciphered_text = shifted_text
                shift = i
        if min_number_of_words == 0:
            break

    DechiperResult = (deciphered_text, shift, min_number_of_words)
    return DechiperResult
