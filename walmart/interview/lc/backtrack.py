
def get_permutation(nums, temp_arr, used):

    if len(used) == len(nums):
        res.append(temp_arr)

    for num in nums:
        if num not in used:
            used[num] = 1
            get_permutation(nums, temp_arr + [num], used)
            del used[num]


def n_queen_backtrack(n, level, taken):

        if len(taken) == n:
            tmp = []
            for board in taken:
                tmp.append('.' * board[0] + 'Q' + '.' * (n-1-board[0]))
            res.append(tmp.copy())
            return True

        taken_temp = {}
        # taken = [(pos1, level1), (pos2, level2)]
        if taken:
            for pos, lev in taken:
                taken_temp[pos] = True
                if pos + level - lev < n:
                    taken_temp[pos + level - lev] = True
                if pos - level + lev > -1:
                    taken_temp[pos - level + lev] = True

        for i in range(n):
            if i not in taken_temp:
                # taken.append((i, level))
                n_queen_backtrack(n, level + 1, taken + [(i, level)])
                # taken.pop()

        del taken_temp


#lc 78 all possible subsets
def get_all_subsets(arr, tmp, start):
    res.append(tmp)
    for i in range(start, len(arr)):
        get_all_subsets(arr, tmp + [arr[i]], i + 1)


# lc 77 combinations

def get_all_k_combinations(n, tmp, start, k):
    if len(tmp) == k:
        res.append(tmp)

    for i in range(start, n+1):
        get_all_k_combinations(n, tmp + [i], i+1, k)
    

# lc 90 all subset with duplicates


def get_all_subsets_dup(arr, tmp, start):
    res.append(tmp)

    for i in range(start, len(arr)):
        if i > start and arr[i] == arr[i-1]:
            continue
        get_all_subsets_dup(arr, tmp + [arr[i]], i+1)


# lc 40 combination sum

def comb_sum(candidates, target, tmp, start):
    if sum(tmp) == target:
        res.append(tmp)
        return True
    elif sum(tmp) > target:
        return False

    for i in range(start, len(candidates)):
        if i > start and candidates[i] == candidates[i - 1]:
            continue
        comb_sum(candidates, target, tmp + [candidates[i]], i+1)
    

if __name__ == '__main__':

    
    # n = 10
    # res = []
    # n_queen_backtrack(n, 0, [])
    # a = [1,2,3]
    # get_permutation(a, [], {})
    # print(res)
    # print(len(res))

    res = []
    # arr = [1,2,3]
    # arr = [0]
    # get_all_subsets(arr, [], 0)

    # n = 3
    # k = 2
    # get_all_k_combinations(n, [], 1, k)

    # arr = [1,2,2]
    # get_all_subsets_dup(arr, [], 0)


    # candidates = [10,1,2,7,6,1,5]
    # target = 8

    candidates = [2,5,2,1,2]
    target = 5

    candidates.sort()
    comb_sum(candidates, target, [], 0)

    print(res)




