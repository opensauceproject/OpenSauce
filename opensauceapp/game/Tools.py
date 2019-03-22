import unidecode
import string
import difflib

def sanitize(s, ignored_prefix):
        # any special char unicode char to the closest ascci char
        s = unidecode.unidecode(s)
        # remove punctuation and remove whitespaces
        s = s.translate(str.maketrans('', '', string.punctuation))
        # only lower cases
        s = s.lower()
        # remove special char sequence
        for sequence in ignored_prefix:
            l = len(sequence)
            word_prefix = s[:l]
            if word_prefix == sequence:
                s = s[l:]
                break
        s = s.translate(str.maketrans('', '', string.whitespace))
        return s

def str_delta(str1, str2):
    ndiff = list(difflib.ndiff(str1, str2))
    diffs = list(filter(lambda a: a[0] != ' ',  ndiff))
    return len(diffs)
