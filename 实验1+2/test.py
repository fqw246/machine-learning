import pandas as pd
import numpy as np

# 读取数据
data1 = pd.read_excel('test.xlsx', sheet_name=0)
data2 = pd.read_csv('test.txt', sep=',')

pd.set_option('display.max_columns', None)  # 设置显示最大列数
pd.set_option('display.width', None)  # pandas设置显示宽度
pd.set_option('display.max_colwidth', None)  # 值的最大宽度
pd.set_option("display.max_rows", None)  # 设置显示最大行数

# 处理id问题
data1['ID'] = data1['ID'] + 202000
data2['ID'] = data2['ID'] + 202000


# 处理性别问题
def Handle_gender(gender_list):
    NewGender_list = []
    for i in gender_list:
        if i == 'girl':
            NewGender_list.append('female')
        if i == 'boy':
            NewGender_list.append('male')
        if i == 'female':
            NewGender_list.append('female')
        if i == 'male':
            NewGender_list.append('male')
    return NewGender_list


data1['Gender'] = Handle_gender(data1['Gender'].tolist())
data2['Gender'] = Handle_gender(data2['Gender'].tolist())


# 处理身高问题
def Handle_height(height_list):
    NewHeight_list = []
    for k in height_list:
        if k <= 3.00:
            NewHeight_list.append(k * 100)
        else:
            NewHeight_list.append(k)
    return NewHeight_list


data1['Height'] = Handle_height(data1['Height'].tolist())
data2['Height'] = Handle_height(data2['Height'].tolist())

# 处理体育成绩问题
Constitution_list = data1['Constitution'].tolist()
NewConstitution_list = []
for i in Constitution_list:
    if i == 'good':
        NewConstitution_list.append('good')
    elif i == 'general':
        NewConstitution_list.append('general')
    elif i == 'bad':
        NewConstitution_list.append('bad')
    elif i == 'excellent':
        NewConstitution_list.append('excellent')
    else:
        NewConstitution_list.append('general')
data1['Constitution'] = NewConstitution_list


# 填充空值
def valuation_formula(x, y):
    if x > 0:
        return x
    elif y > 0:
        return y
    else:
        return 60


# 外连接表2
tables = data1.merge(data2, how="left", on="ID")
tables['Height_x'] = tables.apply(lambda tables: valuation_formula(tables['Height_x'], tables['Height_y']), axis=1)
tables['C1_x'] = tables.apply(lambda tables: valuation_formula(tables['C1_x'], tables['C1_y']), axis=1)
tables['C2_x'] = tables.apply(lambda tables: valuation_formula(tables['C2_x'], tables['C2_y']), axis=1)
tables['C3_x'] = tables.apply(lambda tables: valuation_formula(tables['C3_x'], tables['C3_y']), axis=1)
tables['C4_x'] = tables.apply(lambda tables: valuation_formula(tables['C4_x'], tables['C4_y']), axis=1)
tables['C5_x'] = tables.apply(lambda tables: valuation_formula(tables['C5_x'], tables['C5_y']), axis=1)
tables['C6_x'] = tables.apply(lambda tables: valuation_formula(tables['C6_x'], tables['C6_y']), axis=1)
tables['C7_x'] = tables.apply(lambda tables: valuation_formula(tables['C7_x'], tables['C7_y']), axis=1)
tables['C8_x'] = tables.apply(lambda tables: valuation_formula(tables['C8_x'], tables['C8_y']), axis=1)
tables['C9_x'] = tables.apply(lambda tables: valuation_formula(tables['C9_x'], tables['C9_y']), axis=1)

# 去重
tables.drop(
    ["Name_y", "City_y", "Gender_y", "Height_y", "C1_y", "C2_y", "C3_y", "C4_y", "C5_y", "C6_y", "C7_y", "C8_y", "C9_y",
     "C10_y", "Constitution_y"], axis=1, inplace=True)
tables.drop_duplicates(subset=['ID'], keep='first', inplace=True)

# 将列名恢复成原始状态
tables.rename(
    columns={'Name_x': 'Name', 'City_x': 'City', 'Gender_x': 'Gender', 'Height_x': 'Height', 'C1_x': 'C1', 'C2_x': 'C2',
             'C3_x': 'C3', 'C4_x': 'C4', 'C5_x': 'C5', 'C6_x': 'C6', 'C7_x': 'C7', 'C8_x': 'C8', 'C9_x': 'C9',
             'C10_x': 'C10', 'Constitution_x': 'Constitution'}, inplace=True)

