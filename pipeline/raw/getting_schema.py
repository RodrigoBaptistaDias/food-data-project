import json

with open('data/food_data_dublin.json', 'r', encoding='utf-8') as f:
    json_dump = json.load(f)

data_value = json_dump['returnvalue']['data']
first_data_value = data_value[0]['featuredReviews']

#for k,v in first_data_value.items():
#    print(f'{k}:{type(v)}')

print (first_data_value)
#for k in first_data_value:
#    print(f' {k}:{type(k)}')  