#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import regex as re
import pandas as pd
import spacy
from pathlib import Path
from collections import Counter


# In[2]:


# Read in the text file and make sure it's encoded in UTF-8. 
# Please change it to your respective file path.

text = open("corpus/Potter_Rabbit_anno_20.01.xml", mode='r', encoding='utf-8-sig').read()
#text[:100]


# In[3]:


# Regular expression pattern to match <sound>...</sound>
pattern = r'(<sound>[A-Za-z]+</sound>)'

# Find all matches in the text
sound_words = re.findall(pattern, text)

# Print the list of matches
#print(sound_words)


# In[4]:


pattern = r'(?s)\<\?xml version="1.0" encoding="UTF-8"\?>.*?<body>'
pattern2 = r'(?s)\</body>.*?</TEI>'

# Use re.sub to remove the matched portion from the text
text_without_match = re.sub(pattern, '', text)
text_without_match = re.sub(pattern2, '', text_without_match)

#print(text_without_match)


# In[5]:


text_without_match = re.sub('\n+', ' ', text_without_match)
text_without_match = re.sub('\s+', ' ', text_without_match)
text_without_match


# In[6]:


import spacy
from spacy.util import compile_infix_regex

# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Sample text
input_text = text_without_match

# Define custom infix patterns to preserve "<sound>...</sound>" as one token
infixes = [
    r"(?<=\</sound>)(?=[\s\.,;:!?])",  # Split after '</sound>' followed by punctuation or space
    r"(?<=\s|[\<\>\.,;:!?])(?=\<sound\>)",  # Split before '<sound>' followed by punctuation or space
]

# Compile infix regex patterns
infix_re = compile_infix_regex(infixes)

# Set the custom infix regex as the tokenizer's infix pattern finder
nlp.tokenizer.infix_finditer = infix_re.finditer

# Tokenize the input text
doc = nlp(input_text)

# Get the tokens
tokens = [token.text for token in doc]

# Print the tokens
#print(tokens)


# In[7]:


df = pd.DataFrame(tokens, columns=['tokens'])
#df


# In[8]:


#filtered_df['sound_annotation'] = filtered_df['tokens'].str.match(r'sound>(.*?)</sound')
df['sound_annotation'] = df['tokens'].str.extract(r'(sound>((.)*)</sound)')[1]


# In[9]:


length = len(tokens)
#print(length)
list = ['O']* length 
#len(list)


# In[10]:


# Show and controll the data frame before saving it to a csv-file.
df['annotation'] = list
#df.head(n = 10)


# In[11]:


# Iterate over the "tokens" column and update the "annotation" column
for index, row in df.iterrows():
    token_text = row["tokens"]
    if re.search(r'sound>(.*?)</sound', token_text):
        df.at[index, "annotation"] = "sound"


# In[12]:


# Iterate over the DataFrame and update the "tokens" column
for index, row in df.iterrows():
    token_text = row["tokens"]
    sound_annotation = row["sound_annotation"]
    match = re.search(r'sound>(.*?)</sound', token_text)
    if match:
        df.at[index, "tokens"] = sound_annotation


# In[13]:


# Drop rows with empty cells in the "tokens" column
df = df[df["tokens"].str.strip() != ""]
df = df[~df["tokens"].str.contains("<|>")]

# Reset the index to have continuous row numbers
df.reset_index(drop=True, inplace=True)


# In[14]:


del df['sound_annotation']


# In[15]:


#df


# In[16]:


# Save the DataFrame to a CSV file
df.to_csv("611Potter1902_anno.csv", index=False)


# In[ ]:





# In[ ]:




