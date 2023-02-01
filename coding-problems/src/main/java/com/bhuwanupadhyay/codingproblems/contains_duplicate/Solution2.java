package com.bhuwanupadhyay.codingproblems.contains_duplicate;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

class Solution2 {

    public boolean containsDuplicate(int[] nums) {

        var sets = new HashSet<>();

        for (var num : nums) {
            if (sets.contains(num)) {
                return true;
            }
            sets.add(num);
        }

        return false;

    }

}
