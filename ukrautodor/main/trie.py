import pandas as pd
import time
import pickle


class Node():
    def __init__(self, children, isWord):
        self.children = children
        self.isWord = isWord


class Trie():
    def __init__(self, mapping):
        self.root = None
        self.mapping = mapping

    def build(self, words):
        self.root = Node({}, False)
        for word in words:
            current = self.root
            for char in word:
                if not char in current.children:
                    current.children[char] = Node({}, False)
                current = current.children[char]
            current.isWord = True

    def autocomplete(self, prefix):
        if prefix == '':
            return []
        current = self.root
        for char in prefix:
            if not char in current.children:
                return []
            current = current.children[char]
        return self._findWordsFromNode(current, prefix)

    def _findWordsFromNode(self, node, prefix):
        words = []
        if node.isWord:
            words += [{'number':prefix, 'id':self.mapping[prefix]}]  # [prefix]
        for char in node.children:
            words += self._findWordsFromNode(node.children[char], prefix + char)
        return words

    def BFS(self, key):
        if key == '':
            return []

        current = self.root
        return self._dfs_helper(current, key, '', 0)

    def find_similar(self, key):
        if key == '' or len(key) < 5:
            return []
        words = []
        for i in range(1, 4):
            words += self.BFS(key[i:])
            words += self.autocomplete(key[:-i])
        return words

    def _dfs_helper(self, node, key, prefix, index):
        words = []
        if index == len(key):
            if node.isWord:
                words += [{'number':prefix, 'id':self.mapping[prefix]}]
            for char in node.children:
                words += self._dfs_helper(node.children[char], key, prefix + char, index)
        else:
            for char in node.children:
                if char == key[index]:
                    words += self._dfs_helper(node.children[char], key, prefix + char, index + 1)
                else:
                    words += self._dfs_helper(node.children[char], key, prefix + char, 0)
        return words

    def execute(self, name, arg):
        return getattr(self, name)(arg)


def test():
    f = open("tree.txt", 'rb')
    tree = pickle.load(f)
    print(tree.root.children.keys())
    print("Data loading was completed")
    while True:
        number = input("Enter the car number: ")
        start_time = time.time()
        print(tree.autocomplete(number))
        # print(tree.BFS(number))
        print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    data = pd.read_csv("WIM_vehicles_search.csv")
    data = data[data['Id'] <= 4212862]
    data.to_html("output.html")
    print("Finished")

    mapping = dict()
    start_time = time.time()
    numbers = list(map(str, data['govNumber_plate']))

    for id, number in zip(data['Id'], numbers):
        mapping[number] = id

    tree = Trie(mapping)
    tree.build(numbers)
    print("time elapsed: {:.2f}s".format(time.time() - start_time))
    print(tree.root.children.keys())
    print("Data loading was completed")
    while True:
        number = input("Enter the car number: ")
        start_time = time.time()
        print(tree.BFS(number))
        print("time elapsed: {:.2f}s".format(time.time() - start_time))