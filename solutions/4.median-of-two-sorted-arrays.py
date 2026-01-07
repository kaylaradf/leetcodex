'''
    Topics: Array, Binary Search, Divide and Conquer
    Difficulty: Hard
    Acceptance: 45.5%

    Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

    The overall run time complexity should be O(log (m+n)).

    Example 1:
    Input: nums1 = [1,3], nums2 = [2]
    Output: 2.00000
    Explanation: merged array = [1,2,3] and median is 2.

    Example 2:
    Input: nums1 = [1,2], nums2 = [3,4]
    Output: 2.50000
    Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
'''

class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m, n = len(nums1), len(nums2)
        low, high = 0, m
        total_half_len = (m + n + 1) // 2

        while low <= high:
            partition1 = (low + high) // 2
            partition2 = total_half_len - partition1

            max_left1 = nums1[partition1 - 1] if partition1 != 0 else float('-inf')
            min_right1 = nums1[partition1] if partition1 != m else float('inf')
            
            max_left2 = nums2[partition2 - 1] if partition2 != 0 else float('-inf')
            min_right2 = nums2[partition2] if partition2 != n else float('inf')

            if max_left1 <= min_right2 and max_left2 <= min_right1:
                if (m + n) % 2 == 0:
                    return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
                else:
                    return float(max(max_left1, max_left2))
            elif max_left1 > min_right2:
                high = partition1 - 1
            else:
                low = partition1 + 1
        
        raise ValueError("Input arrays are not sorted")