# #
# # "LSM树"
# class MemTable:
#     """简单的内存表"""
#     def __init__(self, max_size=5):
#         self.max_size = max_size
#         self.data = {}
#
#     def put(self, key, value):
#         """插入数据"""
#         self.data[key] = value
#         return len(self.data) >= self.max_size  # 返回是否已满
#
#     def get(self, key):
#         """查询数据"""
#         return self.data.get(key)
#
#     def get_all_data(self):
#         """获取所有数据"""
#         return list(self.data.items())
#
# class SSTable:
#     """简单的磁盘表（用列表模拟）"""
#     def __init__(self, data):
#         # 数据按键排序存储
#         self.data = sorted(data, key=lambda x: x[0])
#
#     def get(self, key):
#         """二分查找数据"""
#         left, right = 0, len(self.data) - 1
#
#         while left <= right:
#             mid = (left + right) // 2
#             mid_key, mid_value = self.data[mid]
#
#             if mid_key == key:
#                 return mid_value
#             elif mid_key < key:
#                 left = mid + 1
#             else:
#                 right = mid - 1
#
#         return None  # 没找到
#
# class SimpleLSMTree:
#     """简单的LSM树"""
#
#     def __init__(self, memtable_size=5):
#         self.memtable_size = memtable_size
#         self.memtable = MemTable(memtable_size)
#         self.sstables = []  # SSTable列表，新的在前面
#
#     def put(self, key, value):
#         """插入数据"""
#         # 先插入内存表
#         is_full = self.memtable.put(key, value)
#
#         # 如果内存表满了，刷新到磁盘
#         if is_full:
#             self._flush_to_disk()
#
#     def get(self, key):
#         """查询数据"""
#         # 先查内存表
#         result = self.memtable.get(key)
#         if result is not None:
#             return result
#
#         # 再查SSTable（从新到旧）
#         for sstable in self.sstables:
#             result = sstable.get(key)
#             if result is not None:
#                 return result
#
#         return None  # 没找到
#
#     def _flush_to_disk(self):
#         """将内存表数据刷新到磁盘"""
#         if not self.memtable.data:
#             return
#
#         # 获取内存表所有数据
#         data = self.memtable.get_all_data()
#
#         # 创建新的SSTable
#         new_sstable = SSTable(data)
#
#         # 添加到SSTable列表（新的在前面）
#         self.sstables.insert(0, new_sstable)
#
#         # 清空内存表
#         self.memtable = MemTable(self.memtable_size)
#
#         print(f"内存表已刷新到磁盘，创建了新的SSTable，包含 {len(data)} 条数据")
#
#     def print_status(self):
#         """打印当前状态"""
#         print(f"\n=== LSM树状态 ===")
#         print(f"内存表大小: {len(self.memtable.data)}/{self.memtable_size}")
#         print(f"SSTable数量: {len(self.sstables)}")
#
#         for i, sstable in enumerate(self.sstables):
#             print(f"SSTable {i}: {len(sstable.data)} 条数据")
#
#         # 显示所有数据
#         all_data = {}
#
#         # 内存表数据（最新）
#         for key, value in self.memtable.data.items():
#             all_data[key] = value
#
#         # SSTable数据（从新到旧）
#         for sstable in self.sstables:
#             for key, value in sstable.data:
#                 if key not in all_data:  # 只保留旧数据中未被覆盖的
#                     all_data[key] = value
#
#         if all_data:
#             print("\n所有数据（按键排序）:")
#             for key in sorted(all_data.keys()):
#                 print(f"  {key}: {all_data[key]}")
#         else:
#             print("\n当前没有数据")
#
# # 演示函数
# def demo_simple_lsm():
#     """演示简单的LSM树"""
#     print("=== 简单LSM树演示 ===\n")
#
#     # 创建LSM树，内存表大小为3（很小以便演示刷新）
#     lsm = SimpleLSMTree(memtable_size=3)
#
#     # 插入一些数据
#     test_data = [
#         ("name", "Alice"),
#         ("age", "25"),
#         ("city", "Beijing"),  # 插入3条后内存表会满
#         ("country", "China"), # 这会触发刷新
#         ("job", "Engineer"),
#         ("language", "Python")
#     ]
#
#     print("插入数据:")
#     for key, value in test_data:
#         print(f"  插入: {key} = {value}")
#         lsm.put(key, value)
#
#     # 查询演示
#     print("\n查询演示:")
#     test_queries = ["name", "age", "country", "nonexistent"]
#     for query in test_queries:
#         result = lsm.get(query)
#         print(f"  查询 '{query}': {result}")
#
#     # 显示最终状态
#     lsm.print_status()
#
# # 运行演示
# if __name__ == "__main__":
#     demo_simple_lsm()









#Merkle树
import hashlib
from typing import List, Optional


class MerkleNode:
    """Merkle树节点"""

    def __init__(self, hash_value: str, left=None, right=None, data=None):
        self.hash = hash_value
        self.left = left
        self.right = right
        self.data = data  # 仅叶子节点存储数据

    def __repr__(self):
        return f"MerkleNode(hash={self.hash[:8]}...)"


