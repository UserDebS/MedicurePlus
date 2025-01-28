import os
import base64 as bsf

def imageToBase64(imageName : str) -> str:
    imagePath = f'c:\\Users\\PC\\OneDrive\\Desktop\\MedicurePlus\\Backend\\medicines\\{imageName}.png'
    if os.path.exists(path=imagePath):
        with open(imagePath, 'rb') as image:
            return bsf.b64encode(image.read()).decode()
        
def imageToBase64URL(imageName : str) -> str:
    return f'data:image/png;base64,{imageToBase64(imageName=imageName)}'


if __name__ == '__main__':
    print(__file__)