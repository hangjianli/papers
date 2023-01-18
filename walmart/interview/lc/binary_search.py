# find an numberin array

import numpy as np

nums = np.array([-1,0,3,5,9,12])
target = 9


def find_number(nums, target):
    lo = 0
    hi = len(nums) - 1

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            hi = mid
        else:
            lo = mid
    return -1


print(find_number(nums, target))
# print(np.where(nums==target))

# print(np.argsort(nums, ))