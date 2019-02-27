import json
import pandas as pd
import matplotlib.pyplot as plt

# open input file: 
ifile = open('review.json') 

# read the first 100k entries
# set to -1 to process everything
stop = -1

all_data = list()
for i, line in enumerate(ifile):
    if i%10000==0:
        print(i)
    if i==stop:
        break    
    # convert the json on this line to a dict
    data = json.loads(line)
    # extract what we want
    text = data['text']
    stars = data['stars']
    # add to the data collected so far
    all_data.append([stars, text])
# create the DataFrame
df = pd.DataFrame(all_data, columns=['stars','text'])
print(df)
# df.to_hdf('revie20ws.h5','reviews')

ifile.close()

