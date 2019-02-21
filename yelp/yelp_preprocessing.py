import json
import pandas as pd

# open input file: 
fname = 'review.json'
ifile = open(fname) 

# read the first 100k entries
# set to -1 to process everything
stop = -1

all_data = list()
for i, line in enumerate(ifile):
    # convert the json on this line to a dict
    data = json.loads(line)
    # extract what we want
    text = data['text']
    stars = data['stars']
    # add to the data collected so far
    all_data.append([stars, text])
    if i%10000==0:
        print(i)
    if i==stop:
        break
# create the DataFrame
df = pd.DataFrame(all_data, columns=['stars','text'])
print(df)

ifile.close()

