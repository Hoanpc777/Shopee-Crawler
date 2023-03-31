import pandas as pd
import re

# Get data from dict value
def flat_dict(data):
    df = pd.DataFrame(data)
    unnest = df.explode('categories')
    list_cate = [i['display_name'] for i in unnest['categories']]
    cate_df = pd.concat([data,pd.DataFrame(list_cate).T], axis=1)
    return cate_df

def remove_char_in_Square_brackets(text):
  result = re.sub(r'\[[^]]*\]', '', text).strip()
  return result