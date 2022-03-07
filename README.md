1. 使用序列相加和使用extend()得到的结果是相同的，但使用序列相加时，并不改变任何变量的值，而使用extend()方法时，会更改变量的值。
2. list.insert(index,obj)
3. 将num分片后的值赋给变量n后，对n进行排序的结果不影响num的变量值。这是因为对num分片后赋值给变量n时，变量n开辟的是一块新的内存空间，也就是变量n指向的内存与变量num不是同一块了，所有对变量n的操作不会影响变量num。
4. sort()方法有一个有同样功能的函数——sorted函数。该函数可以直接获取列表的副本进行排序，sorted函数的使用方式如下
5. copy()方法用于复制列表，类似于 a[:]。copyfield=field.copy()
6. remove()方法用于移除列表中某个值的第一个匹配项。list.remove(obj)；不能移除列表中不存在的值，系统会告知移除的对象不在列表中，remove()方法没有返回值，是一个直接对元素所在位置变更的方法，它修改了列表却没有返回值。
7. pop()方法用于移除列表中的一个元素，并且返回该元素的值。在使用pop()方法时，若没有指定需要移除的元素，则默认移除列表中的最后一个元素，list.pop(obj=list[-1])，对原列表进行修改
8. reverse()方法用于反向列表中的元素。该方法改变了列表但不返回值（和前面的remove()方法一样）
9. clear()方法用于清空列表，类似于 del a[:]。field.clear()
10. count()方法用于统计某个元素在列表中出现的次数
11. str.find(str, beg=0, end=len(string))
12. str.replace(old, new[, max])此语法中，str代表指定检索的字符串；old代表将被替换的子字符串；new代表新字符串，用于替换old子字符串；max代表可选字符串，如果指定了max参数，则替换次数不超过max次。
13. translate()方法的使用属于比较高级的应用，学有余力的读者可以多做一些深入了解。
14. del student['小张']  #删除 键值为“小张”的键
15. 字典中的元素是无序的，即不能通过索引下标的方式从字典中取元素;查找和插入的速度极快，不会随着字典中键的增加而变慢;字典需要占用大量内存，内存浪费多
16. get()方法返回字典中指定键的值 dict.get(key, default=None);dict代表指定字典，key代表字典中要查找的键，default代表指定的键不存在时返回的默认值
17. keys()方法用于返回一个字典的所有键 dict.keys()
18. values()方法用于返回字典中的所有值 dict.values()
19. 字典中的in操作符用于判断键是否存在于字典中 key in dict
20. dict.update(dict2) dict代表指定字典，dict2代表添加到指定字典dict里的字典
21. clear()方法用于删除字典内的所有元素 dict.clear()
22. dict.copy()
23. fromkeys()方法用于创建一个新字典，dict.fromkeys(seq[, value]))
24. items()方法以列表返回可遍历的（键/值）元组数组 dict.items()
25. setdefault()方法和get()方法类似，用于获得与给定键相关联的值 dict.setdefault(key, default=None)当键不存在时，setdefault()方法返回默认值并更新字典；当键存在时，就返回与其对应的值，不改变字典
26. 在集合中，使用add()方法为集合添加元素;在集合中，使用remove()方法可以删除的元素
27. assert x%2 == 0, "x is not an even number" 当assert后面的条件为真时，程序正常运行；当assert后面的条件为假时，输出错误信息;assert语句失败时，会引发一个AssertionError
28. 在while条件语句为false时，执行else的语句块
29. 在for条件语句为false或结束后没有被break中断时，执行else的语句块
30. 函数：关键字参数可以不按位置，如person_info(age=21,name='小萌')；默认参数：def default_param(name, age=23) 默认参数一定要放在非默认参数后面
31. 可变参数函数，*号后面的都将被放入一个列表。注意：*标记的参数可有可无。def person_info_var(arg,*vartuple):



