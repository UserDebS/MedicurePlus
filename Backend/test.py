import base64 as bsf
import numpy as np
from service.base64Man import base64imageSplit, base64padding
import easyocr as eo
import cv2
from .service.trie import Trie

class ImageClassifier:
    def __init__(self) -> None:
        self.__reader = eo.Reader(['en'])
    
    def read(self, imagestr : str):
        img = np.frombuffer(bsf.b64decode(base64padding(base64imageSplit(imagestr))), dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
        self.matches = self.__reader.readtext(image=img)    
        return self.__findSimilarity()

    def __findSimilarity(self, trie : Trie) -> list[str]:
        output_similarities : list[str] = []
        for match in self.matches:
            if(match[1] != ''):
                output_similarities.extend(trie.showSimilarities(match[1]))
        return output_similarities
    