from typing import Tuple
from typing import Optional


class KeyValuePair:
    def __init__(self, key, val):
        self.key = key
        self.val = val


class TwoThreeNode:
    def __init__(self):
        self.parent = None
        self.items = [None, None, None]
        self.children = [None, None, None, None]
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
            childIndex = self.numOfChildren-1
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
            itemIndex = self.numOfItems-1
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
        for i in range(0, self.numOfItems):
            if self.items[i].key == key:
                return i
        return -1

    def isLeafNode(self) -> bool:
        return self.numOfChildren == 0


class TwoThreeTree:
    def __init__(self):
        self.root = None

    def isEmpty(self):
        return self.root is None

    def insertItem(self, newItem) -> bool:
        if self.root is None:
            self.root = TwoThreeNode()
            self.root.appendItem(newItem)
            return True
        return self.insert(self.root, newItem)

    def insert(self, root, newItem) -> bool:
        if root.itemIndex(newItem.key) != -1:
            return False
        if root.isLeafNode():
            root.addItem(newItem)
            self.split(root)
            return True
        return self.insert(root.children[root.findSubTree(newItem.key)], newItem)

    def split(self, toSplit: TwoThreeNode):
        if toSplit is None:
            return
        if not toSplit.needsToSplit():
            return
        if toSplit is self.root:
            self.root = TwoThreeNode()
            self.root.appendChild(toSplit)

        newLeftChild = TwoThreeNode()
        newLeftChild.appendItem(toSplit.getItem(0))
        newLeftChild.appendChild(toSplit.getChild(0))
        newLeftChild.appendChild(toSplit.getChild(1))
        newRightChild = TwoThreeNode()
        newRightChild.appendItem(toSplit.getItem(2))
        newRightChild.appendChild(toSplit.getChild(2))
        newRightChild.appendChild(toSplit.getChild(3))
        index_of_promoted_item_in_parent = toSplit.parent.addItem(toSplit.getItem(1))
        toSplit.parent.removeChild(index_of_promoted_item_in_parent)
        toSplit.parent.insertChild(newLeftChild, index_of_promoted_item_in_parent)
        toSplit.parent.insertChild(newRightChild, index_of_promoted_item_in_parent + 1)
        self.split(toSplit.parent)

    def deleteItem(self, searchKey) -> bool:
        return self.delete(searchKey, self.root)

    def delete(self, searchKey, root: Optional[TwoThreeNode]) -> bool:
        if root is None:
            return False

        itemIndex = root.itemIndex(searchKey)
        if itemIndex != -1:
            if root.isLeafNode():
                root.removeItem(itemIndex)
                self.fix(root)
                return True
            # swap met inorder successor
            inorderSuccessorNode = self.getInorderSuccessor(root, itemIndex)
            inorderSuccessorItem = inorderSuccessorNode.removeItem(0)
            root.items[itemIndex] = inorderSuccessorItem
            self.fix(inorderSuccessorNode)
            return True
        return self.delete(searchKey, root.children[root.findSubTree(searchKey)])

    def fix(self, toFix: TwoThreeNode):
        if not toFix.isEmpty():
            return

        if toFix is self.root:
            self.root = toFix.removeChild(0)
            if self.root is not None:
                self.root.parent = None
            return

        toFixChildIndex = toFix.parent.getChildIndex(toFix)

        # Does toFix have a left sibling with spare items?
        if toFix.parent.childHasSpareItems(toFixChildIndex-1):
            donorNode = toFix.parent.children[toFixChildIndex-1]
            toFix.addItem(toFix.parent.removeItem(toFixChildIndex-1))
            toFix.insertChild(donorNode.removeChild(-1), 0)
            toFix.parent.addItem(donorNode.removeItem(-1))
            return
        if toFix.parent.childHasSpareItems(toFixChildIndex+1):
            donorNode = toFix.parent.children[toFixChildIndex+1]
            toFix.addItem(toFix.parent.removeItem(toFixChildIndex))
            toFix.appendChild(donorNode.removeChild(0))
            toFix.parent.addItem(donorNode.removeItem(0))
            return

        # Redistribution is not possible => merge
        # Merge to right sibling
        if toFixChildIndex == 0:
            mergeSibling = toFix.parent.children[1]
            mergeSibling.addItem(toFix.parent.removeItem(0))
            mergeSibling.insertChild(toFix.children[0], 0)
            toFix.parent.removeChild(0)
            self.fix(toFix.parent)
            return

        # Merge to left sibling
        mergeSibling = toFix.parent.children[toFixChildIndex-1]
        mergeSibling.addItem(toFix.parent.removeItem(toFixChildIndex-1))
        mergeSibling.appendChild(toFix.children[0])
        toFix.parent.removeChild(toFixChildIndex)
        self.fix(toFix.parent)
        return

    def getInorderSuccessor(self, root, itemIndex) -> TwoThreeNode:
        """
        pre: root is not a leaf node.
        pre: itemIndex is a valid index

        :return: the inorder successor node, the inorder successor is the zeroth item
        """
        if root.isLeafNode():
            raise ValueError("getInorderSuccessor: root is a leaf node you dummy!")
        if itemIndex >= root.numOfItems:
            raise ValueError("getInroderSuccessor: itemIndex is out of bounds you dummy!")

        cur = root.children[itemIndex+1]
        while not cur.isLeafNode():
            cur = cur.children[0]
        return cur


    def retrieveItem(self, searchKey) -> Tuple[Optional[KeyValuePair], bool]:
        return self.retrieveItemRecursive(searchKey, self.root)

    def retrieveItemRecursive(self, searchKey, root: Optional[TwoThreeNode]) -> Tuple[Optional[KeyValuePair], bool]:
        if root is None:
            return None, False

        itemIndex = root.itemIndex(searchKey)
        if itemIndex != -1:
            return root.items[itemIndex], True
        return self.retrieveItemRecursive(searchKey, root.children[root.findSubTree(searchKey)])

    def inorderTraverse(self, visit):
        self.inorderTraverseRecursive(self.root, visit)

    def inorderTraverseRecursive(self, root, visit):
        if root is None:
            return
        for i in range(0, root.numOfItems):
            self.inorderTraverseRecursive(root.children[i], visit)
            visit(root.items[i].key)
        self.inorderTraverseRecursive(root.children[root.numOfItems], visit)

    def save(self):
        if self.root is None:
            return dict()
        return self.saveRecursive(self.root)

    def saveRecursive(self, root: Optional[TwoThreeNode]):
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
    twothreetree = TwoThreeTree()
    twothreetree.insertItem(KeyValuePair(4, "Value of 4"))
    twothreetree.insertItem(KeyValuePair(1, "value of 1"))
    twothreetree.insertItem(KeyValuePair(-10, "value of -10"))
    twothreetree.insertItem(KeyValuePair(100, " val 100"))
    twothreetree.insertItem(KeyValuePair(-20, " val -20"))
    twothreetree.insertItem(KeyValuePair(35, " val 35"))
    twothreetree.insertItem(KeyValuePair(36, " val 36"))
    twothreetree.insertItem(KeyValuePair(37, " val 37"))
    twothreetree.insertItem(KeyValuePair(38, " val 38"))
    twothreetree.inorderTraverse(print)
    print(twothreetree.save())
    print("#########################################")
    print(twothreetree.retrieveItem(10)[1])
    print("#########################################")
    twothreetree.deleteItem(37)
    twothreetree.deleteItem(38)
    print(twothreetree.save())
    twothreetree.deleteItem(4)
    print(twothreetree.save())
    twothreetree.deleteItem(1)
    print(twothreetree.save())
    twothreetree.deleteItem(35)
    print(twothreetree.save())
    twothreetree.deleteItem(-20)
    print(twothreetree.save())
    twothreetree.deleteItem(100)
    print(twothreetree.save())
    twothreetree.deleteItem(-10)
    print(twothreetree.save())
    twothreetree.deleteItem(36)
    print(twothreetree.save())

