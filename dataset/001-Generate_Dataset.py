import numpy as np
import pandas as pd
import random
import os
import subprocess

Num = 2000

def judge_increasing(data):
    diff = np.diff(data)
    if np.any(diff < -0.0001):
        return False
    return True


for i in range(Num):
    while True:
        try:
            OCR_Control = round(random.uniform(1, 10), 1)
            Stru_Control = round(random.uniform(0.1, 1.0), 2)
            OCR_initial = round(random.uniform(0.75, 1.5), 1)
            Stru_initial = round(random.uniform(0, 1), 2)

            Soil_Parameter_List = []

            Soil_Parameter_List.append(OCR_Control)
            Soil_Parameter_List.append(Stru_Control)
            Soil_Parameter_List.append(OCR_initial)
            Soil_Parameter_List.append(Stru_initial)

            # 将列表转换为DataFrame对象(也就是标签）
            Label_Data = pd.DataFrame(Soil_Parameter_List)

            with open('in.dat', 'w') as f:
                #  覆写in.dat中的第一行内容
                f.write('8' + '   ' + '2' + '\n')
                #  覆写in.dat中的第二行内容
                f.write('0.35' + '   ' + '1.08' + '   ' + '2.97' + '   ' + '0.08' + '   ' + '0.042' + '   '
                        + '1' + '   ' + '500' + '   ' + str(OCR_Control) + '   ' + str(Stru_Control) + '   ' + '0' + '   '
                        + '0' + '   ' + '1' + '   ' + '80000' + '   ' + '0.5' + '   ' + '20' + '   ' + '1.9' + '    \n')
                #  覆写in.dat中的第三行内容
                f.write('115' + '   ' + str(OCR_initial) + '   ' + str(Stru_initial) + '   ' + '0' + '   ' + '0.6' + '    \n')
                #  覆写in.dat中的第四行内容
                f.write('2' + '   ' + '2' + '   ' + '1' + '   ' + '500000' + '   ' + '500000' + '   ' + '100' + '   \n')
                #  覆写in.dat中的第五行内容
                f.write('0.15' + '   ' + '50000' + '   ' + '0' + '   \n')

            subprocess.run('TSmain.exe')

            # 获取文件夹路径
            f_path = 'out.txt'
            # 用pandas读取文件(index_col=False是为了使得表头和数据一一对应)
            data = pd.read_csv(f_path, index_col=False)
            data["SIG(1)"] = pd.to_numeric(data["SIG(1)"], errors='coerce')
            data["SIG(2)"] = pd.to_numeric(data["SIG(2)"], errors='coerce')
            data["SIG(3)"] = pd.to_numeric(data["SIG(3)"], errors='coerce')
            data["p"] = (data["SIG(1)"] + data["SIG(2)"] + data["SIG(3)"]) / 3
            data["q/p"] = (data["SIG(1)-SIG(3)"]/data["p"])
            data["u"] = (data["PORE"] - data.at[0, "PORE"])

            # 生成特征数据
            Scatter_Data = data[["EPSON11", "SIG(1)-SIG(3)", "q/p", "u"]]
            Scatter_Data.to_excel('001-CurveData_Folder/Curve_Data-{}.xlsx'.format(i + 1), index=False, header=False)

            # TODO 第一列数据
            line1_point = np.array(Scatter_Data.iloc[:, 0])


            # TODO 第二列数据
            line2_point = np.array(Scatter_Data.iloc[:, 1])
            if judge_increasing(line2_point):

                K1_max = max(np.diff(line2_point) / np.diff(line1_point))
                K1_min = min(np.diff(line2_point) / np.diff(line1_point))
                q_max = max(line2_point)
                q_min = q_max
                q_last = line2_point[-1]

            else:
                line2_diffs = np.diff(line2_point)
                line2_split_index = np.argmax(line2_diffs < 0) + 1
                line2_first_half, line2_second_half = np.split(line2_point, [line2_split_index])
                line1_first_half, line1_second_half = np.split(line1_point, [line2_split_index])

                K1_max = max(np.diff(line2_first_half) / np.diff(line1_first_half))
                K1_min = min(np.diff(line2_second_half) / np.diff(line1_second_half))
                q_max = max(line2_first_half)
                q_min = min(line2_second_half)
                q_last = line2_second_half[-1]



            #  TODO 第三列数据
            line3_point = np.array(Scatter_Data.iloc[:, 2])
            if judge_increasing(line3_point):

                K2_max = max(np.diff(line3_point) / np.diff(line1_point))
                K2_min = min(np.diff(line3_point) / np.diff(line1_point))
                qp_max = max(line3_point)
                qp_min = qp_max
                qp_last = line3_point[-1]

            else:
                line3_diffs = np.diff(line3_point)
                line3_split_index = np.argmax(line3_diffs < 0) + 1
                line3_first_half, line3_second_half = np.split(line3_point, [line3_split_index])
                line1_first_half, line1_second_half = np.split(line1_point, [line3_split_index])

                K2_max = max(np.diff(line3_first_half) / np.diff(line1_first_half))
                K2_min = min(np.diff(line3_second_half) / np.diff(line1_second_half))
                qp_max = max(line3_first_half)
                qp_min = min(line3_second_half)
                qp_last = line3_second_half[-1]


            # TODO 第四列数据
            line4_point = np.array(Scatter_Data.iloc[:, 3])

            if judge_increasing(line4_point):
                K3_max = max(np.diff(line4_point) / np.diff(line1_point))
                K3_min = min(np.diff(line4_point) / np.diff(line1_point))
                u_max = max(line4_point)
                u_min = u_max
                u_last = line4_point[-1]

            else:
                line4_diffs = np.diff(line4_point)
                line4_split_index = np.argmax(line4_diffs < 0) + 1
                line4_first_half, line4_second_half = np.split(line4_point, [line4_split_index])
                line1_first_half, line1_second_half = np.split(line1_point, [line4_split_index])

                K3_max = max(np.diff(line4_first_half) / np.diff(line1_first_half))
                K3_min = min(np.diff(line4_second_half) / np.diff(line1_second_half))
                u_max = max(line4_first_half)
                u_min = min(line4_second_half)
                u_last = line4_second_half[-1]

            
            #  TODO 创建DataFrame
            Feature_Data = pd.DataFrame({'values': [K1_max, K1_min, q_max, q_min, q_last,
                                                    K2_max, K2_min, qp_max, qp_min, qp_last,
                                                    K3_max, K3_min, u_max, u_min, u_last]})

            #  将标签和特征数据组合成一个DataFrame，然后保存在excel中
            df = pd.concat([Label_Data, Feature_Data], axis=1)
            df.to_excel('002-Dataset_Folder/Data-{}.xlsx'.format(i + 1), index=False, header=False)

            print(f"{i+1}/{Num}")
            break  # 成功生成 excel 文件，退出当前的 while 循环，开始下一次循环
        except Exception as e:
            print(f"Error: {e}")
            continue  #  如果出现报错，直接重新开始当前的循环


