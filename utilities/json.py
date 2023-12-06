def set_data_to_file(data, file_name):
    with open(file_name, 'w') as file:
        for key, value in data.items():
            file.write(f'{key}: {value}\n')


def get_data_from_file(file_name) -> dict:
    result_dict = {}
    with open(file_name, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')

            if value[0] == '(':
                value = value[1:-1]
                value = [int(num) for num in value.split(",")]
            else:
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass

            result_dict[key] = value

    return result_dict
