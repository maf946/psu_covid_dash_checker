def print_updated_numbers(data_dictionary):
    label_width = len(max(data_dictionary, key=len))
    value_width = len(str(max(data_dictionary.values())))
    for k, v in data_dictionary.items():
        print('{label: <{width1}} {value: <{width1}}'.format(label=k, value=v, width1=label_width, width2=value_width))

