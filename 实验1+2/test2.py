import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sn

pd.set_option('display.max_columns', None)  # 设置显示最大列数
pd.set_option('display.width', None)  # pandas设置显示宽度
pd.set_option('display.max_colwidth', None)  # 值的最大宽度
pd.set_option("display.max_rows", None)  # 设置显示最大行数
np.set_printoptions(threshold=np.inf)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
data = pd.read_excel('data.xlsx', sheet_name=0)

HandleCon = data['Constitution'].tolist()
y1 = []
for i in HandleCon:
    if i == 'good':
        y1.append(90)
    elif i == 'general':
        y1.append(80)
    elif i == 'bad':
        y1.append(70)
    elif i == 'excellent':
        y1.append(100)
    else:
        y1.append(70)


# 画散点图
x1 = data['C1'].tolist()
plt.title('以课程1成绩为x轴，体能成绩为y轴的散点图')
plt.xlabel('课程1成绩')
plt.ylabel('体侧成绩')
plt.xlim(xmax=100, xmin=60)  # 设置坐标轴
plt.ylim(ymax=110, ymin=50)  # 设置坐标轴
plt.scatter(x1, y1, s=50, c='blue', alpha=0.4)
plt.savefig('散点图.png')
plt.show()
plt.close('散点图.png')

# 画直方图
plt.title('课程1的成绩直方图')
plt.xlabel('课程1成绩')
plt.ylabel('人数')
plt.xlim(xmax=100, xmin=60)  # 设置坐标轴
plt.ylim(ymax=40, ymin=0)  # 设置坐标轴
plt.hist(x1, bins=10, edgecolor='black')
plt.yticks([0, 5, 10, 15, 20, 25, 30, 35, 40])  # 根据分布频率手动设置y轴的刻度
plt.xticks([60, 65, 70, 75, 80, 85, 90, 95, 100])  # 根据分布频率手动设置x轴的刻度
plt.savefig('直方图.png')
plt.show()
plt.close('直方图.png')


# 对每门成绩进行z-score归一化，得到归一化的数据矩阵
# get_average：求数组平均数
def get_average(records):
    return sum(records) / len(records)


# get_variance：求数组方差
def get_variance(records):
    average = get_average(records)
    return sum([(x - average) ** 2 for x in records]) / len(records)


# get_standard_deviation：求数组标准差
def get_standard_deviation(records):
    variance = get_variance(records)
    return math.sqrt(variance)


# get_z_score：求数组的z-score归一化最后的结果
def get_z_score(records):
    avg = get_average(records)
    stan = get_standard_deviation(records)
    scores = [(i - avg) / stan for i in records]
    return scores


rec_c1 = get_z_score(data['C1'].tolist())
rec_c2 = get_z_score(data['C2'].tolist())
rec_c3 = get_z_score(data['C3'].tolist())
rec_c4 = get_z_score(data['C4'].tolist())
rec_c5 = get_z_score(data['C5'].tolist())
rec_c6 = get_z_score(data['C6'].tolist())
rec_c7 = get_z_score(data['C7'].tolist())
rec_c8 = get_z_score(data['C8'].tolist())
rec_c9 = get_z_score(data['C9'].tolist())
rec_c10 = get_z_score(data['C10'].tolist())
rec_constitution = get_z_score(y1)
df = pd.DataFrame({'C1': rec_c1, 'C2': rec_c2,
                   'C3': rec_c3, 'C4': rec_c4,
                   'C5': rec_c5, 'C6': rec_c6,
                   'C7': rec_c7, 'C8': rec_c8,
                   'C9': rec_c9, 'Constitution': rec_constitution})

# Dataframe转矩阵
df1 = df.values
print("归一数据矩阵：\n\n\n")
df2 = pd.DataFrame({'C1': data['C1'].tolist(), 'C2': data['C2'].tolist(),
                    'C3': data['C3'].tolist(), 'C4': data['C4'].tolist(),
                    'C5': data['C5'].tolist(), 'C6': data['C6'].tolist(),
                    'C7': data['C7'].tolist(), 'C8': data['C8'].tolist(),
                    'C9': data['C9'].tolist(), 'Constitution': y1})

df3 = df2.values
corr_result = np.corrcoef(df3)
np.savetxt('归一化矩阵.txt', corr_result, fmt='%f', delimiter="\t")
print('\n\n相关矩阵:')
print(corr_result)
# 可视化混淆矩阵
df_cm = pd.DataFrame(corr_result)  # 矩阵转DataFrame
sn.heatmap(df_cm)  # 生成混淆矩阵（用热力图方式展示）
plt.savefig('混淆矩阵图.png')
plt.show()
plt.close('混淆矩阵图.png')


# 5.根据相关矩阵，找到距离每个样本最近的三个样本，得到100x3的矩阵（每一行为对应三个样本的ID）输出到txt文件中，以\t,\n间隔。
# 100*3矩阵函数
def solution5(dfm):
    value = [0, 0, 0]
    result_ID = np.zeros((len(dfm), 3))
    for i in range(len(dfm)):
        temp = sorted(dfm[i])
        value[0], value[1], value[2] = temp[-2], temp[-3], temp[-4]
        result_ID[i][0], result_ID[i][1], result_ID[i][2] = dfm[i].tolist().index(value[0]), dfm[
            i].tolist().index(value[1]), dfm[i].tolist().index(value[2])
    return result_ID


# 输出矩阵
print('\n\n\n\n100x3矩阵:')
print(solution5(corr_result))

# 保存txt文件
np.savetxt('Nearest.txt', solution5(corr_result), fmt='%d', delimiter="\t")
