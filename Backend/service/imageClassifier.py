import base64 as bsf
import numpy as np
from service.base64Man import base64imageSplit, base64padding
import easyocr as eo
import cv2
from .trie import Trie

class ImageClassifier:
    def __init__(self, trie : Trie) -> None:
        self.__reader = eo.Reader(['en'])
        self.__trie = trie
    
    def read(self, imagestr : str) -> list[str]:
        img = np.frombuffer(bsf.b64decode(base64padding(base64imageSplit(imagestr))), dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
        self.matches = self.__reader.readtext(image=img)    
        return self.__findSimilarity()

    def __findSimilarity(self) -> list[str]:
        output_similarities : list[str] = []
        for match in self.matches:
            if(match[1] != '' or match[1] == ' '):
                for m in match[1].split(' '):
                    output_similarities.extend(self.__trie.showSimilarities(m))
        return output_similarities
    