class Blog:
    def __init__(self, num):
        print("a new object num is", num)
        self.value = num

    def __str__(self):
        return str(self.value)


# 循环建立四个对象，locals()函数可以将字符串转换为变量名！
# 具体的操作和含义我并不清楚，大家可以自行百度～
for i in range(1, 5):
    locals()['blog_' + str(i)] = Blog(i)

# 验证是否有blo_3这个对象变量
print(blog_1)
