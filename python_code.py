
def find_pair(num):
    nums=sorted(num)
    n=len(nums)
    for i in range(1,n):
        if(nums[i]==nums[i-1]):
            return True
        
    return False

print(find_pair([1,2,1,2]))
print(find_pair([1,3,2,3,2]))
print(find_pair([1,2,3,4]))

