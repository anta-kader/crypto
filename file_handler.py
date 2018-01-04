import tkinter
from tkinter import filedialog


def get_plain_data():
    root = tkinter.Tk()
    root.withdraw()
    #get file path
    file_path = filedialog.askopenfilename()
    #open file and read the bytes
    file = open(file_path, "rb")
    byte = file.read()
    array = bytearray(byte)
    file.close()
    #convert bytes to binary values and return them
    return ''.join('{0:08b}'.format(x, 'b') for x in array)

def fill_in(data, desired_size):
    data_size = len(data)
    filler = "00000000"
    last = bin(data_size)[2:]
    if data_size < desired_size :
        diff = (desired_size - data_size) // 8
        for i in range(0, diff) :
            if i == (diff - 1) :
                data += last
            else :
                data += filler
    return data


def open_file(desired_size):
    data = get_plain_data()
    full_data = fill_in(data, desired_size)
    return full_data


def binary_to_bytes(binary_string):
    n = 8
    size = len(binary_string)
    return [binary_string[i:i+n] for i in range(0, size, n)]


def bytes_to_int(bytes_array):
    result = []
    size = len(bytes_array)
    for i in range(0, size):
        result.append(int(bytes_array[i], 2))
    return result


def remove_fillers(data, desired_size):
    bytes_array = binary_to_bytes(data)
    filler = "00000000"
    size = len(bytes_array)
    if filler in bytes_array:
        diff = (desired_size - int(bytes_array[size-1], 2)) // 8
        del bytes_array[-diff:]
    return bytes_array


def write_file(file_name, bytes_array):
    bytearray_data =  bytearray(bytes_to_int(bytes_array))
    #write data on file
    f = open(file_name, "w")
    f.write(bytearray_data.decode())
    f.close()
    return True

def save_data_in_file(file_name, data, size, remove_fillers):
    bytes_array = []
    if(remove_fillers):
        bytes_array = remove_fillers(data, size)
    else:
        bytes_array = binary_to_bytes(data)
    return write_file(file_name, bytes_array)


data = open_file(256)
print(data)
data_minus_fillers = remove_fillers(data, 256)
print(data_minus_fillers)
write_file("trying", data_minus_fillers)