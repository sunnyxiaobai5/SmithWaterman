#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

# 使用动态规划算法
# 1.读取sequence1和sequence2
# 2.获取sequence1和sequence2的长度
# 3.根据sequence1和sequence2的长度初始化两个矩阵;两个矩阵一个用来存储得分，另一个用来存储得分矩阵对应格子得分的来源
# 4.填充分值矩阵和方向矩阵
#	按从左到右，从上到下的顺序填充分值矩阵，初始坐标是(1,1)
#	1)根据左上格子获取当前格子得分；规则是：若当前格子横纵坐标字符匹配，则 得分 = 左上格子分值 + 1，否则 - 1
#	2)根据上方格子获取当前格子得分；规则是：无论匹配与否				   得分 = 上方格子分值 - 1
#	3)根据左方格子获取当前格子得分；规则是：无论匹配与否				   得分 = 左方格子分值 - 1
#	4)当前格子分值等于以上三个分值中最大的值
#	5)设置方向规则：若由左上格子得到的值等于最大值，则设置方向矩阵中对应格子值为 LU，否则 若上方得到的值为最大值，设置方向为 UP，左方同上方
# 5.获取分值矩阵中最大值的坐标
#	按从右到左，从下到上的的顺序从分值矩阵右下角开始遍历整个矩阵，若当前格子的值大于已得到的最大值，则替换，并记录坐标，遍历结束，返回坐标
# 6.构造两个序列的最终结果
#	在方向矩阵中从 5 中获取到的坐标位置开始回溯
#	1)若当前格子方向为 NO  ，停止回溯
#	2)若当前格子方向为 UP  ，则在序列 1 中加入 "_" 在序列 2 中加入当前格子 纵 坐标对应的字符，将回溯的 纵 坐标 -1
#	3)若当前格子方向为 LEFT，则在序列 2 中加入 "_" 在序列 1 中加入当前格子 横 坐标对应的字符，将回溯的 横 坐标 -1
#	4)若当前格子方向为 LU  ，则在序列 1	中加入当前格子 横 坐标对应的字符，在序列 2 中加入当前格子 纵 坐标对应的字符，将回溯的横纵坐标均 -1
# 7.逆序输出 序列1 和序列 2


# 获取当前格子应该设置的值和方向
def get_cur(matrix_score,c_row,c_col):

	# 获取由左上方格子得到的值 
	tmp = matrix_score[c_row - 1][c_col - 1]
	direction = LU
	if s1[c_col -1] == s2[c_row - 1]:
		tmp = tmp + 1
	else:
		tmp = tmp - 1
	
	# 左上角得到的值与上方的得到的值比较
	if tmp < matrix_score[c_row - 1][c_col] - 1:
		tmp = matrix_score[c_row - 1][c_col] - 1
		direction = UP

	# 左上方和上方中的最大值与左边得到的值比较
	if tmp < matrix_score[c_row][c_col - 1] - 1:
		tmp = matrix_score[c_row][c_col - 1] - 1
		direction = LEFT

	# 若最终的得到值小于等于0,将当前值设置为0,且不指定方向
	if tmp <= 0:
		direction = NO
		tmp = 0
	
	return (tmp,direction)


# 构造分值矩阵和方向矩阵
def fill_m(matrix_score,matrix_arrow,row,col,s1,s2):
	for i in range(1,row):
		for j in range(1,col):
			direction = NO
			(cur,direction) = get_cur(matrix_score,i,j)
			matrix_score[i][j] = cur
			matrix_arrow[i][j] = direction


# 获取最大分值格子的坐标
def get_max(matrix_score,row,col):

	# 初始设置最大分值为右下角的格子的分值 
	max_row = row - 1 
	max_col = col - 1 
	max_score = matrix_score[max_row][max_col]

	for i in range(max_row,-1,-1):
		for j in range(max_col,-1,-1):
			if max_score < matrix_score[i][j]:
				max_score = matrix_score[i][j]
				max_row = i
				max_col = j
	return (max_row,max_col)


# 获取最终两个序列
def result(matrix_score,matrix_arrow,row,col,s1,s2):

	# 定义两列表用于存储最终输出的两序列
	result1 = []
	result2 = []

	# 获取最大分值格子的坐标
	(max_row,max_col) = get_max(matrix_score,row,col)

	# 构造序列1的结果
	cur_row = max_row
	cur_col = max_col
	while matrix_arrow[cur_row][cur_col] != NO:
		if matrix_arrow[cur_row][cur_col] == UP:
			result1.append("_")
			cur_row -= 1
		elif matrix_arrow[cur_row][cur_col] == LEFT:
			result1.append(s1[cur_col-1])
			cur_col -= 1
		elif matrix_arrow[cur_row][cur_col] == LU:
			result1.append(s1[cur_col-1])
			cur_col -= 1
			cur_row -= 1

	# 构造序列2的结果
	cur_row = max_row
	cur_col = max_col
	while matrix_arrow[cur_row][cur_col] != NO:
		if matrix_arrow[cur_row][cur_col] == UP:
			result2.append(s2[cur_row-1])
			cur_row -= 1
		elif matrix_arrow[cur_row][cur_col] == LEFT:
			result2.append("_")
			cur_col -= 1
		elif matrix_arrow[cur_row][cur_col] == LU:
			result2.append(s2[cur_row-1])
			cur_col -= 1
			cur_row -= 1

	return (result1,result2)


# 输出最终构成的序列（逆序输出 list 的值)
def output(list_result):
	length = len(list_result)
	for i in range(length,0,-1):
		sys.stdout.write(list_result[i-1])
	print



# 定义几个方向向量的值; 0 为不设置方向
NO = 0
UP = 1
LEFT = 2
LU = 3

# 打开两个文件并读取两个序列
fileHandle1 = open("Sequence1.fasta","r");
fileHandle2 = open("Sequence2.fasta","r");
s1 = fileHandle1.read()
s2 = fileHandle2.read()
fileHandle1.close()
fileHandle2.close()

# 获取两个序列的长度
# 因为读取的时候将换行符也读取到了，所以 -1
l1 = len(s1) - 1	
l2 = len(s2) - 1

# 根据序列1和序列2的长度设置矩阵的行和列数
# 矩阵的行列比 l2 和 l1 的长度大1
M_ROW = l2 + 1
M_COL = l1 + 1

# 定义并初始化分值矩阵和方向矩阵
matrix_score = [[0 for i in range(M_COL)] for j in range(M_ROW)]
matrix_arrow = [[0 for i in range(M_COL)] for j in range(M_ROW)]

# 根据序列1和序列2构造分值矩阵和方向矩阵
fill_m(matrix_score,matrix_arrow,M_ROW,M_COL,s1,s2)

# 根据分值矩阵和方向矩阵获取最终生成的两个序列
(result1,result2) = result(matrix_score,matrix_arrow,M_ROW,M_COL,s1,s2)
# 输出结果
print "Sequence1 ",; output(result1)
print "Sequence2 ",; output(result2)