class MerkleTree:
    """Merkle树实现"""

    @staticmethod
    def hash_data(data: str) -> str:
        """计算数据的SHA-256哈希值"""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def __init__(self, data: List[str]):
        if not data:
            self.root = None
            return

        # 创建叶子节点
        leaves = []
        for item in data:
            leaf_hash = self.hash_data(item)
            leaves.append(MerkleNode(leaf_hash, data=item))

        # 如果叶子节点数量不是2的幂，复制最后一个节点直到满足条件
        while len(leaves) > 1 and (len(leaves) & (len(leaves) - 1)) != 0:
            leaves.append(leaves[-1])

        self.leaves = leaves
        self.root = self._build_tree(leaves)

    def _build_tree(self, nodes: List[MerkleNode]) -> MerkleNode:
        """递归构建Merkle树"""
        if len(nodes) == 1:
            return nodes[0]

        next_level = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1] if i + 1 < len(nodes) else left

            # 合并左右节点的哈希
            combined_hash = left.hash + right.hash
            parent_hash = self.hash_data(combined_hash)

            parent_node = MerkleNode(parent_hash, left, right)
            next_level.append(parent_node)

        return self._build_tree(next_level)

    def get_root_hash(self) -> str:
        """获取根哈希"""
        return self.root.hash if self.root else ""

    def verify_data(self, data: str) -> bool:
        """验证数据是否在树中"""
        target_hash = self.hash_data(data)
        return self._verify_hash(target_hash, self.root)

    def _verify_hash(self, target_hash: str, node: MerkleNode) -> bool:
        """递归验证哈希"""
        if node is None:
            return False

        # 如果是叶子节点，直接比较哈希
        if node.left is None and node.right is None:
            return node.hash == target_hash

        # 如果是内部节点，检查左右子树
        left_result = self._verify_hash(target_hash, node.left)
        right_result = self._verify_hash(target_hash, node.right)

        return left_result or right_result

    def get_proof(self, data: str) -> List[str]:
        """获取数据的Merkle证明路径"""
        target_hash = self.hash_data(data)
        proof = []
        self._find_proof(target_hash, self.root, proof)
        return proof

    def _find_proof(self, target_hash: str, node: MerkleNode, proof: List[str]) -> bool:
        """递归查找证明路径"""
        if node is None:
            return False

        # 如果是叶子节点
        if node.left is None and node.right is None:
            if node.hash == target_hash:
                return True
            return False

        # 检查左子树
        if self._find_proof(target_hash, node.left, proof):
            proof.append(node.right.hash)  # 添加兄弟节点哈希
            return True

        # 检查右子树
        if self._find_proof(target_hash, node.right, proof):
            proof.append(node.left.hash)  # 添加兄弟节点哈希
            return True

        return False

    @staticmethod
    def verify_proof(data: str, proof: List[str], root_hash: str) -> bool:
        """使用Merkle证明验证数据"""
        current_hash = MerkleTree.hash_data(data)

        for sibling_hash in proof:
            # 决定哈希组合的顺序（根据哈希值大小）
            if current_hash < sibling_hash:
                combined = current_hash + sibling_hash
            else:
                combined = sibling_hash + current_hash

            current_hash = MerkleTree.hash_data(combined)

        return current_hash == root_hash

    def print_tree(self, node: Optional[MerkleNode] = None, level: int = 0, prefix: str = "根"):
        """打印树结构"""
        if node is None:
            if level == 0:
                node = self.root
            if node is None:
                print("空树")
                return

        indent = "    " * level
        hash_display = node.hash[:12] + "..."

        if node.data:
            print(f"{indent}{prefix}: {hash_display} (数据: '{node.data}')")
        else:
            print(f"{indent}{prefix}: {hash_display}")

        if node.left:
            self.print_tree(node.left, level + 1, "左")
        if node.right and node.right != node.left:  # 避免重复打印复制的节点
            self.print_tree(node.right, level + 1, "右")


def demo_merkle_tree():
    """演示Merkle树的使用"""
    print("=== Merkle树演示 ===\n")

    # 测试数据
    data_list = ["区块1", "区块2", "区块3", "区块4"]
    print(f"原始数据: {data_list}")

    # 创建Merkle树
    merkle_tree = MerkleTree(data_list)

    # 显示根哈希
    root_hash = merkle_tree.get_root_hash()
    print(f"根哈希: {root_hash}")

    # 打印树结构
    print("\nMerkle树结构:")
    merkle_tree.print_tree()

    # 验证数据
    print("\n数据验证:")
    test_data = ["区块1", "区块3", "不存在的数据"]
    for data in test_data:
        exists = merkle_tree.verify_data(data)
        print(f"  '{data}' 是否存在: {exists}")

    # Merkle证明演示
    print("\nMerkle证明演示:")
    for data in ["区块2", "区块4"]:
        proof = merkle_tree.get_proof(data)
        is_valid = MerkleTree.verify_proof(data, proof, root_hash)
        print(f"  '{data}' 的证明路径: {[p[:8] + '...' for p in proof]}")
        print(f"  证明验证结果: {is_valid}")

    # 演示数据篡改检测
    print("\n数据篡改检测:")
    tampered_data = "篡改的数据"
    fake_proof = merkle_tree.get_proof("区块1")  # 使用区块1的证明路径
    is_valid_tampered = MerkleTree.verify_proof(tampered_data, fake_proof, root_hash)
    print(f"  篡改数据验证结果: {is_valid_tampered} (应该为False)")


def advanced_demo():
    """高级演示：不同数据量的Merkle树"""
    print("\n" + "=" * 50)
    print("高级演示：不同数据量的Merkle树")
    print("=" * 50)

    # 测试不同数量的数据
    test_cases = [
        ["单一数据"],
        ["数据A", "数据B"],
        ["1", "2", "3", "4", "5"],
        ["a", "b", "c", "d", "e", "f", "g", "h"]
    ]

    for i, data in enumerate(test_cases, 1):
        print(f"\n--- 测试用例 {i}: {len(data)} 个数据项 ---")
        tree = MerkleTree(data)
        print(f"根哈希: {tree.get_root_hash()[:16]}...")

        # 验证所有数据
        for item in data:
            if tree.verify_data(item):
                print(f"  ✓ '{item}' 验证成功")
            else:
                print(f"  ✗ '{item}' 验证失败")


if __name__ == "__main__":
    demo_merkle_tree()
    advanced_demo()