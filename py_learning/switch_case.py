def num_to_string(num):
    numbers = {
        0 : "zero",
        1 : "one",
        2 : "two",
        3 : "three"
    }

    return numbers.get(num, None)

if __name__ == "__main__":
    print(num_to_string(2))
    print( num_to_string(5))

'''
--------------------- 
作者：平常心o 
来源：CSDN 
原文：https://blog.csdn.net/l460133921/article/details/74892476 
版权声明：本文为博主原创文章，转载请附上博文链接！
'''