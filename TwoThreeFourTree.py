from typing import Tuple, List
from typing import Optional


class KeyValuePair:
    def __init__(self, key, val):
        self.key = key
        self.val = val


class TwoThreeFourNode:
    def __init__(self):
        self.parent: Optional[TwoThreeFourNode] = None
        self.items: List[Optional[KeyValuePair]] = [None, None, None, None]
        self.children: List[Optional[TwoThreeFourNode]] = [None, None, None, None, None]
        self.numOfItems = 0
        self.numOfChildren = 0

    def appendItem(self, newItem):
        if self.numOfItems >= 3:
            raise ValueError("appendItem: items is full")
        self.items[self.numOfItems] = newItem
        self.numOfItems += 1

    def appendChild(self, child):
        if self.numOfChildren >= 4:
            raise ValueError("appendChild: children is full")
        if child is None:
            return
        self.children[self.numOfChildren] = child
        self.numOfChildren += 1
        child.parent = self

    def removeChild(self, childIndex):
        if self.numOfChildren == 0:
            return None
        if childIndex >= self.numOfChildren:
            return None

        if childIndex == -1:
            childIndex = self.numOfChildren - 1
        removedChild = self.children[childIndex]
        j = childIndex
        while j <= len(self.children) - 2:
            self.children[j] = self.children[j + 1]
            j += 1

        self.numOfChildren -= 1
        return removedChild

    def removeItem(self, itemIndex):
        if self.numOfItems == 0:
            return None
        if itemIndex >= self.numOfItems:
            raise ValueError("removeItem: invalid index")
        if itemIndex == -1:
            itemIndex = self.numOfItems - 1
        removedItem = self.items[itemIndex]
        j = itemIndex
        while j <= len(self.items) - 2:
            self.items[j] = self.items[j + 1]
            j += 1

        self.numOfItems -= 1
        return removedItem

    def insertChild(self, child, childIndex):
        if childIndex > self.numOfChildren:
            raise ValueError("insertChild: childIndex out of bounds")
        if child is None:
            return
        self.numOfChildren += 1
        i = len(self.children) - 1
        while i > childIndex:
            self.children[i] = self.children[i - 1]
            i -= 1
        self.children[childIndex] = child
        child.parent = self

    def getItem(self, i):
        if i >= self.numOfItems:
            raise ValueError("getItem: invalid index")
        return self.items[i]

    def getChild(self, i):
        return self.children[i]

    def getChildIndex(self, child) -> int:
        for i in range(0, self.numOfChildren):
            if self.children[i] is child:
                return i
        return -1

    def addItem(self, newItem) -> int:
        """
        Inserts newItem into its right spot in the items list

        :return: index of newItem in this node
        """
        if self.numOfItems >= 3:
            raise ValueError("addItemToItems: items is full")

        self.numOfItems += 1

        i = 0
        while (self.items[i] is not None) and newItem.key > self.items[i].key:
            i += 1
        if self.items[i] is None:
            self.items[i] = newItem
            return i

        j = len(self.items) - 1
        while j > i:
            self.items[j] = self.items[j - 1]
            j -= 1
        self.items[i] = newItem
        return i

    def findSubTree(self, key) -> int:
        """
        :return: The index of the child subtree where item belongs
        """
        i = 0
        while (self.items[i] is not None) and key > self.items[i].key:
            i += 1
        return i

    def needsToSplit(self) -> bool:
        return self.numOfItems == 3

    def isEmpty(self) -> bool:
        return self.numOfItems == 0

    def childHasSpareItems(self, childIndex) -> bool:
        if childIndex < 0 or childIndex >= self.numOfChildren:
            return False
        return self.children[childIndex].numOfItems > 1

    # def popRightmostChild(self) -> Optional['TwoThreeNode']:
    #     if self.numOfChildren == 0:
    #         return None
    #     rightmostChild = self.children[self.numOfChildren - 1]
    #     self.removeChild(self.numOfChildren-1)
    #     return rightmostChild

    def itemIndex(self, key) -> int:
        """
        :return: the index of the item with key in this node. If not present: returns -1
        """
        for i in range(0, self.numOfItems):
            if self.items[i].key == key:
                return i
        return -1

    def hasItem(self, key) -> bool:
        return self.itemIndex(key) != -1

    def isLeafNode(self) -> bool:
        return self.numOfChildren == 0


class TwoThreeFourTree:
    def __init__(self):
        self.root: Optional[TwoThreeFourNode] = None

    def isEmpty(self) -> bool:
        return self.root is None

    def insertItem(self, newItem: KeyValuePair) -> bool:
        if self.isEmpty():
            self.root = TwoThreeFourNode()
            self.root.appendItem(newItem)
            return True
        return self.insert(self.root, newItem)

    def insert(self, root: TwoThreeFourNode, newItem: KeyValuePair) -> bool:
        if root is None:
            return False
        if root.hasItem(newItem.key):
            return False

        root = self.split(root)
        if root.isLeafNode():
            root.addItem(newItem)
            return True
        return self.insert(root.children[root.findSubTree(newItem.key)], newItem)

    def split(self, toSplit: TwoThreeFourNode) -> Optional[TwoThreeFourNode]:
        if toSplit is None:
            return None
        if not toSplit.needsToSplit():
            return toSplit
        if toSplit is self.root:
            self.root = TwoThreeFourNode()
            self.root.appendChild(toSplit)

        newLeftChild = TwoThreeFourNode()
        newLeftChild.appendItem(toSplit.getItem(0))
        newLeftChild.appendChild(toSplit.getChild(0))
        newLeftChild.appendChild(toSplit.getChild(1))
        newRightChild = TwoThreeFourNode()
        newRightChild.appendItem(toSplit.getItem(2))
        newRightChild.appendChild(toSplit.getChild(2))
        newRightChild.appendChild(toSplit.getChild(3))
        index_of_promoted_item_in_parent = toSplit.parent.addItem(toSplit.getItem(1))
        toSplit.parent.removeChild(index_of_promoted_item_in_parent)
        toSplit.parent.insertChild(newLeftChild, index_of_promoted_item_in_parent)
        toSplit.parent.insertChild(newRightChild, index_of_promoted_item_in_parent + 1)
        return toSplit.parent

    def save(self):
        if self.root is None:
            return dict()
        return self.saveRecursive(self.root)

    def saveRecursive(self, root: Optional[TwoThreeFourNode]):
        treeDict = dict()
        treeDict['root'] = []
        for i in range(0, root.numOfItems):
            treeDict['root'].append(root.items[i].key)
        if root.isLeafNode():
            return treeDict
        treeDict['children'] = []
        for i in range(0, root.numOfChildren):
            treeDict['children'].append(self.saveRecursive(root.children[i]))
        return treeDict


if __name__ == "__main__":
    tree = TwoThreeFourTree()
    tree.insertItem(KeyValuePair(60, "Value of 4"))
    tree.insertItem(KeyValuePair(30, "value of 1"))
    tree.insertItem(KeyValuePair(10, "value of -10"))
    tree.insertItem(KeyValuePair(20, " val 100"))
    tree.insertItem(KeyValuePair(50, " val -20"))
    tree.insertItem(KeyValuePair(40, " val 35"))
    tree.insertItem(KeyValuePair(70, " val 36"))
    tree.insertItem(KeyValuePair(80, " val 37"))
    tree.insertItem(KeyValuePair(15, " val 38"))
    tree.insertItem(KeyValuePair(90, " val 38"))
    tree.insertItem(KeyValuePair(100, " val 38"))
    print(tree.save())
