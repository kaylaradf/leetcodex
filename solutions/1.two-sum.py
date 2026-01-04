# Difficulty: Easy
# Category: Array, Hash Table

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Given an array of integers nums and an integer target, return indices of the two numbers
        such that they add up to target.
        """
        hash_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in hash_map:
                return [hash_map[complement], i]
            hash_map[num] = i
        return []

# Example of how to test the solution
if __name__ == '__main__':
    solver = Solution()
    # Test case 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    print(f"Input: nums = {nums1}, target = {target1}")
    print(f"Output: {solver.twoSum(nums1, target1)}") # Expected: [0, 1]

    # Test case 2
    nums2 = [3, 2, 4]
    target2 = 6
    print(f"Input: nums = {nums2}, target = {target2}")
    print(f"Output: {solver.twoSum(nums2, target2)}") # Expected: [1, 2]
