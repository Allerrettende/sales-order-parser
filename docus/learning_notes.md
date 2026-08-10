# Developer Notes
My Python learning notes and frequently used commands.

[RUNOOB Markdown教程](https://www.runoob.com)  
[GitHub](https://github.com)

# Python Environment
## Activate Virtual Environment (Windows PowerShell)
```bash
.\.venv\Scripts\Activate.ps1
```
## Deactivate Environment
```bash
deactivate
```
# Python Package Management: 
- Install Package  
`pip install package_name`  
Example:  
`pip install pandas`

- Check Installed Packages  
`pip list`
- Export Environment  
`pip freeze > requirements.txt`
----
# 4. Learning Notes
2026-07-26
Virtual Environment

Python项目最好使用独立虚拟环境。
原因：
    避免不同项目包冲突
    保证项目可复现
    方便部署

Git Understanding
Git = local version control  
GitHub = remote repository

---

``使用 `反引号` 包围代码``

# 符号
转义字符
# 切片

## 简单切片
简单切片指的是这样的切片形式：a[start:stop]，  
其行为是得到下标在这样一个前闭后开区间范围内的元素，其中start和stop为负数时，简单看作是负数下标对应的位置即可。
包括start,但不包括stop位置的值

>想象某个值所在位置有左右大门，如图：|n|。start是从位置左边的大门开始，所以包括本身。stop到达位置左边的|即结束，所以不包括stop本身。    
>逆向切片，是start从右门开始，stop到右门结束。


### 超出有效索引范围
当start或stop超出上文提到的有效索引范围​时，切片操作不会抛出异常，而是进行截断。  
可以这样去理解截断机制：我们假象把索引范围扩充到全体整数，只不过小于​或大于​的区域对应空元素，在这个扩充后的数轴上进行切片，只需把最终结果中的所有空元素忽略即可。

### 缺省
start和stop都是可以缺省的，在缺省的情况下，Python的行为是尽可能取最大区间，具体来说：
按照扩充索引范围的观点，start的缺省值是无穷小(​)，stop的缺省值是无穷大(​)。


## 扩展切片
指的是这样的切片形式：a[start:stop:step]，  

### Step
其中step是一个非零整数，即比简单切片多了调整步长的功能。  
此时切片的行为可概括为：从start对应的位置出发，以step为步长索引序列，<Mark>**直至越过stop对应的位置，且不包括stop本身。**</Mark> 
事实上，简单切片就是step=1的扩展切片的特殊情况。需要详细解释的是step分别为正数和负数的两种情况。

### step为正数
当step为正数时，切片行为很容易理解，start和stop的截断和缺省规则也与简单切片完全一致：

### step为负数
当step为负数时，切片将其解释为从start出发以步长step**逆序**索引序列，此时，start和stop的截断依然遵循前述规则.  
但缺省发生一点变化，因为我们说过，在缺省的情况下，Python的行为是尽可能取最大区间，此时访问是逆序的，start应尽量取大，stop应尽量取小，才能保证区间最大，因此：  
按照扩充索引范围的观点，start的缺省值是无穷大(​)，stop的缺省值是无穷小(​)

# (),[],{}的使用
[]:List  
():Tuple  
{"":,}:Dictionary  
{}:Set

# 可迭代，迭代器
所有可以用for循环遍历的对象，都是可迭代对象，甚至包括文件对象.  
迭代器是一个可以记住遍历的位置的对象。(有点像指针，书签)
iter() 创建新对象：每次调用都会创建新的迭代器实例  
next() 不创建新对象：只修改现有迭代器的内部状态

## 比喻：队伍 + 点名员
用【队伍 + 点名员】完整讲透 for 循环底层原理
设定：
可迭代对象 = 一队人 [1,2,3]（队伍本身不会消失、顺序不变）
迭代器 = 点名员（一次性工作，有自己的进度）
```python
运行
nums = [1,2,3]
for person in nums:
    print(person)
```
Python 底层自动悄悄执行这几步：
```
it = iter(nums)
```
👉 从队伍里聘请一名新点名员
循环执行：
```
person = next(it) → 点名员喊下一个人
```
不断重复，直到点名员喊：没人了（抛出 StopIteration）
循环结束，点名员任务完成，作废。
### 关键现象对应比喻

#### 场景 1 两次 for 循环同一个列表
```python
for x in nums: print(x)
for x in nums: print(x)
```
第一轮：请来点名员 A，点名完毕，A 下班；
第二轮：重新请来点名员 B，从头开始点名。
队伍完好无损，可以无限雇佣新点名员。
#### 场景 2 复用同一个迭代器
```python
it = iter(nums)
for x in it: print(x)
for x in it: print(x)  # 无任何输出
```
只雇佣一名点名员。第一轮全部点完；
第二轮这名点名员已经全部走完，没有人可以再喊，直接结束。
#### 场景 3 两个独立迭代器
```python
it1 = iter(nums)
it2 = iter(nums)
next(it1)
print(list(it1))
print(list(it2))
```
it1、it2 是两个互不认识的点名员。
点名员 A 走到中途，不影响点名员 B 从头开始点名。
## 一句话黄金口诀（方便记忆）
- 队伍（可迭代对象）永久存在；
- 点名员（迭代器）一次性上岗，走完就下岗；
- iter () = 招募一位新点名员。

# 生成器
使用了 yield 的函数被称为生成器（generator）。  
yield 是一个关键字，用于定义生成器函数，生成器函数是一种特殊的函数，可以在迭代过程中逐步产生值，而不是一次性返回所有结果。  
跟普通函数不同的是，生成器是一个返回迭代器的函数，只能用于迭代操作，更简单点理解生成器就是一个迭代器。  
当在生成器函数中使用 yield 语句时，<函数的执行将会暂停>，并将 <yield 后面的表达式作为当前迭代的值返回。>  

## 三大关键特性（必记）
✅ 生成器属于迭代器，拥有迭代器全部特征：只能单向前进、一次性消耗  
✅ 惰性求值：不会一次性把所有数据存入内存；海量数据场景极其省内存  
比如读取百万行日志、超大数值序列，不能用列表，优先生成器  
❌ 无法重复从头遍历、不能切片、不能索引  
你不能写 gen[0]，不存在完整数据集

### 区分重点
1. list：可迭代对象，可以生成很多独立迭代器；数据常驻内存
2. iter(list)：迭代器，读取已有数据
3. generator：自带的迭代器，动态产生数据，没有后备原始队伍

### 实战例子，直观感受惰性
```python
def test():
    print("生成1")
    yield 1
    print("生成2")
    yield 2

g = test() #在调用 next 之前，函数代码根本不会执行！懒！！对应比喻：点名员不走过去，就不会临时造出这个人。
print("暂时没有任何输出！")
next(g) #打印：生成1
next(g) #打印：生成2
```
生成器：列表推导式用小括号()，不用[],[]是List

### 生成器的核心特性——惰性求值
```python
gen = (x * 3 for x in [1, 2, 3, 4])
```
此时 gen 只是一个"工厂"，还没有产出任何值  
它不占内存存储计算结果, 要取值，必须调用 next() 
```pythob
print(next(gen))  # 3  ← 现在才开始计算第一个值
print(next(gen))  # 6  ← 计算第二个值
```

## 生成器不只是一个简单的指针
生成器内部维护的不只是一个简单的索引指针，而是一个完整的执行状态帧（frame）。  
为什么说"指针"不完全准确？
|概念|	简单指针|	生成器状态帧
|---|---|---|
|存储内容|	一个地址/索引|	完整的执行环境（局部变量、循环状态、异常处理）|
|恢复执行|	直接跳转|	恢复整个执行上下文|
|可变性|	简单增减	|复杂的状态机|

## 生成器的地址
```python
gen = (x * 3 for x in [1, 2, 3, 4])
print(id(gen))  # 地址 A
next(gen)       # 消耗第一个值
print(id(gen))  # 地址 A（没变！）
next(gen)       # 消耗第二个值
print(id(gen))  # 地址 A（还是没变！）
```

### 总结一句话
__print(gen) 显示的是对象的十六进制内存地址。id(gen) 返回的是同一个地址的十进制整数形式.__  
只要你不重新赋值，生成器对象不变，地址永远固定；内部状态的变化（next 调用）不影响它所在的“房子”位置。


# 类属性与方法
## 类的私有属性
__private_attrs：两个下划线开头，声明该属性为私有，不能在类的外部被使用或直接访问。在类内部的方法中使用时 self.__private_attrs。

## 类的方法
在类的内部，使用 def 关键字来定义一个方法，与一般函数定义不同，类方法必须包含参数 self，且为第一个参数，  __self 代表的是类的实例__

## 类的私有方法
__private_method：两个下划线开头，声明该方法为私有方法，只能在类的内部调用 ，不能在类的外部调用。self.__private_methods。

# 函数
## Lambda 函数
是 Python 中用于创建简单、一次性使用的匿名函数的工具。  
它在函数式编程中非常有用，特别适合与 map()、filter()、sorted() 等函数配合使用。  
但记住：__能提高代码可读性时使用，否则优先考虑普通函数或列表推导式.__

### 与其他方式的对比
|方式	|代码	|适用场景|
|---|---|----|
|Lambda	|lambda x: x * 2	|简单单行表达式，一次性使用|
|普通函数	|def double(x): return x * 2	|复杂逻辑，多次复用|
|列表推导式	|[x * 2 for x in list]	|简单的列表转换，比 map 更直观|

## Map 函数
map() 是 Python 内置的高阶函数，用于将一个函数应用于可迭代对象（如列表、元组等）的每个元素，并返回一个迭代器。  
重要：map 对象只能使用一次

### 基本语法
```python
map(函数, 可迭代对象1, 可迭代对象2, ...)
```
函数：可以是普通函数、lambda 表达式，或任何可**调用对象**. (<Mark>不是函数调用，如test，而不是test().</Mark>) 
可迭代对象：一个或多个序列（列表、元组、字符串等）  
返回值：返回一个 map 对象（迭代器），可以通过 list()、tuple() 等转换为具体的数据结构

```python
from math import sqrt

points = [(1, 2), (3, 4), (5, 6)]
center = (2, 3)  # 自定义中心点

def dist_from_center(p):
    return sqrt((p[0] - center[0])**2 + (p[1] - center[1])**2)

distances = list(map(dist_from_center, points)) #不是dist_from_center()
print(distances)  # [1.414, 1.414, 4.243]

```
### 总结
Map 是函数式编程中的重要工具，用于批处理数据  
最常与 lambda 表达式配合使用  
返回迭代器，惰性求值，节省内存  
可以处理多个可迭代对象  
在简单的转换场景下，列表推导式通常更 Pythonic  
适合与现有函数（如 int(), str(), strip() 等）配合使用  
### 选择建议：
简单转换：使用列表推导式  
复杂逻辑或函数复用：使用 map  
处理多个可迭代对象：使用 map  
链式处理：可以使用 map 组合


# if __name__ == "__main__":

用来控制 Python 代码的执行时机  
在 Python 中，每个模块（.py 文件）都有一个内置属性 __name__。

当模块被直接运行时，__name__ 被设置为 "__main__"

当模块被导入时，__name__ 被设置为该模块的文件名（不含 .py）
## 用途
1. 双用途模块
让一个文件既能被直接运行，又能被作为库导入：
2. 作为程序入口点
相当于其他语言的 main() 函数：
```python
# main.py
import sys
from pathlib import Path

def process_data(input_file):
    # 处理数据...
    pass

def main():
    """程序主入口"""
    if len(sys.argv) < 2:
        print("请指定输入文件")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    process_data(input_file)
    print("处理完成！")

if __name__ == "__main__":
    main()
```


## 核心作用：

✅ 隔离测试代码：让测试代码只在开发时运行

✅ 定义程序入口：清晰告诉用户这个文件的用途

✅ 模块复用：同一个文件既能被调用，也能被导入

✅ 最佳实践：Python 项目中的标准写法

黄金法则： 任何可以直接运行的 Python 脚本都应该包含这个判断！