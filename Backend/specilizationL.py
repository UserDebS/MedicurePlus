# import pickle as pkl


specializations = [
    'cardiologist',
    'dermatologist',
    'neurologist',
    'orthopedic surgeon',
    'pediatrician',
    'psychiatrist',
    'radiologist',
    'gastroenterologist',
    'endocrinologist',
    'oncologist',
    'urologist',
    'nephrologist',
    'ophthalmologist',
    'rheumatologist',
    'allergist',
    'anesthesiologist',
    'pulmonologist',
    'gynecologist',
    'otolaryngologist',
    'plastic surgeon',
    'hematologist',
    'immunologist',
    'infectious disease specialist',
    'neurosurgeon',
    'obstetrician',
    'pathologist',
    'podiatrist',
    'emergency medicine specialist',
    'sports medicine specialist',
    'geriatrician',
    'family medicine physician',
    'general surgeon',
    'vascular surgeon',
    'thoracic surgeon',
    'hepatologist',
    'intensivist',
    'occupational medicine specialist',
    'pain management specialist',
    'rehabilitation medicine specialist',
    'sleep medicine specialist'
]

class Node:
    def __init__(self, val : str) -> None:
        self.val = val
        self.children : list[Node] = [None for i in range(27)]
    
class SpecializationTrie:
    def __init__(self) -> None:
        self.__root : Node = Node('')
        self.__suggestion : list[str] = []
    
    def insert(self, val : str, addon : str = ''):
        curr = self.__root
        for i in val:
            if(i == ' '):
                if(curr.children[-1] == None):
                    curr.children[-1] = Node(addon + i)
                    addon += i
                    curr = curr.children[-1]
                else:
                    addon += i
                    curr = curr.children[-1]
            
            else:
                if(curr.children[ord(i) - 97] == None):
                    curr.children[ord(i) - 97] = Node(addon + i)
                    addon += i
                    curr = curr.children[ord(i) - 97]
                
                else: 
                    addon += i
                    curr = curr.children[ord(i) - 97]

    def search(self, val : str) -> list[str]:
        self.__suggestion.clear()
        curr = self.__root
        for i in val:
            if(i == ' '):
                curr = curr.children[-1]
            else:
                curr = curr.children[ord(i) - 97]
            
            if(curr == None):
                break

        self.__traversal(curr)
        return self.__suggestion

    def all(self):
        self.__suggestion.clear()
        self.__traversal(self.__root)
        print(self.__suggestion)
        self.__suggestion.clear()

    def __traversal(self, curr : Node):
        if(curr == None):
            return
        if(curr.children.count(None) == 27):
            self.__suggestion.append(curr.val)
        for i in curr.children:
            self.__traversal(i)
        

tree = SpecializationTrie()
for i in specializations:
    tree.insert(i)

# with open('specilizations.pkl', 'wb') as file:
#     pkl.dump(tree, file=file)