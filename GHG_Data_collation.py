# -*- coding: utf-8 -*-

#%% 資料處理

import numpy as np
import pandas as pd


# 讀取Excel檔案
file_path = r"F:\shareDATA\溫室氣體監測\彙整.xlsx"
xl = pd.ExcelFile(file_path)

# 取得所有分頁名稱
sheet_names = xl.sheet_names
sheet_names.remove(sheet_names[-1])

# 建立空的liat來存放資料
data = []

for sheet in sheet_names:
    
    # 取得分頁資料
    df = pd.read_excel(file_path, sheet)
    df = df.iloc[[0,14, 15,16,17,18,19,20,21,22],:]
    
    # 取得檢測項目
    item = sheet.split('(')[1].split(')')[0]
    # 取得作物類別
    plant = df.iloc[1,0][-2]
    
    # 依序執行不同行
    for num in range(3, df.shape[1]):
        
        # 取得檢測日期
        day = df.iloc[0,num].strftime('%Y-%m-%d')
        # 取得檢測數值
        for i in range(1,10):
            value = df.iloc[i, num]
            if np.isnan(value):
                pass
            else:
                L = [day, plant, i, item, round(value,2)]
                data.append(L)


data = pd.DataFrame(data, columns = ['date', 'plant', 'no', 'item', 'flux(mg /h/m2)'])

# 加入施氮量
mask_S = (data['plant'] == 'S') & (data['no'].isin([3, 7, 9]))
mask_P = (data['plant'] == 'P') & (data['no'].isin([3, 7, 9]))
data.loc[mask_S | mask_P, 'treat'] = 'N0'

mask_S = (data['plant'] == 'S') & (data['no'].isin([1, 6, 8]))
mask_P = (data['plant'] == 'P') & (data['no'].isin([2, 4, 5]))
data.loc[mask_S | mask_P, 'treat'] = 'N40'

mask_S = (data['plant'] == 'S') & (data['no'].isin([2, 4, 5]))
mask_P = (data['plant'] == 'P') & (data['no'].isin([1, 6, 8]))
data.loc[mask_S | mask_P, 'treat'] = 'N80'

# data.to_csv(r'F:\shareDATA\溫室氣體監測\86田資料統整.csv', index = False, encoding = 'utf-8-sig')
#%% 畫圖
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

file = r'F:\shareDATA\溫室氣體監測\86田資料統整.csv'

data_1 = pd.read_csv(file)
# 選擇分析作物及項目
# 注意，Soybean需移除03/10的資料
day = '2023-02-16'  # 2023-02-16, 2023-03-13
plant = 'Peanut'    # Peanut, Soybean
item = 'CH4'  # CO2, N2O, CH4, N2O-N
T1, T2 = 1, 69    # 1, 69, -24, 44

# 篩選資料
plant_day = pd.Timestamp(day)
data_1 = data_1[(data_1['plant'] == plant[0])]
data_1 = data_1[(data_1['item'] == item)]

# 取得平均值與標準偏差
data_1['name'] = data_1['date'] + data_1['treat']
data_mean = data_1[['flux(mg /h/m2)', 'name']].groupby('name').mean()
data_std = data_1[['flux(mg /h/m2)', 'name']].groupby('name').std()

# 彙整
data_2 = pd.concat([data_mean, data_std], axis = 1)
data_2.columns = ['mean', 'std']
data_2['date'] = pd.to_datetime(data_2.index.str[:10])
data_2['treat'] = data_2.index.str[10:]
# 重新定義index
data_2 = data_2.reset_index(drop = True)
# 將std為nan的移除
data_2 = data_2.dropna(subset=['std'])
# 計算種植天數
data_2['DAP'] = (data_2['date'] - plant_day).dt.days
# 將'mean'小於0的值改為0
data_2.loc[data_2['mean'] < 0, 'mean'] = 0

# 排除資料
# data_2 = data_2.iloc[1:,]

# =============================================================================
# 計算anova與LSD
# =============================================================================
# 因只有3施肥處理，直接將資料取出
df1 = data_2[data_2['treat'] == 'N0']['mean']
df2 = data_2[data_2['treat'] == 'N40']['mean']
df3 = data_2[data_2['treat'] == 'N80']['mean']

# 進行ANOVA
f_stat, p_value = stats.f_oneway(df1, df2, df3)

