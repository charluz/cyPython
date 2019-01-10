#!/usr/bin/env python
# encoding: utf-8

#-- 類似 C 的 Macro
MaxAB = lambda a, b: a if a > b else b

#-- 模擬 C 的 switch-case
#-- emulate a fuction distribution table
def example_function_lookup_table():
    score = int(input("Input index number(6~10): "))
    lut = {
        10: lambda: print("Score 10: perfect"),
        9: lambda: print("Score 9: A"),
        8: lambda: print("Score 8: B"),
        7: lambda: print("Score 7: C"),
        6: lambda: print("Score 6: D"),
    }

    f = lut.get(score, lambda: print("Score {0}, You failed!".format(score)))
    f()


#------------------
# Main
#------------------
if not __name__ == "__main__":
    exit(0)

example_function_lookup_table()

a, b = 5, 9
print("Maximun of {0}, {1} is {2}".format(a, b, MaxAB(a, b)))
