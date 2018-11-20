def csv_converter(function_output):
    converted_list = []
    for x in function_output:
        new_dict = {}
        new_dict['x'] = x[0]
        new_dict['y'] = x[1]
        converted_list.append(new_dict)
    toCSV = converted_list
    keys = toCSV[0].keys()
    with open('people.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)
