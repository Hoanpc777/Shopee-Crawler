import json
import pandas as pd
import requests
import re

# Get data from dict value
def flat_dict(data, columns):
    raw = pd.json_normalize(data[0])[[columns]].set_index([pd.Index(['lv1','lv2','lv3'])]).T.reset_index().drop('index',axis=1)
    return raw

def remove_char_in_Square_brackets(text):
  result = re.sub(r'\[[^]]*\]', '', text).strip()
  return result