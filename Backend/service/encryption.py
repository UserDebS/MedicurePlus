from random import randint

def encryption(data : str) -> str:
    xorlist = [5, 8, 3, 2]
    result = ""
    for i in range(len(data)):
        result += chr(((ord(data[i]) ^ xorlist[i % 4]) % 123) + 65)
    return result


def strGen(length : int) -> str:
    result : str = ''
    alphalist = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(length):
        result += alphalist[randint(0, len(alphalist) - 1)]
    return result