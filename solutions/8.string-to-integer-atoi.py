'''
    Topics: String
    Difficulty: Medium
    Acceptance: 20.3%

    Implement the myAtoi(string s) function, which converts a string to a 32-bit signed integer (similar to C/C++'s atoi function).

    The algorithm for myAtoi(string s) is as follows:
    1. Read in and ignore any leading whitespace.
    2. Check if the next character (if not already at the end of the string) is '-' or '+'. Read this character in if it is either. This determines if the final result is negative or positive respectively. Assume the result is positive if neither is present.
    3. Read in next the characters until the next non-digit character or the end of the input is reached. The rest of the string is ignored.
    4. Convert these digits into an integer (i.e. "123" -> 123, "0032" -> 32). If no digits were read, then the integer is 0. Change the sign as necessary (from step 2).
    5. If the integer is out of the 32-bit signed integer range [-2^31, 2^31 - 1], then clamp the integer so that it remains in the range. Specifically, integers less than -2^31 should be clamped to -2^31, and integers greater than 2^31 - 1 should be clamped to 2^31 - 1.
    6. Return the integer as the final result.

    Example 1:
    Input: s = "42"
    Output: 42

    Example 2:
    Input: s = "   -42"
    Output: -42
    Explanation: The first non-whitespace character is '-', which is the minus sign. Then take as many numerical digits as possible, which gets 42.

    Example 3:
    Input: s = "4193 with words"
    Output: 4193
    Explanation: Conversion stops at digit '3' as the next character is not a numerical digit.
'''

class Solution(object):
    def myAtoi(self, s):
        """
        :type s: str
        :rtype: int
        """
        s = s.lstrip()
        if not s:
            return 0
        
        sign = 1
        index = 0
        
        if s[index] == '+':
            index += 1
        elif s[index] == '-':
            sign = -1
            index += 1
            
        result = 0
        while index < len(s) and s[index].isdigit():
            digit = int(s[index])
            # Check for overflow/underflow before adding digit is strictly necessary in C++/Java
            # In Python, we can just check the final result, but to simulate logic:
            result = result * 10 + digit
            index += 1
            
        result *= sign
        
        # Clamp to 32-bit signed integer range
        int_min, int_max = -2**31, 2**31 - 1
        if result < int_min:
            return int_min
        if result > int_max:
            return int_max
            
        return result
