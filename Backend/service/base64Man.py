def base64padding(b64 : str) -> str:
    missing = len(b64) % 4
    b64 += ('=' * (4 - missing))
    return b64

def getImageType(data : str):
    return data.split(';')[0].split('/')[-1]

def base64imageSplit(data : str):
    return data.split(',')[-1]

if __name__ == '__main__':
    print(getImageType('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII'))