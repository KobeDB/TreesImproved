from BinarySearchTree import BinarySearchTree
from BinarySearchTree import KeyValuePair

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