# TODO 设置数据文件夹路径
Data_folder = "002-Dataset_Folder"

# TODO 获取标签和特征的数量信息
df_Data = pd.read_excel("002-Dataset_Folder/Data-1.xlsx", header=None)  # 读取数据集Data-1.xlsx
Label_index_num = df_Data.iloc[:, 0].count()  # 获取Label的标签个数
Feature_index_num = df_Data.iloc[:, 1].count() # 获取Feature的特征数目

# TODO 定义一个列表
data_merged_list = []

# TODO 遍历数据文件夹，将标签数据和特征数据进行合并转置
i = 0  # 计数
for data_file in os.listdir(Data_folder):

    data_file_path = os.path.join(Data_folder, data_file)  # 获取标签数据文件所在的路径
    data_df = pd.read_excel(data_file_path, header=None)  # 使用 pandas 读取标签数据集

    data_labels = data_df.iloc[:Label_index_num, 0].transpose()  # 读取每个文件中的标签Label数据集
    data_features = data_df.iloc[:Feature_index_num, 1].transpose()  # 读取每个文件中的特征Feature数据集
    data_merged = pd.concat([data_labels, data_features], axis=0)   # 将标签Label和特征Feature进行合并
    data_merged = data_merged.to_frame().transpose()  # 对合并后的数据进行转置，保存为一行

    data_merged_list.append(data_merged)  # 依次遍历文件夹中的所有数据，添加进列表中

    i += 1  # 计数+1
    print(f"{i}/2000")  # 打印目前进行的进度情况


data_all = pd.concat(data_merged_list, ignore_index=True)
data_all.to_excel('003-Merged_Datasets/Merged-Datasets.xlsx', index=False, header=False)