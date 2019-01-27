import json
import sys
import pprint
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.casual import casual_tokenize
from spellchecker import SpellChecker

spell = SpellChecker()
tokenizer = RegexpTokenizer(r'\w+')

known = [
    'google', 'youtube', 
    '3d', '1d', '2d', 'scipy', 'numpy',
    'scikit', 'jupyter', 'matplotlib', 'pyplot', 'linspace', 'downloads'
    'linux', 'plt', 'github', 'plot_multi', 'linux'
    'website'
    ]

def check(cell):
    lines = cell['source']
    for line in lines:
        # using casual tokenize to get rid of urls and emojis
        words = casual_tokenize(line)
        words = [word for word in words if not word.startswith('http')]
        newline = ' '.join(words)
        newwords = tokenizer.tokenize(newline)
        newwords = [word for word in newwords if word.lower() not in known]
        misspelled = spell.unknown(newwords)
        if len(misspelled):
            print(line)
            pprint.pprint(words)
            pprint.pprint(newwords)
            pprint.pprint(misspelled)
            import pdb; pdb.set_trace()
            
with open(sys.argv[1]) as finput:
    notebook = json.load(finput)
    # pprint.pprint(notebook)

cells = notebook['cells']
cells_md = [cell for cell in cells if cell['cell_type'] == 'markdown']

# pprint.pprint(cells)

for cell in cells:
    check(cell)
