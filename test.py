class TreeNode:
    def __init__(self, vector):
        self.vector = vector
        self.left = None
        self.right = None

def compare_vectors(v1, v2):
    """So sánh theo lexicographical order"""
    for a, b in zip(v1, v2):
        if a < b:
            return -1
        elif a > b:
            return 1
    return len(v1) - len(v2)  # nếu giống nhau thì vector ngắn hơn < dài hơn

def insert_node(root, vector):
    if root is None:
        return TreeNode(vector)
    
    cmp = compare_vectors(vector, root.vector)
    if cmp < 0:
        root.left = insert_node(root.left, vector)
    else:
        root.right = insert_node(root.right, vector)
    return root

def inorder_traversal(root, result):
    if root:
        inorder_traversal(root.left, result)
        result.append(root.vector)
        inorder_traversal(root.right, result)

def tree_sort(vectors):
    root = None
    for vec in vectors:
        root = insert_node(root, vec)
    result = []
    inorder_traversal(root, result)
    return result

# ✅ Ví dụ:
data = [
    [2025, 5, 14],
    [2024, 12, 31],
    [2025, 1, 1],
    [2023, 7, 10]
]

sorted_data = tree_sort(data)

print("Sorted vectors:")
for vec in sorted_data:
    print(vec)
