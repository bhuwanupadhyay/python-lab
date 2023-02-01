package com.bhuwanupadhyay.codingproblems.contains_duplicate;

import java.util.HashMap;
import java.util.Map;

class Solution3 {

    public boolean containsDuplicate(int[] nums) {

        Map<Integer, Integer> map = new HashMap<>();

        for (var num : nums) {
            var count = map.get(num);
            if (count == null) {
                map.put(num, 1);
            } else {
                map.put(num, ++count);
            }
        }

        for (var entry : map.entrySet()) {
            if (entry.getValue() > 1) {
                return true;
            }
        }

        return false;
    }

}
