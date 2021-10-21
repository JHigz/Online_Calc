def add(Number_1, Number_2):
    result = Number_1 + Number_2
    return result

def sub(Number_1, Number_2):
    result = Number_1 - Number_2
    return result

def mult(Number_1, Number_2):
    result = Number_1 * Number_2
    return result

def div(Number_1, Number_2):
    result = Number_1 / Number_2
    return result


def process(Number_1, Number_2, Operation):
    if Operation == '+':
        return add(Number_1, Number_2)
    elif Operation == '-':
        return sub(Number_1, Number_2)
    elif Operation == '*':
        return mult(Number_1, Number_2)
    elif Operation == '/':
        return div(Number_1, Number_2)
    else:
        return "Operation isn't supported"
