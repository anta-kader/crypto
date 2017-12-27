import math

#Diviser un bloc en sous-blocs de 64 bits
def sub_bytes (b):
    res = [];
    while(len(b) > 64):
        res.append(b[:64])
        b = b[64:]
    res.append(b)
    return res

def modulo_2_64(x) :
    if len(x) > 64:
        x = x[-64:]
    elif len(x) < 64:
        x = x.zfill(64)
    return x

def binary_xor(x, y):
    x = int(x, 2)
    y = int(y, 2)
    return bin(x ^ y)[2:]

def binary_addition(x, y):
    x = int(x, 2)
    y = int(y, 2)
    return bin(x + y)[2:]

def binary_substraction(x, y):
    x = int(x, 2)
    y = int(y, 2)
    return bin(x - y)[2:]

#clés de la même taille que le texte
#diviser le bloc en mots de 64 bits
def add_nth_key (keys_array):
    c = "0001101111010001000110111101101010101001111111000001101000100010"
    kn = keys_array[0]
    size = len(keys_array)
    for i in range(1, size):
        kn = binary_xor(kn, keys_array[i])
    kn = binary_xor(kn, c).zfill(64)
    keys_array.append(kn)
    return True

#
def keys_generator (key, Nb):
    initial_keys_array = sub_bytes(key)
    res_key_arrays = []
    t0 = initial_keys_array[0]
    t1 = initial_keys_array[1]
    t2 = modulo_2_64(binary_xor(t0,t1))
    tweaks = [t0, t1, t2]
    #initial N+1 keys
    add_nth_key(initial_keys_array)
    #All the key rounds 76/4 + 1 = 20
    for i in range(0, 20):
        i_key_array = []
        for n in range(0, Nb):
            k = initial_keys_array[(i+n) % (Nb+1)]
            if n == Nb-3:
                k = modulo_2_64(binary_addition(k,tweaks[i % 3]))
            elif n == Nb-2:
                k = modulo_2_64(binary_addition(k,tweaks[(i+1) % 3]))
            else:
                k = modulo_2_64(bin(int(k, 2) + i)[2:])
            i_key_array.append(k)
        res_key_arrays.append(i_key_array)
    return res_key_arrays

def shift_left_method(bits, val):
    if(val > 64):
        val %= 64
    return bits[val:] + bits[:val]


def mix (words_array, R):
    size = len(words_array)
    for i in range(0, size, 2):
        m1, m2 = words_array[i], words_array[i + 1]
        res_m1 = modulo_2_64(binary_addition(m1, m2))
        res_m2 = modulo_2_64(binary_xor(res_m1, shift_left_method(m2, R)))
        words_array[i], words_array[i + 1] = res_m1, res_m2
        i += 1
    return words_array

def mix_reverse (words_array, R):
    size = len(words_array)
    for i in range(0, size, 2):
        res_m1, res_m2 = words_array[i], words_array[i + 1]
        m2 = shift_left_method(modulo_2_64(binary_xor(res_m2, res_m1)), R)
        #res_m2 étant le rés
        if(int(res_m1, 2) < int(m2, 2)):
            res_m1 = "1" + res_m1
        m1 = modulo_2_64(binary_substraction(res_m1, m2))
        words_array[i], words_array[i + 1] = m1, m2
        i += 1
    return words_array

#this method is autoreversible
def permute(words_array):
    size = len(words_array)
    for i in range(0, size):
        words_array[i] = shift_left_method(words_array[i], 32)
    words_array.reverse()
    return words_array


def threefish_cipher(plain_text, key, size):
    #Get the number of blocs {4, 8, 16}
    n = size // 64
    # Divise plain text bloc
    text_blocs = sub_bytes(plain_text)
    # Generate all the subkeys
    sub_keys_array = keys_generator(key, n)
    #Start the 76 rounds
    for i in range(0, 76):
        # get sub keys for this round and make the addition [64]
        if (i % 4 == 0 or i == 75):
            sub_keys = sub_keys_array[round(i / 4)]
            for id in range(0, n):
                text_blocs[id] = modulo_2_64(binary_addition(text_blocs[id], sub_keys[id]))
        # mix the words two by two R = 49
        text_blocs = mix(text_blocs, 49)
        # permute the words
        text_blocs = permute(text_blocs)
    joint = "";
    return joint.join(text_blocs)



def threefish_decipher(cipher_text, key, size):
    # Get the number of blocs {4, 8, 16}
    n = size // 64
    # Divise plain text bloc
    text_blocs = sub_bytes(cipher_text)
    # Generate all the subkeys
    sub_keys_array = keys_generator(key, n)
    for i in range(0, 76):
        # permute the words
        text_blocs = permute(text_blocs)
        # mix the words two by two R = 64 - 49 = 15
        text_blocs = mix_reverse(text_blocs, 15)
        # get sub keys for this round and make the addition [64]
        if (i== 0 or i % 4 == 3 or i == 75):
            j = round(i / 4) + 1
            sub_keys = sub_keys_array[-j]
            for id in range(0, n):
                text_bloc = text_blocs[id]
                sub_key = sub_keys[id]
                if (int(text_bloc, 2) < int(sub_key, 2)):
                    text_bloc = "1" + text_bloc
                text_blocs[id] = modulo_2_64(binary_substraction(text_bloc, sub_key))

    joint = "";
    return joint.join(text_blocs)


plain_text = "0001101111010001000110111101100011011110100010001101111011010101010011111110000011010001000100101010100111111100000110100010001000011011110100010001101111010001101111010001000110111101101010101001111111000001101000100010101010101001111111000001101000100010"
key = "1101010011111110110111110111101101010101001110010001101110010001101100011011110100010000101010101101010010101011110000011010001000101111010100111110000110101010011111110000011010001000100001101111010001000110000011010001000100001101111010001000110111101000"


print(plain_text)
cipher_text = threefish_cipher(plain_text, key, 256)
print(cipher_text)
print(threefish_decipher(cipher_text, key, 256))

