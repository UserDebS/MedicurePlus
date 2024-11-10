class Trie:
    class Node:
        def __init__(self, end : bool = False) -> None:
            self.end = end
            self.children = [None for i in range(38)]
            
    def __init__(self) -> None:
        self.node = self.Node()
        self.__similarityList = []
    
    def encrypt(self, ch : chr) -> int:
        if(ch >= 'a' and ch <= 'z'):
            return ord(ch) - ord('a')
        elif(ch >= '0' and ch <= '9'):
            return ord(ch) - ord('0') + 26
        elif(ch == ' '):
            return 36
        elif(ch == '-'):
            return 37
    
    def decrypt(self, ind : int) -> chr:
        if(ind >= 0 and ind <= 25):
            return chr(ind + ord('a'))
        elif(ind >= 26 and ind <= 65):
            return chr(ind - 26 + ord('0'))
        elif(ind == 36):
            return ' '
        elif(ind == 37):
            return '-'

    def add(self, item : str):
        item = item.lower()
        cur = self.node
        for index, letter in enumerate(item):
            if(cur.children[(self.encrypt(letter))] != None):
                cur = cur.children[self.encrypt(letter)]
            else:
                cur.children[self.encrypt(letter)] = self.Node(end = (index == len(item) - 1))
                cur = cur.children[self.encrypt(letter)]

    def showSimilarities(self, item : str):
        print(item)
        item = item.lower()
        self.__similarityList.clear()
        cur = self.node
        for letter in item:
            if(self.encrypt(letter) is None):
                return []
            if(cur.children[(self.encrypt(letter))] != None):
                cur = cur.children[self.encrypt(letter)]
            else:
                return []
        
        self.__recursiveSearch(cur=cur, prev=item)
        return self.__similarityList

    def __recursiveSearch(self, cur : Node, prev : str = ''):
        if(cur.end):
            self.__similarityList.append(prev)
        for index, node in enumerate(cur.children):
            if(node is not None):
                self.__recursiveSearch(node, (prev + self.decrypt(index)))

    def addClass(self, classInput : str | list[str]):
        if(isinstance(classInput, str)):
            self.add(classInput)
            return
        for cls in classInput:
            self.add(cls)


if __name__ == '__main__':
    trie = Trie()
    trie.addClass(['hello', 'how', 'hehe'])
    print(trie.showSimilarities('hp'))