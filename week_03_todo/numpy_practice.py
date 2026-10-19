import numpy as np

scores = np.array(
    [
    [85,90],
    [78,88],
    [92,95],
    [60,70]
    ]
)

# # day1
# print(scores)         # 打印数组
# print(scores.shape)   # 形状 (4, 2)
# print(scores.ndim)      # 维度
# print(scores.dtype)    # 数据类型
# print('-'*40)
# # 1. 取出第三个学生的两科成绩
# print(scores[2])
# print('-'*40)
# # 2. 取出所有学生的第二科成绩
# print(scores[:,1])
# print('-'*40)
# # 3. 取出前两个学生的数据
# print(scores[:2])
# print('-'*40)
# # 4. 将第四个学生的第一科成绩改为65
# scores[3][0] = 65
# print(scores[3])
# print('-'*40)

# day2
# # 每门课程的平均分 列平均
# print(scores.mean(axis=0))
# print('-'*40)
# # 每个学生的平均分 行平均
# print(scores.mean(axis=1))
# print('-'*40)
# # 总分
# print(scores.sum(axis=1))
# # 第一科成绩达到80的学生
# print(scores[scores[:,0]>=80])
#
# #这里表示每个学生第一科加 2 分、第二科加 3 分。NumPy 会让这个长度为 2 的数组参与每一行的运算。
# bonus = np.array([2, 3])
# adjusted_scores = scores + bonus

# day2 验收
# 计算每个学生的总分和平均分
print(scores.sum(axis=1))
print(scores.mean(axis=1))
print('-'*40)

# 每门课程的最高分
print(scores.max(axis=0))
print('-'*40)

# 平均分不低于85的学生
print(scores[scores.mean(axis=1)>=85])
print('-'*40)

#比较下面两个的区别
scores1 = scores * 2
scores2 = [85,90] *2
print(scores1)
print(scores2)