# 進行LSD（最小顯著差異）檢定
LSD = stats.t.ppf(0.975, len(data_2)) * stats.sem(data_2['mean'])
LSD_table = pd.DataFrame({'N0 vs N40': [df1.mean() - df2.mean() - LSD, df1.mean() - df2.mean() + LSD],
                              'N0 vs N80': [df1.mean() - df3.mean() - LSD, df1.mean() - df3.mean() + LSD],
                              'N40 vs N80': [df2.mean() - df3.mean() - LSD, df2.mean() - df3.mean() + LSD]})
f_stat = round(f_stat,3)
p_value = round(p_value,3)
LSD_table = round(LSD_table,4)
ANOVA_table = pd.DataFrame([f_stat, p_value], index = ["F-statistic:", "p-value:"], columns = ["ANOVA結果:"])
ANOVA_table = ANOVA_table.reset_index()
ANOVA_table.columns = ['', "ANOVA:"]
# # 顯示ANOVA結果
# print("ANOVA結果：")
# print("F-statistic:", round(f_stat,3))
# print("p-value:", round(p_value,3))

# # 顯示LSD檢定結果
# print("LSD結果：")
# print(round(LSD_intervals,3))

# =============================================================================
# 有errorbar
# =============================================================================
# 建立新的圖表
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams["axes.unicode_minus"] = False
plt.figure(dpi=200)
# 取得唯一的 'treat' 值
treat_values = data_2['treat'].unique()
# 逐一繪製不同 'treat' 值的折線圖
for treat in treat_values:
    # 選取相應的資料
    subset = data_2[data_2['treat'] == treat]
    # 繪製折線圖，以 'DOP' 為 x 軸，'mean' 為 y 軸，誤差條為 'std' 值
    plt.errorbar(subset['DAP'], subset['mean'], yerr=subset['std'], fmt='o-', capsize=3, label=treat)

plt.axhline(0, color='black', linestyle='-', linewidth=0.8)
plt.axvline(T1, color='Orange', linestyle='--', linewidth=0.8)
plt.axvline(T2, color='Orange', linestyle='--', linewidth=0.8)
plt.xlabel('DAP (days)')
plt.ylabel(f'flux (mg {item}/h/m2)')
plt.legend()
plt.title(f'{plant}  {item}')
table1 = plt.table(cellText = ANOVA_table.values, colLabels = ANOVA_table.columns, loc='center', bbox=[0.0, -0.4, 0.35, 0.2])
table2 = plt.table(cellText = LSD_table.values, colLabels = LSD_table.columns, loc='center', bbox=[0.45, -0.4, 0.55, 0.2])
table1.auto_set_font_size(False)
table1.set_fontsize(10)
table2.auto_set_font_size(False)
table2.set_fontsize(10)
plt.show()

# =============================================================================
# # 單純折線圖
# =============================================================================
# 建立新的圖表
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams["axes.unicode_minus"] = False
plt.figure(dpi=200)
# 取得唯一的 'treat' 值
treat_values = data_2['treat'].unique()
# 逐一繪製不同 'treat' 值的折線圖
for treat in treat_values:
    # 選取相應的資料
    subset = data_2[data_2['treat'] == treat]
    # 繪製折線圖，以 'DOP' 為 x 軸，'mean' 為 y 軸
    plt.plot(subset['DAP'], subset['mean'], marker='o', label=treat)

# 加入 y=0 的水平線
plt.axhline(0, color='black', linestyle='-', linewidth=0.8)
plt.axvline(T1, color='Orange', linestyle='--', linewidth=0.8)
plt.axvline(T2, color='Orange', linestyle='--', linewidth=0.8)
plt.xlabel('DAP (days)')
plt.ylabel(f'flux (mg {item}/h/m2)')
plt.legend()
plt.title(f'{plant}  {item}')
# plt.text(0, -30, "ANOVA結果:", ha='left')
# plt.text(0, -35, f"F-statistic: {f_stat,3}", ha='left')
# plt.text(0, -40, f"p-value: {p_value,3}", ha='left')
table1 = plt.table(cellText = ANOVA_table.values, colLabels = ANOVA_table.columns, loc='center', bbox=[0.0, -0.4, 0.35, 0.2])
table2 = plt.table(cellText = LSD_table.values, colLabels = LSD_table.columns, loc='center', bbox=[0.45, -0.4, 0.55, 0.2])
table1.auto_set_font_size(False)
table1.set_fontsize(10)
table2.auto_set_font_size(False)
table2.set_fontsize(10)
plt.show()
