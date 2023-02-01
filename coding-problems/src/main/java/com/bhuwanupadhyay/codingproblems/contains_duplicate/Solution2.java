package com.bhuwanupadhyay.codingproblems.contains_duplicate;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

class Solution2 {

    public boolean containsDuplicate(int[] nums) {
        Arrays.sort(nums);
        for (var i = 0; i < nums.length - 1; i++) {
            if (nums[i] == nums[i + 1]) {
                return true;
            }
        }
        return false;
    }

}
