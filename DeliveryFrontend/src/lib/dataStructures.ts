class Node<T> {
    private data : T;
    public nextNode : Node<T> | null;

    public constructor(data : T, nextNode : Node<T> | null) {
        this.data = data;
        this.nextNode = nextNode;
    }

    public getData() : T {
        return this.data;
    }

    public setData(data : T) {
        this.data = data;
    }
}

export class LinkedList<T> {
    private headNode : Node<T> | null;
    private lastNode : Node<T> | null;
    private compareTo : (a : T, b : T) => boolean;
    private addingCondition : (listElement : T, insertingElement : T) => number;
    private size : number = 0;

    public getSize() : number {
        return this.size;
    }

    public constructor(compareTo : (a : T, b : T) => boolean = (a : T, b : T) => a === b, addingCondition : (listElement : T, insertingElement : T) => number = (_ : T, __ : T) => 1) {
        this.headNode = null;
        this.lastNode = null;
        this.compareTo = compareTo;
        this.addingCondition = addingCondition;
    }

    public addData(data : T) : void {
        const newData : Node<T> = new Node<T>(data, null);

        if(this.headNode === null) {
            this.headNode = newData;
            this.lastNode = this.headNode;
        } else {
            //if head has greater distance or adding at first
            if(this.addingCondition(this.headNode.getData(), data) === 1) {
                newData.nextNode = this.headNode;
                this.headNode = newData;
            }
            //if lastNode's distance is lower than or equal to the added Node
            else if(this.addingCondition(this.lastNode!.getData(), data) === -1 || this.addingCondition(this.lastNode!.getData(), data) === 0) {
                newData.nextNode = this.lastNode!.nextNode;
                this.lastNode!.nextNode = newData;
            }
            //if and only if nextNode has higher distance than the added Node
            else {
                let temp : Node<T> = this.headNode!;
                while(temp.nextNode !== null) {
                    //nextNode is equal to the addedNode
                    if(this.addingCondition(temp.nextNode.getData(), data) === 0) {
                        newData.nextNode = temp.nextNode.nextNode;
                        temp.nextNode.nextNode = newData;
                        return;
                    }
                    //nextNode has greater distance than addedNode
                    else if(this.addingCondition(temp.nextNode.getData(), data) === 1) {
                        newData.nextNode = temp.nextNode;
                        temp.nextNode = newData;
                        return;
                    }

                    temp = temp.nextNode;
                }
            }
        }
        ++this.size;
    }

    public addDataAtLast(data : T) {
        const newData : Node<T> = new Node<T>(data, null);
        
        if(this.headNode === null) {
            this.headNode = newData;
            this.lastNode = this.headNode;
        } else {
            this.lastNode!.nextNode = newData;
            this.lastNode = this.lastNode!.nextNode;
        }

        ++this.size;
    }

    public deleteData(data : T) {
        if(this.headNode === null) return;
        
        if(this.compareTo(this.headNode.getData(), data)) {
            this.headNode = this.headNode.nextNode;

            if(this.headNode === null) {
                this.lastNode = null;
            }

            --this.size;
        } else {
            let temp : Node<T> = this.headNode!;
            while(temp.nextNode !== null && !this.compareTo(temp.nextNode.getData(), data)) temp = temp.nextNode;

            if(temp.nextNode !== null) {
                temp.nextNode = temp.nextNode.nextNode;
                --this.size;
            }

            if(temp.nextNode === null) {
                this.lastNode = temp;
            }
        }
    }

    public updateData(data : T) {
        if(this.headNode === null) return;

        let temp : Node<T> | null = this.headNode;

        while(temp !== null && !this.compareTo(temp.getData(), data)) temp = temp.nextNode;

        if(temp !== null) {
            temp.setData(data);
        }
    }

    public insertDataFromList(linkedList : LinkedList<T>, limit : number) {
        const data : T[] = linkedList.toList();

        data.forEach(item => {
            if(limit-- > 0) this.addData(item);
            linkedList.deleteData(item);
        });
    }

    public toList() : T[] {
        const ret : T[] = [];
        let temp : Node<T> | null = this.headNode;

        while(temp !== null) {
            ret.push(temp.getData());
            temp = temp.nextNode;
        }

        return ret;
    }

    public copy() : LinkedList<T> {
        const newList : LinkedList<T> = new LinkedList<T> (this.compareTo, this.addingCondition);
        let temp : Node<T> | null = this.headNode;
        while(temp !== null) {
            newList.addDataAtLast(temp.getData());
            temp = temp.nextNode;
        }
        return newList;
    }
}