# open instance/responses.txt and extract data

import json
import pandas as pd

def read_responses():
    responses = []
    with open('instance/responses.txt', 'r') as f:
        for line in f:
            responses.append(json.loads(line))
    return responses
  
data = read_responses()

pd.DataFrame(data)