# 输出已经清洗后的数据
tables.to_excel('data.xlsx', index=False)


# 1.	学生中家乡在Beijing的所有课程的平均成绩。
def Average_Beijing(xx):
    xx_list = tables.loc[tables["City"] == "Beijing", xx].tolist()  # 先用列表存放传入数据
    sum1 = 0  # sum用来计算列表中所有数字总和
    for i1 in xx_list:
        sum1 += i1
    average = sum1 / len(xx_list)  # average用来存平均成绩
    print(xx + "平均成绩：" + str(average))


Average_Beijing("C1")
Average_Beijing("C2")
Average_Beijing("C3")
Average_Beijing("C4")
Average_Beijing("C5")
Average_Beijing("C6")
Average_Beijing("C7")
Average_Beijing("C8")
Average_Beijing("C9")

print("********************************************")
# 2.	学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量。
C1_list = tables.loc[tables["City"] == "Guangzhou", 'C1'].tolist()
C9_list = tables.loc[tables["City"] == "Guangzhou", 'C9'].tolist()
male_list = tables.loc[tables["City"] == "Guangzhou", 'Gender'].tolist()
sum2 = 0
for i in range(0, len(C1_list), 1):
    if C1_list[i] >= 80 and C9_list[i] >= 9 and male_list[i] == "male":
        sum2 = sum2 + 1
print("学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量:", +sum2)

print("********************************************")


# 3.	比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
def search2(xx):
    if xx == 'excellent':
        return 100
    elif xx == 'good':
        return 80
    elif xx == 'general':
        return 60
    elif xx == 'bad':
        return 0
    else:
        return xx


GZ_list = tables.loc[(tables["City"] == "Guangzhou") & (tables["Gender"] == "female"), 'Constitution'].tolist()
SH_list = tables.loc[(tables["City"] == "Shanghai") & (tables["Gender"] == "female"), 'Constitution'].tolist()
arg1 = 0
arg2 = 0
for i in range(0, len(GZ_list), 1):
    arg1 = arg1 + search2(GZ_list[i])
arg1 = arg1 / len(GZ_list)

for i in range(0, len(SH_list), 1):
    arg2 = arg2 + search2(SH_list[i])
arg2 = arg2 / len(SH_list)

if arg1 > arg2:
    print("广州女生平均体能测试成绩比较强。")
elif arg1 == arg2:
    print("广州和上海女生的平均体能测试成绩一样强。")
else:
    print("上海女生平均体能测试成绩比较强。")

print("********************************************")


# 4.
def aveg1(xx):
    xx_list = tables[xx].tolist()
    sum1 = 0
    for i in xx_list:
        sum1 += search2(i)
    average = sum1 / len(xx_list)
    return average


def fang1(xx, ave):
    xx_list = tables[xx].tolist()
    sum = 0
    for i in xx_list:
        sum = sum + pow(search2(i) - ave, 2)
    sum = sum / (len(xx_list) - 1)
    sum = np.sqrt(sum)
    return sum


def search4(xx):
    xx_list = tables[xx].tolist()
    Tiyu2 = tables['Constitution'].tolist()
    ave1 = aveg1(xx)
    fan1 = fang1(xx, ave1)
    sum3 = 0
    for i in range(0, len(xx_list), 1):
        sum3 = sum3 + ((xx_list[i] - ave1) / fan1) * ((search2(Tiyu2[i]) - ave2) / fan2)
    print("————————————————————————————————————————————")
    print("{0}成绩的平均值为：".format(xx), ave1)
    print("{0}成绩的标准差为：".format(xx), fan1)
    print("{0}课程与体育课程的相关性为：".format(xx), sum3)


ave2 = aveg1("Constitution")
fan2 = fang1("Constitution", ave2)
print("体育成绩的平均值为：", ave2)
print("体育成绩的标准差为：", fan2)
search4("C1")
search4("C2")
search4("C3")
search4("C4")
search4("C5")
search4("C6")
search4("C7")
search4("C8")
search4("C9")
