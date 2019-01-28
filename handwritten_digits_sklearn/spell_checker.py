import json
import sys
import os 
import pprint
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.casual import casual_tokenize
from spellchecker import SpellChecker
from termcolor import cprint

spell = SpellChecker()
tokenizer = RegexpTokenizer(r'\w+')

dict_fname = os.path.expandvars('$HOME/.spellchecker.txt')
with open(dict_fname, 'a'):
    os.utime(dict_fname, None)
spell.word_frequency.load_text_file(dict_fname)

learnt_words = []
ignored_words = []

def print_highlight(line, words):
    # import pdb; pdb.set_trace()
    for word in line.split():
        # if word in words:
        printed = False
        for msword in words:
            if msword in word.lower():
                cprint(word, 'blue', end=' ')
                printed = True
                break 
        if not printed:
            sys.stdout.write(word)
            sys.stdout.write(' ')
    sys.stdout.write('\n')
            
def handle_word(word):
    if word in ignored_words:
        return
    if len(word)>10:
        spell.distance = 1
    cprint('Word:', 'red', end=' ')
    cprint(word, 'blue')
    print('suggested :', spell.correction(word))
    candidates = spell.candidates(word)
    if len(candidates)>1:
        print('candidates:')
        for i, candidate in enumerate(candidates):
            print('[{}] : {}'.format(i, candidate))
    spell.distance = 2
    answer = None
    while answer not in list('ilcs'):
        answer = input('(i)gnore (l)earn, (c)hange, (s)top : ')
    if answer == 's':
        exit()
    elif answer == 'i':
        ignored_words.append(word)
        return
    elif answer == 'l':
        spell.word_frequency.load_words([word])
        learnt_words.append(word)
    elif answer == 'c':
        print('changing')
   
def check(cell):
    lines = cell['source']
    for line in lines:
        # using casual tokenize to get rid of urls and emojis
        words = casual_tokenize(line)
        words = [word for word in words if not word.startswith('http')]
        newline = ' '.join(words)
        # this handles e.g. contractions: you're, etc
        words = tokenizer.tokenize(newline)
        misspelled = spell.unknown(words)
        if len(misspelled):
            print_highlight(line, misspelled)
            for word in misspelled:
                handle_word(word)

def exit():
    # save dictionnary 
    answer = None
    while answer not in list('yn'):
        answer = input('Save dictionnary? [y/n]')
        if answer == 'y':
            with open(dict_fname, 'a') as dict_file:
                for word in learnt_words: 
                    dict_file.write(word + '\n')
    # save modified file
    answer = None
    while answer not in list('yn'):
        answer = input('Save file? [y/n]')
        if answer == 'y':
            print('saving file')
        elif answer == 'n':
            print('discarding changes')
    sys.exit(0)
    

                
with open(sys.argv[1]) as finput:
    notebook = json.load(finput)
    # pprint.pprint(notebook)

cells = notebook['cells']
cells_md = [cell for cell in cells if cell['cell_type'] == 'markdown']

for cell in cells:
    check(cell)

exit()
