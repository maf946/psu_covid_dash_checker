def print_updated_numbers(dataDictionary):
    labelWidth = len(max(dataDictionary, key=len))
    valueWidth = len(str(max(dataDictionary.values())))
    for k, v in dataDictionary.items():
        print('{label: <{width1}} {value: <{width1}}'.format(label=k, value=v, width1=labelWidth, width2=valueWidth))
