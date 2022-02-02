from typing import Tuple
from typing import Optional
import typing


class KeyValuePair:
    def __init__(self, key, val):
        self.key = key
        self.val = val


class BinarySearchTreeNode:
    def __init__(self, keyval):
        self.keyval = keyval
        self.left = None
        self.right = None

    def hasAsLeftChild(self, maybeLeftChild):
        """
        Returns True if maybeLeftChild is the left child of this node
        :param maybeLeftChild:
        :return:
        """
        return maybeLeftChild is self.left


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def isEmpty(self) -> bool:
        return self.root is None

    def searchTreeInsert(self, newItem) -> bool:
        if self.isEmpty():
            self.root = BinarySearchTreeNode(newItem)
            return True
        return self.insert(self.root, newItem)

    def insert(self, root, newItem) -> bool:
        if root.keyval.key == newItem.key:
            return False
        if newItem.key < root.keyval.key:
            if root.left is None:
                root.left = BinarySearchTreeNode(newItem)
                return True
            return self.insert(root.left, newItem)
        # newItem.key > root.keyval.key
        if root.right is None:
            root.right = BinarySearchTreeNode(newItem)
            return True
        return self.insert(root.right, newItem)

    def searchTreeDelete(self, searchKey) -> bool:
        if self.isEmpty():
            return False
        return self.delete(None, self.root, searchKey)

    def delete(self, parent, root, searchKey) -> bool:
        """
        param parent: The parent of root, parent is None if and only if root is self.root
        param root: root is not None
        """
        if root.keyval.key == searchKey:
            if root.left is None and root.right is None:
                if root is self.root:
                    self.root = None
                    return True
                if parent.hasLeftChild(root):
                    parent.left = None
                else:
                    parent.right = None
                return True
            if root.left is None or root.right is None:
                if root is self.root:
                    if root.left is not None:
                        self.root = root.left
                    else:
                        self.root = root.right
                    return True
                parent.keyval = root.keyval
                rootLeftChild = root.left
                rootRightChild = root.right
                root.left = None
                root.right = None
                parent.left = rootLeftChild
                parent.right = rootRightChild
                return True
            # root has 2 children
            # look for inorder successor, may the inorder successor have a right child, then make it a child of his parent
            inorderSuccessor, inorderSuccessorParent = self.getInorderSuccessor(root)
            root.keyval = inorderSuccessor.keyval
            if inorderSuccessorParent is not root:
                inorderSuccessorParent.left = None
                if inorderSuccessor.right is not None:
                    inorderSuccessorParent.left = inorderSuccessor.right
            else:
                root.right = None
            return True
        # root is not the one te be deleted => continue search recursively
        if searchKey < root.keyval.key:
            if root.left is None:
                return False
            return self.delete(root, root.left, searchKey)
        # searchKey > root.keyval.key
        if root.right is None:
            return False
        return self.delete(root, root.right, searchKey)

    def getInorderSuccessor(self, root) -> Tuple[BinarySearchTreeNode, BinarySearchTreeNode]:
        """
        Gets inorder successor of root
        :param root: root has 2 children
        :return: inorderSuccessor, parentOfInorderSuccessor
        """
        parent = root
        cur = root.right
        while cur.left is not None:
            parent = cur
            cur = cur.left
        return cur, parent

    def searchTreeRetrieve(self, searchKey) -> Tuple[Optional[KeyValuePair], bool]:
        if self.isEmpty():
            return None, False
        return self.retrieve(self.root, searchKey)

    def retrieve(self, root, searchKey) -> Tuple[Optional[KeyValuePair], bool]:
        if root.keyval.key == searchKey:
            return root.keyval, True
        if searchKey < root.keyval.key:
            if root.left is None:
                return None, False
            return self.retrieve(root.left, searchKey)
        # searchKey > root.keyval.key
        if root.right is None:
            return None, False
        return self.retrieve(root.right, searchKey)

    def inorderTraverse(self, visit):
        self.inorderTraverseRecursive(self.root, visit)

    def inorderTraverseRecursive(self, root, visit):
        if root is None:
            return
        self.inorderTraverseRecursive(root.left, visit)
        visit(root.keyval.key)
        self.inorderTraverseRecursive(root.right, visit)

    def save(self):
        if self.isEmpty():
            return dict()
        return self.saveRecursive(self.root)

    def saveRecursive(self, root):
        treeDict = dict()
        treeDict['root'] = root.keyval.key
        if root.left or root.right:
            treeDict['children'] = [None, None]
            if root.left:
                treeDict['children'][0] = self.saveRecursive(root.left)
            if root.right:
                treeDict['children'][1] = self.saveRecursive(root.right)
        return treeDict


if __name__ == '__main__':
    bst = BinarySearchTree()
    bst.searchTreeInsert(KeyValuePair(6, "Value van 6"))
    bst.searchTreeInsert(KeyValuePair(7, "Value van 7"))
    bst.searchTreeInsert(KeyValuePair(2, "Value 2"))
    bst.searchTreeInsert(KeyValuePair(3, "Value 3"))
    bst.searchTreeInsert(KeyValuePair(-10, "Value 3"))
    bst.searchTreeDelete(6)
    bst.searchTreeInsert(KeyValuePair(6, "Value van 6"))
    bst.searchTreeInsert(KeyValuePair(5, "Value van 5"))
    bst.searchTreeDelete(7)
    print(bst.searchTreeRetrieve(3)[0].val)
    bst.inorderTraverse(print)
    print(bst.save())
