package com.bhuwanupadhyay.codingproblems.contains_duplicate;


import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.stream.Stream;

import static com.bhuwanupadhyay.codingproblems.contains_duplicate.Constraints.duplicateElementsHavingArray;
import static com.bhuwanupadhyay.codingproblems.contains_duplicate.Constraints.uniqueArray;
import static org.junit.jupiter.api.Assertions.*;

class SolutionsTests {

    private static Stream<Arguments> simple() {
        return Stream.of(
                Arguments.of(new int[]{1, 2, 3, 1}, true),
                Arguments.of(new int[]{1, 2, 3, 4}, false),
                Arguments.of(new int[]{1, 1, 1, 3, 3, 4, 3, 2, 4, 2}, true)
        );
    }

    @ParameterizedTest
    @MethodSource("simple")
    void checkWithSimple(int[] input, boolean expected) {
        assertEquals(expected, new Solution1().containsDuplicate(input));
    }


    @Test
    void checkWithConstraints() {
        int maxLen = (int) (1 * Math.pow(10, 5));
        int minValue = (int) (1 * Math.pow(10, -9));
        int maxValue = (int) (1 * Math.pow(10, 9));

        int[] duplicateElementsHavingArray = duplicateElementsHavingArray(maxLen, minValue, maxValue, 5);
        assertTrue(new Solution2().containsDuplicate(duplicateElementsHavingArray));

        int[] uniqueArray = uniqueArray(maxLen, minValue, maxValue);
        assertFalse(new Solution2().containsDuplicate(uniqueArray));

    }


}