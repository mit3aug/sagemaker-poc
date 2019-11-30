import json

data_partition_names = ['train', 'verify', 'test']
messages = {}
x = 1
for d in data_partition_names:

    messages[d] = "This is Test {}".format(x)
    x = x + 1


print(json.dumps(messages))


