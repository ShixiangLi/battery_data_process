
# -*- coding: utf-8 -*- 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import PySimpleGUI as sg
#%matplotlib auto

def file_pretreatment_cell(read_dir,save_dir):
    
    # 文件名读取函数
    def file_name_get(folder):
        file_dir = folder
        L = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.dat':
                    L.append(file_dir + '\\'+ file)
        return L
    
    # 预处理

    file_name_list = file_name_get(read_dir)
    save_path = save_dir
    
    for file_name in file_name_list:             
        
        # .dat文件导入
        
        data = pd.read_table(file_name,sep = '\t',header=None,engine='python')
        data = data.dropna(axis=1,how='any')

        # 修改列名

        data.columns=['串并联_Ea1','串并联_Eb1','串并联_E2','串并联_Ia','串并联_Ib','并串联_E1','并串联_E2','并串联_Ia1','并串联_Ib1','并串联_Ia2','串联_E1','串联_E2','串联_Ia','并联_E1','并联_Ia','并联_Ib','串并联_Ta01','串并联_Ta02','串并联_Tb01','串并联_Tb02','并串联_Ta01','并串联_Ta02','并串联_Tb01','并串联_Tb02','串联_Ta01','串联_Ta02','并联_Ta01','并联_Tb01','环境温度'] 

        # 剔除相同记录点，使两个记录点间的间隔为3s

        data_dedup = data.drop([x for x in range(data.shape[0]) if x % 6 != 0])

        # 调整index

        index = np.array(range(data_dedup.shape[0])) + 1

        # 增加Time列

        data_dedup.insert(0,'Time/s',(np.array(range(data_dedup.shape[0])) + 1) * 3 - 3)


        # 将处理好的数据储存为.csv文件

        data_dedup.to_csv(save_path + '\\\\' + file_name[-23:-13] + '.csv',index=False,encoding="utf_8_sig")
        

def file_pretreatment_Pack(read_dir,save_dir):
    
    def file_name_get(folder):
        file_dir = folder
        L = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.xls':
                    L.append(file_dir + '\\'+ file)
        return L
    
    file_name_list = file_name_get(read_dir)
    save_path = save_dir
    
    file = pd.DataFrame()
    file_name_current = file_name_list[0]
    for file_name in file_name_list:
    
        if file_name[-16:-6] == file_name_current[-16:-6] and file_name != file_name_list[-1]:
            data = pd.read_excel(file_name, sheet_name = 2)
            file = pd.concat([file,data], axis=1)
        elif file_name[-16:-6] != file_name_current[-16:-6] and file_name != file_name_list[-1]:
            file.to_csv(save_path + '\\\\' + file_name_current[-16:-6] + '.csv',index=False,encoding="utf_8_sig")
            file_name_current = file_name
            file = pd.DataFrame()
            data = pd.read_excel(file_name, sheet_name = 2)
            file = pd.concat([file,data], axis=1)
        else:
            data = pd.read_excel(file_name, sheet_name = 2)
            file = pd.concat([file,data], axis=1)
            file.to_csv(save_path + '\\\\' + file_name_current[-16:-6] + '.csv',index=False,encoding="utf_8_sig")
        
        
        
def capacity_and_time_pack(read_dir,save_dir):
    
    #获取电池组各循环放电容量与放电时间
    
    def file_name_get(folder):
        file_dir = folder
        L = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.csv':
                    L.append(file_dir + '\\'+ file)
        return L
    
    file_name_list = file_name_get(read_dir)
    save_path = save_dir
    
    Discharge = pd.DataFrame(columns=('Date','Capacity_SP','Time_SP','Capacity_PS','Time_PS','Capacity_S','Time_S','Capacity_P','Time_P'))
    order = ['Date','Capacity_SP','Time_SP','Capacity_PS','Time_PS','Capacity_S','Time_S','Capacity_P','Time_P']
    
    for file_name in file_name_list:    
        data = pd.read_csv(file_name)

        data = data[data['Status'].str.contains('CC_DChg')]
        if data.shape[1] == 76:
            [Capacity_SP, Time_SP] = [data.iloc[:,9], data.iloc[:,10]]
            [Capacity_PS, Time_PS] = [data.iloc[:,28], data.iloc[:,29]]
            [Capacity_S, Time_S] = [data.iloc[:,47], data.iloc[:,48]]
            [Capacity_P, Time_P] = [data.iloc[:,66], data.iloc[:,67]]

            D = pd.concat([Capacity_SP,Time_SP,Capacity_PS,Time_PS,Capacity_S,Time_S,Capacity_P,Time_P],axis=1)
            D.columns = ['Capacity_SP','Time_SP','Capacity_PS','Time_PS','Capacity_S','Time_S','Capacity_P','Time_P']
            D['Date'] = file_name[-14:-4]
            #order = ['Date','Capacity_SP','Time_SP','Capacity_PS','Time_PS','Capacity_S','Time_S','Capacity_P','Time_P']
            D = D[order]

            Discharge = pd.concat([Discharge,D], ignore_index=True)
        else:
            [Capacity_SP, Time_SP] = [data.iloc[:,9], data.iloc[:,10]]
            #[Capacity_PS, Time_PS] = [data.iloc[:,28], data.iloc[:,29]]
            [Capacity_S, Time_S] = [data.iloc[:,28], data.iloc[:,29]]
            [Capacity_P, Time_P] = [data.iloc[:,47], data.iloc[:,48]]
            
            D = pd.concat([Capacity_SP,Time_SP,Capacity_S,Time_S,Capacity_P,Time_P],axis=1)
            D.columns = ['Capacity_SP','Time_SP','Capacity_S','Time_S','Capacity_P','Time_P']
            D['Date'] = file_name[-14:-4]
            order_1 = ['Date','Capacity_SP','Time_SP','Capacity_S','Time_S','Capacity_P','Time_P']
            D = D[order_1]
            
            Discharge = pd.concat([Discharge,D], ignore_index=True)
            Discharge = Discharge[order]

    for x in ['Time_SP','Time_PS','Time_S','Time_P']:
        Discharge[x] = Discharge[x].map(lambda k: int(k[2:4]) / 60 + int(k[5:7]) / 3600 if k == k else None)
    
    Discharge.to_csv(save_path + '\\\\' + 'Discharge_Pack' + '.csv',index=True,encoding="utf_8_sig")

def capacity_cell(read_dir,save_dir,pack_dir):
    def cell_name_get(folder):
        file_dir = folder
        L = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.csv':
                    L.append(file_dir + '\\'+ file)
        return L
    
    
    
    cell_name_list = cell_name_get(read_dir)
    pack_name = pack_dir
    print(pack_name)
    save_path = save_dir

    data_pack = pd.read_csv(pack_name)
    Discharge = pd.DataFrame(columns=('Date','Ia_SP','Ib_SP','Ia1_PS','Ib1_PS','Ia2_PS','Ib2_PS','Ia_S','Ia_P','Ib_P','T_1','T_2','T_3','T_4','T_5','T_6','T_7','T_8','T_9','T_10','T_11','T_12','T_e'))
    order = ['Date','Ia_SP','Ib_SP','Ia1_PS','Ib1_PS','Ia2_PS','Ib2_PS','Ia_S','Ia_P','Ib_P','T_1','T_2','T_3','T_4','T_5','T_6','T_7','T_8','T_9','T_10','T_11','T_12','T_e']

    for cell_name in cell_name_list:
        data_cell = pd.read_csv(cell_name)

        #串并联
        data_SP_Ia = data_cell[['串并联_Ia','串并联_Ta01','串并联_Ta02','环境温度']]
        data_SP_Ib = data_cell[['串并联_Ib','串并联_Tb01','串并联_Tb02','环境温度']]
        data_SP_Ia = data_SP_Ia.drop([x for x in range(data_SP_Ia.shape[0]) if data_SP_Ia.iloc[x,0] > -0.5])
        data_SP_Ib = data_SP_Ib.drop([x for x in range(data_SP_Ib.shape[0]) if data_SP_Ib.iloc[x,0] > -0.5])
        interval = data_pack[data_pack['Date'] == cell_name[-14:-4]]['Time_SP']


        Capacity_SP = pd.DataFrame(columns=['Ia_SP','Ib_SP','T_1','T_2','T_3','T_4','T_e'])
        current_loc = 0
        for i in range(interval.shape[0]):
            if i != interval.shape[0] - 1 and interval.iloc[i] == interval.iloc[i]:
                Ia = np.mean(data_SP_Ia['串并联_Ia'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)]) * interval.iloc[i] * 1000
                Ib = np.mean(data_SP_Ib['串并联_Ib'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)]) * interval.iloc[i] * 1000
                T1 = np.mean(data_SP_Ia['串并联_Ta01'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                T2 = np.mean(data_SP_Ia['串并联_Ta02'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                T3 = np.mean(data_SP_Ib['串并联_Tb01'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                T4 = np.mean(data_SP_Ib['串并联_Tb02'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                Te = np.mean(data_SP_Ib['环境温度'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                Capacity_SP.loc[i] = [Ia,Ib,T1,T2,T3,T4,Te]
                current_loc += int(interval.iloc[i] * 3600 // 3)
            elif i == interval.shape[0] - 1 and interval.iloc[i] == interval.iloc[i]:
                Ia = np.mean(data_SP_Ia['串并联_Ia'][current_loc:]) * interval.iloc[i] * 1000
                Ib = np.mean(data_SP_Ib['串并联_Ib'][current_loc:]) * interval.iloc[i] * 1000
                T1 = np.mean(data_SP_Ia['串并联_Ta01'][current_loc:])
                T2 = np.mean(data_SP_Ia['串并联_Ta02'][current_loc:])
                T3 = np.mean(data_SP_Ib['串并联_Tb01'][current_loc:])
                T4 = np.mean(data_SP_Ib['串并联_Tb02'][current_loc:])
                Te = np.mean(data_SP_Ib['环境温度'][current_loc:])
                Capacity_SP.loc[i] = [Ia,Ib,T1,T2,T3,T4,Te]
            else:
                Ia = "Ia_SP"
                Ib = "Ib_SP"
                T1 = "T1"
                T2 = "T2"
                T3 = "T3"
                T4 = "T4"
                Te = "Te"
                Capacity_SP.loc[i] = [Ia,Ib,T1,T2,T3,T4,Te]
        Capacity_SP['Date'] = cell_name[-14:-4]
        

        #并串联

        data_PS_Ia1 = data_cell[['并串联_Ia1','并串联_Ta01','并串联_Ta02']]
        data_PS_Ib1 = data_cell[['并串联_Ib1','并串联_Tb01','并串联_Tb02']]
        data_PS_Ia2 = data_cell[['并串联_Ia2']]
        data_PS_Ib2 = data_PS_Ia1['并串联_Ia1'] + data_PS_Ib1['并串联_Ib1'] - data_PS_Ia2['并串联_Ia2']
        data_PS_Ia1 = data_PS_Ia1.drop([x for x in range(data_PS_Ia1.shape[0]) if data_PS_Ia1.iloc[x,0] > -0.5])
        data_PS_Ib1 = data_PS_Ib1.drop([x for x in range(data_PS_Ib1.shape[0]) if data_PS_Ib1.iloc[x,0] > -0.5])
        data_PS_Ia2 = data_PS_Ia2.drop([x for x in range(data_PS_Ia2.shape[0]) if data_PS_Ia2.iloc[x,0] > -0.5])
        data_PS_Ib2 = data_PS_Ib2.drop([x for x in range(data_PS_Ib2.shape[0]) if data_PS_Ib2.iloc[x] > -0.5])        
        interval = data_pack[data_pack['Date'] == cell_name[-14:-4]]['Time_PS']


        Capacity_PS = pd.DataFrame(columns=['Ia1_PS','Ib1_PS','Ia2_PS','Ib2_PS','T_5','T_6','T_7','T_8'])
        current_loc = 0
        for i in range(interval.shape[0]):
            if i != interval.shape[0] - 1 and interval.iloc[i] == interval.iloc[i]:
                Ia1 = np.mean(data_PS_Ia1['并串联_Ia1'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)]) * interval.iloc[i] * 1000
                Ib1 = np.mean(data_PS_Ib1['并串联_Ib1'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)]) * interval.iloc[i] * 1000
                Ia2 = np.mean(data_PS_Ia2['并串联_Ia2'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)]) * interval.iloc[i] * 1000
                Ib2 = np.mean(data_PS_Ib2.iloc[current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)]) * interval.iloc[i] * 1000
                T5 = np.mean(data_PS_Ia1['并串联_Ta01'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                T6 = np.mean(data_PS_Ib1['并串联_Tb01'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                T7 = np.mean(data_PS_Ia1['并串联_Ta02'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                T8 = np.mean(data_PS_Ib1['并串联_Tb02'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])                
                Capacity_PS.loc[i] = [Ia1,Ib1,Ia2,Ib2,T5,T6,T7,T8]
                current_loc += int(interval.iloc[i] * 3600 // 3)
            elif i == interval.shape[0] - 1 and interval.iloc[i] == interval.iloc[i]:
                Ia1 = np.mean(data_PS_Ia1['并串联_Ia1'][current_loc:]) * interval.iloc[i] * 1000
                Ib1 = np.mean(data_PS_Ib1['并串联_Ib1'][current_loc:]) * interval.iloc[i] * 1000
                Ia2 = np.mean(data_PS_Ia2['并串联_Ia2'][current_loc:]) * interval.iloc[i] * 1000
                Ib2 = np.mean(data_PS_Ib2.iloc[current_loc:]) * interval.iloc[i] * 1000
                T5 = np.mean(data_PS_Ia1['并串联_Ta01'][current_loc:])
                T6 = np.mean(data_PS_Ib1['并串联_Tb01'][current_loc:])
                T7 = np.mean(data_PS_Ia1['并串联_Ta02'][current_loc:])
                T8 = np.mean(data_PS_Ib1['并串联_Tb02'][current_loc:])                
                Capacity_PS.loc[i] = [Ia1,Ib1,Ia2,Ib2,T5,T6,T7,T8]                
            else:
                Ia1 = "Ia1_PS"
                Ib1 = "Ib1_PS"
                Ia2 = "Ia2_PS"
                Ib2 = "Ib2_PS"
                T5 = 'T_5'
                T6 = 'T_6'
                T7 = 'T_7'
                T8 = 'T_8'
                Capacity_PS.loc[i] = [Ia1,Ib1,Ia2,Ib2,T5,T6,T7,T8]
        Capacity_PS['Date'] = cell_name[-14:-4]

        #串联
        data_S_Ia = data_cell[['串联_Ia','串联_Ta01','串联_Ta02']]
        data_S_Ia = data_S_Ia.drop([x for x in range(data_S_Ia.shape[0]) if data_S_Ia.iloc[x,0] > -0.5])
        interval = data_pack[data_pack['Date'] == cell_name[-14:-4]]['Time_S']
        
        Capacity_S = pd.DataFrame(columns=['Ia_S','T_9','T_10'])
        current_loc = 0
        for i in range(interval.shape[0]):
            if i != interval.shape[0] - 1 and interval.iloc[i] == interval.iloc[i]:
                Ia = np.mean(data_S_Ia['串联_Ia'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)]) * interval.iloc[i] * 1000
                T9 = np.mean(data_S_Ia['串联_Ta01'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                T10 = np.mean(data_S_Ia['串联_Ta02'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                Capacity_S.loc[i] = [Ia,T9,T10]
                current_loc += int(interval.iloc[i] * 3600 // 3)
            elif i == interval.shape[0] - 1 and interval.iloc[i] == interval.iloc[i]:
                Ia = np.mean(data_S_Ia['串联_Ia'][current_loc:]) * interval.iloc[i] * 1000
                T9 = np.mean(data_S_Ia['串联_Ta01'][current_loc:])
                T10 = np.mean(data_S_Ia['串联_Ta02'][current_loc:])
                Capacity_S.loc[i] = [Ia,T9,T10]
            else:
                Ia = 'Ia_S'
                T9 = 'T_9'
                T10 = 'T_10'
                Capacity_S.iloc[i] = [Ia,T9,T10]
        Capacity_S['Date'] = cell_name[-14:-4]

        #并联

        data_P_Ia = data_cell[['并联_Ia','并联_Ta01']]
        data_P_Ib = data_cell[['并联_Ib','并联_Tb01']]
        
        
        data_P_Ia = data_P_Ia.drop([x for x in range(data_P_Ia.shape[0]) if data_P_Ia.iloc[x,0] > -0.5])
        data_P_Ib = data_P_Ib.drop([x for x in range(data_P_Ib.shape[0]) if data_P_Ib.iloc[x,0] > -0.5])
        interval = data_pack[data_pack['Date'] == cell_name[-14:-4]]['Time_P']

        Capacity_P = pd.DataFrame(columns=['Ia_P','Ib_P','T_11','T_12'])
        current_loc = 0
        for i in range(interval.shape[0]):
            if i != interval.shape[0] - 1 and interval.iloc[i] == interval.iloc[i]:
                Ia = np.mean(data_P_Ia['并联_Ia'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)]) * interval.iloc[i] * 1000
                Ib = np.mean(data_P_Ib['并联_Ib'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)]) * interval.iloc[i] * 1000
                T11 = np.mean(data_P_Ia['并联_Ta01'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                T12 = np.mean(data_P_Ib['并联_Tb01'][current_loc:int(current_loc + interval.iloc[i] * 3600 // 3)])
                Capacity_P.loc[i] = [Ia,Ib,T11,T12]
                current_loc += int(interval.iloc[i] * 3600 // 3)
            elif i == interval.shape[0] - 1 and interval.iloc[i] == interval.iloc[i]:
                Ia = np.mean(data_P_Ia['并联_Ia'][current_loc:]) * interval.iloc[i] * 1000
                Ib = np.mean(data_P_Ib['并联_Ib'][current_loc:]) * interval.iloc[i] * 1000
                T11 = np.mean(data_P_Ia['并联_Ta01'][current_loc:])
                T12 = np.mean(data_P_Ib['并联_Tb01'][current_loc:])                
                Capacity_P.loc[i] = [Ia,Ib,T11,T12]
            else:
                Ia = 'Ia_P'
                Ib = 'Ib_P'
                Capacity_P.iloc[i] = [Ia,Ib,T11,T12]
        Capacity_P['Date'] = cell_name[-14:-4]



        D = pd.concat([Capacity_SP,Capacity_PS,Capacity_S,Capacity_P],axis=1,)
        D = D[D.columns].T.drop_duplicates().T
        D = D[order]
        Discharge = pd.concat([Discharge,D])
    
    Discharge = Discharge.reset_index(drop = True) 
    Discharge.to_csv(save_path + '\\\\' + 'Discharge_Cell' + '.csv',index=True,encoding="utf_8_sig")
        
def str2sec(x):
    '''
    字符串时分秒转换成秒
    '''
    h, m, s = x.strip().split(':') #.split()函数将其通过':'分隔开，.strip()函数用来除去空格
    return int(h)*3600 + int(m)*60 + float(s) #int()函数转换成整数运算


def cell_fig(cell_date,pack_date):
    data = pd.read_csv(cell_date)
    try:
        fh = open(pack_date + '\\'+ cell_date[-14:-4] + '-2.xls', "r")
    except IOError:
        date_SP = pd.read_excel(pack_date + '\\' + cell_date[-14:-4] + '-1.xls',sheet_name=2)
        #date_PS = pd.read_excel(pack_date + '\\'+ cell_date[-14:-4] + '-2.xls',sheet_name=2)
        date_S = pd.read_excel(pack_date + '\\'+ cell_date[-14:-4] + '-3.xls',sheet_name=2)
        date_P = pd.read_excel(pack_date + '\\'+ cell_date[-14:-4] + '-4.xls',sheet_name=2)
        
        step_time_SP = date_SP.loc[:,'Endure Time(h:min:s.ms)'].map(str2sec)
        #step_time_PS = date_PS.loc[:,'Endure Time(h:min:s.ms)'].map(str2sec)
        step_time_S = date_S.loc[:,'Endure Time(h:min:s.ms)'].map(str2sec)
        step_time_P = date_P.loc[:,'Endure Time(h:min:s.ms)'].map(str2sec)
        cycle_SP = []
        #cycle_PS = []
        cycle_S = []
        cycle_P = []


        for i in range(len(step_time_SP) // 5):
            cycle_SP.append(sum(step_time_SP[i*5:i*5+5]) / 3600)
        #for i in range(len(step_time_PS) // 5):
        #    cycle_PS.append(sum(step_time_PS[i*5:i*5+5]) / 3600)
        for i in range(len(step_time_SP) // 5):
            cycle_S.append(sum(step_time_S[i*5:i*5+5]) / 3600)    
        for i in range(len(step_time_SP) // 5):
            cycle_P.append(sum(step_time_P[i*5:i*5+5]) / 3600) 
      
    
        X = data.loc[50:,'Time/s'] / 3600

        Voltage_SP_Ea1 = data.loc[50:,'串并联_Ea1']
        Voltage_SP_Ea2 = data.loc[50:,'串并联_E2'] - data.loc[50:,'串并联_Ea1']
        Voltage_SP_Eb1 = data.loc[50:,'串并联_Eb1']
        Voltage_SP_Eb2 = data.loc[50:,'串并联_E2'] - data.loc[50:,'串并联_Eb1']
        Current_SP_Ia = data.loc[50:,'串并联_Ia']
        Current_SP_Ib = data.loc[50:,'串并联_Ib']



        '''Voltage_PS_E1 = data.loc[50:,'并串联_E1']
        Voltage_PS_E2 = data.loc[50:,'并串联_E2'] - data.loc[50:,'并串联_E1']
        Current_PS_Ia1 = data.loc[50:,'并串联_Ia1']
        Current_PS_Ib1 = data.loc[50:,'并串联_Ib1']
        Current_PS_Ia2 = data.loc[50:,'并串联_Ia2']
        Current_PS_Ib2 = data.loc[50:,'并串联_Ia1'] + data.loc[50:,'并串联_Ia2'] - data.loc[50:,'并串联_Ia2']'''


        Voltage_S_E1 = data.loc[50:,'串联_E1']
        Voltage_S_E2 = data.loc[50:,'串联_E2'] - data.loc[50:,'串联_E1']
        Current_S_Ia = data.loc[50:,'串联_Ia']


        Voltage_P_E1 = data.loc[50:,'并联_E1']
        Current_P_Ia = data.loc[50:,'并联_Ia']
        Current_P_Ib = data.loc[50:,'并联_Ib']
        
        fig, ax = plt.subplots(2,2,figsize=(15,10))


        X = data.loc[50:,'Time/s'] / 3600

        Voltage_SP_Ea1 = data.loc[50:,'串并联_Ea1']
        Voltage_SP_Ea2 = data.loc[50:,'串并联_E2'] - data.loc[50:,'串并联_Ea1']
        Voltage_SP_Eb1 = data.loc[50:,'串并联_Eb1']
        Voltage_SP_Eb2 = data.loc[50:,'串并联_E2'] - data.loc[50:,'串并联_Eb1']
        Current_SP_Ia = data.loc[50:,'串并联_Ia']
        Current_SP_Ib = data.loc[50:,'串并联_Ib']



        '''Voltage_PS_E1 = data.loc[50:,'并串联_E1']
        Voltage_PS_E2 = data.loc[50:,'并串联_E2'] - data.loc[50:,'并串联_E1']
        Current_PS_Ia1 = data.loc[50:,'并串联_Ia1']
        Current_PS_Ib1 = data.loc[50:,'并串联_Ib1']
        Current_PS_Ia2 = data.loc[50:,'并串联_Ia2']
        Current_PS_Ib2 = data.loc[50:,'并串联_Ia1'] + data.loc[50:,'并串联_Ia2'] - data.loc[50:,'并串联_Ia2']'''


        Voltage_S_E1 = data.loc[50:,'串联_E1']
        Voltage_S_E2 = data.loc[50:,'串联_E2'] - data.loc[50:,'串联_E1']
        Current_S_Ia = data.loc[50:,'串联_Ia']


        Voltage_P_E1 = data.loc[50:,'并联_E1']
        Current_P_Ia = data.loc[50:,'并联_Ia']
        Current_P_Ib = data.loc[50:,'并联_Ib']



        #串并联
        ax[0][0].plot(X,Voltage_SP_Ea1, '-',linewidth=2) #画子图1的第一个y轴值
        ax[0][0].plot(X,Voltage_SP_Eb1, '--',linewidth=2)
        ax[0][0].plot(X,Voltage_SP_Ea2, '-',linewidth=2)
        ax[0][0].plot(X,Voltage_SP_Eb2, '--',linewidth=2)
        ax[0][0].set_ylim(-3,5)

        ax[0][0].set_ylabel('Voltage/V',fontsize=10) #标记它的第一个纵坐标为'num0'
        ax[0][0].set_xlabel('Time/h',fontsize=10)
        ax11 = ax[0][0].twinx() #产生子图1里的第二个纵坐标
        ax11.plot(X,Current_SP_Ia, '-',linewidth=2)#画子图1的第二个y轴值
        ax11.plot(X,Current_SP_Ib, '--',linewidth=2)
        ax11.set_ylim(-3,5)
        ax11.set_ylabel('Current/A',fontsize=10)#标记子图1里的第二个纵坐标，用'num01'表示
        for i in range(len(cycle_SP)):
            plt.axvline(x=0.04+sum(cycle_SP[:i]),ls="-.",c="k",linewidth=0.5)
        plt.title('Series-Parallel',fontsize=10)



        #并串联
        '''ax[0][1].plot(X,Voltage_PS_E1, '-',linewidth=2) 
        ax[0][1].plot(X,Voltage_PS_E2, '--',linewidth=2)
        ax[0][1].set_ylim(-3,5)
        ax[0][1].set_ylabel('Voltage/V',fontsize=10) 
        ax[0][1].set_xlabel('Time/h',fontsize=10)
        ax12 = ax[0][1].twinx() 
        ax12.plot(X,Current_PS_Ia1, '-',linewidth=2)
        ax12.plot(X,Current_PS_Ib1, '--',linewidth=2)
        ax12.plot(X,Current_PS_Ia2, '-',linewidth=2)
        ax12.plot(X,Current_PS_Ib2, '--',linewidth=2)
        ax12.set_ylim(-3,5)
        ax12.set_ylabel('Current/A',fontsize=10)
        for i in range(len(cycle_PS)):
            plt.axvline(x=0.04+sum(cycle_PS[:i]),ls="-.",c="k",linewidth=0.5)
        plt.title('Paralle-lSeries',fontsize=10)'''



        #串联
        ax[1][0].plot(X,Voltage_S_E1, '-',linewidth=2) 
        ax[1][0].plot(X,Voltage_S_E2, '--',linewidth=2)
        ax[1][0].set_ylim(-3,5)
        ax[1][0].set_ylabel('Voltage/V',fontsize=10) 
        ax[1][0].set_xlabel('Time/h',fontsize=10)
        ax21 = ax[1][0].twinx() 
        ax21.plot(X,Current_S_Ia, '-',linewidth=2)
        ax21.set_ylim(-3,5)
        ax21.set_ylabel('Current/A',fontsize=10)
        for i in range(len(cycle_S)):
            plt.axvline(x=0.04+sum(cycle_S[:i]),ls="-.",c="k",linewidth=0.5)
        plt.title('Series',fontsize=10)


        #并联
        ax[1][1].plot(X,Voltage_P_E1, '-',linewidth=2) 
        ax[1][1].set_ylim(-3,5)
        ax[1][1].set_ylabel('Voltage/V',fontsize=10) 
        ax[1][1].set_xlabel('Time/h',fontsize=10)
        ax22 = ax[1][1].twinx() 
        ax22.plot(X,Current_P_Ia, '-',linewidth=2)
        ax22.plot(X,Current_P_Ib, '--',linewidth=2)
        ax22.set_ylim(-3,5)
        ax22.set_ylabel('Current/A',fontsize=10)
        for i in range(len(cycle_P)):
            plt.axvline(x=0.04+sum(cycle_P[:i]),ls="-.",c="k",linewidth=0.5)
        plt.title('Parallel',fontsize=10)



        plt.show(block=False)
        
        
        
    else:
        
        date_SP = pd.read_excel(pack_date + '\\' + cell_date[-14:-4] + '-1.xls',sheet_name=2)
        date_PS = pd.read_excel(pack_date + '\\'+ cell_date[-14:-4] + '-2.xls',sheet_name=2)
        date_S = pd.read_excel(pack_date + '\\'+ cell_date[-14:-4] + '-3.xls',sheet_name=2)
        date_P = pd.read_excel(pack_date + '\\'+ cell_date[-14:-4] + '-4.xls',sheet_name=2)
        
        step_time_SP = date_SP.loc[:,'Endure Time(h:min:s.ms)'].map(str2sec)
        step_time_PS = date_PS.loc[:,'Endure Time(h:min:s.ms)'].map(str2sec)
        step_time_S = date_S.loc[:,'Endure Time(h:min:s.ms)'].map(str2sec)
        step_time_P = date_P.loc[:,'Endure Time(h:min:s.ms)'].map(str2sec)
        cycle_SP = []
        cycle_PS = []
        cycle_S = []
        cycle_P = []


        for i in range(len(step_time_SP) // 5):
            cycle_SP.append(sum(step_time_SP[i*5:i*5+5]) / 3600)
        for i in range(len(step_time_PS) // 5):
            cycle_PS.append(sum(step_time_PS[i*5:i*5+5]) / 3600)
        for i in range(len(step_time_SP) // 5):
            cycle_S.append(sum(step_time_S[i*5:i*5+5]) / 3600)    
        for i in range(len(step_time_SP) // 5):
            cycle_P.append(sum(step_time_P[i*5:i*5+5]) / 3600) 
      
    
        X = data.loc[50:,'Time/s'] / 3600

        Voltage_SP_Ea1 = data.loc[50:,'串并联_Ea1']
        Voltage_SP_Ea2 = data.loc[50:,'串并联_E2'] - data.loc[50:,'串并联_Ea1']
        Voltage_SP_Eb1 = data.loc[50:,'串并联_Eb1']
        Voltage_SP_Eb2 = data.loc[50:,'串并联_E2'] - data.loc[50:,'串并联_Eb1']
        Current_SP_Ia = data.loc[50:,'串并联_Ia']
        Current_SP_Ib = data.loc[50:,'串并联_Ib']



        Voltage_PS_E1 = data.loc[50:,'并串联_E1']
        Voltage_PS_E2 = data.loc[50:,'并串联_E2'] - data.loc[50:,'并串联_E1']
        Current_PS_Ia1 = data.loc[50:,'并串联_Ia1']
        Current_PS_Ib1 = data.loc[50:,'并串联_Ib1']
        Current_PS_Ia2 = data.loc[50:,'并串联_Ia2']
        Current_PS_Ib2 = data.loc[50:,'并串联_Ia1'] + data.loc[50:,'并串联_Ia2'] - data.loc[50:,'并串联_Ia2']


        Voltage_S_E1 = data.loc[50:,'串联_E1']
        Voltage_S_E2 = data.loc[50:,'串联_E2'] - data.loc[50:,'串联_E1']
        Current_S_Ia = data.loc[50:,'串联_Ia']


        Voltage_P_E1 = data.loc[50:,'并联_E1']
        Current_P_Ia = data.loc[50:,'并联_Ia']
        Current_P_Ib = data.loc[50:,'并联_Ib']
        
        fig, ax = plt.subplots(2,2,figsize=(15,10))


        X = data.loc[50:,'Time/s'] / 3600

        Voltage_SP_Ea1 = data.loc[50:,'串并联_Ea1']
        Voltage_SP_Ea2 = data.loc[50:,'串并联_E2'] - data.loc[50:,'串并联_Ea1']
        Voltage_SP_Eb1 = data.loc[50:,'串并联_Eb1']
        Voltage_SP_Eb2 = data.loc[50:,'串并联_E2'] - data.loc[50:,'串并联_Eb1']
        Current_SP_Ia = data.loc[50:,'串并联_Ia']
        Current_SP_Ib = data.loc[50:,'串并联_Ib']



        Voltage_PS_E1 = data.loc[50:,'并串联_E1']
        Voltage_PS_E2 = data.loc[50:,'并串联_E2'] - data.loc[50:,'并串联_E1']
        Current_PS_Ia1 = data.loc[50:,'并串联_Ia1']
        Current_PS_Ib1 = data.loc[50:,'并串联_Ib1']
        Current_PS_Ia2 = data.loc[50:,'并串联_Ia2']
        Current_PS_Ib2 = data.loc[50:,'并串联_Ia1'] + data.loc[50:,'并串联_Ia2'] - data.loc[50:,'并串联_Ia2']


        Voltage_S_E1 = data.loc[50:,'串联_E1']
        Voltage_S_E2 = data.loc[50:,'串联_E2'] - data.loc[50:,'串联_E1']
        Current_S_Ia = data.loc[50:,'串联_Ia']


        Voltage_P_E1 = data.loc[50:,'并联_E1']
        Current_P_Ia = data.loc[50:,'并联_Ia']
        Current_P_Ib = data.loc[50:,'并联_Ib']



        #串并联
        ax[0][0].plot(X,Voltage_SP_Ea1, '-',linewidth=2) #画子图1的第一个y轴值
        ax[0][0].plot(X,Voltage_SP_Eb1, '--',linewidth=2)
        ax[0][0].plot(X,Voltage_SP_Ea2, '-',linewidth=2)
        ax[0][0].plot(X,Voltage_SP_Eb2, '--',linewidth=2)
        ax[0][0].set_ylim(-3,5)

        ax[0][0].set_ylabel('Voltage/V',fontsize=10) #标记它的第一个纵坐标为'num0'
        ax[0][0].set_xlabel('Time/h',fontsize=10)
        ax11 = ax[0][0].twinx() #产生子图1里的第二个纵坐标
        ax11.plot(X,Current_SP_Ia, '-',linewidth=2)#画子图1的第二个y轴值
        ax11.plot(X,Current_SP_Ib, '--',linewidth=2)
        ax11.set_ylim(-3,5)
        ax11.set_ylabel('Current/A',fontsize=10)#标记子图1里的第二个纵坐标，用'num01'表示
        for i in range(len(cycle_SP)):
            plt.axvline(x=0.04+sum(cycle_SP[:i]),ls="-.",c="k",linewidth=0.5)
        plt.title('Series-Parallel',fontsize=10)



        #并串联
        ax[0][1].plot(X,Voltage_PS_E1, '-',linewidth=2) 
        ax[0][1].plot(X,Voltage_PS_E2, '--',linewidth=2)
        ax[0][1].set_ylim(-3,5)
        ax[0][1].set_ylabel('Voltage/V',fontsize=10) 
        ax[0][1].set_xlabel('Time/h',fontsize=10)
        ax12 = ax[0][1].twinx() 
        ax12.plot(X,Current_PS_Ia1, '-',linewidth=2)
        ax12.plot(X,Current_PS_Ib1, '--',linewidth=2)
        ax12.plot(X,Current_PS_Ia2, '-',linewidth=2)
        ax12.plot(X,Current_PS_Ib2, '--',linewidth=2)
        ax12.set_ylim(-3,5)
        ax12.set_ylabel('Current/A',fontsize=10)
        for i in range(len(cycle_PS)):
            plt.axvline(x=0.04+sum(cycle_PS[:i]),ls="-.",c="k",linewidth=0.5)
        plt.title('Paralle-lSeries',fontsize=10)



        #串联
        ax[1][0].plot(X,Voltage_S_E1, '-',linewidth=2) 
        ax[1][0].plot(X,Voltage_S_E2, '--',linewidth=2)
        ax[1][0].set_ylim(-3,5)
        ax[1][0].set_ylabel('Voltage/V',fontsize=10) 
        ax[1][0].set_xlabel('Time/h',fontsize=10)
        ax21 = ax[1][0].twinx() 
        ax21.plot(X,Current_S_Ia, '-',linewidth=2)
        ax21.set_ylim(-3,5)
        ax21.set_ylabel('Current/A',fontsize=10)
        for i in range(len(cycle_S)):
            plt.axvline(x=0.04+sum(cycle_S[:i]),ls="-.",c="k",linewidth=0.5)
        plt.title('Series',fontsize=10)


        #并联
        ax[1][1].plot(X,Voltage_P_E1, '-',linewidth=2) 
        ax[1][1].set_ylim(-3,5)
        ax[1][1].set_ylabel('Voltage/V',fontsize=10) 
        ax[1][1].set_xlabel('Time/h',fontsize=10)
        ax22 = ax[1][1].twinx() 
        ax22.plot(X,Current_P_Ia, '-',linewidth=2)
        ax22.plot(X,Current_P_Ib, '--',linewidth=2)
        ax22.set_ylim(-3,5)
        ax22.set_ylabel('Current/A',fontsize=10)
        for i in range(len(cycle_P)):
            plt.axvline(x=0.04+sum(cycle_P[:i]),ls="-.",c="k",linewidth=0.5)
        plt.title('Parallel',fontsize=10)



        plt.show(block=False)
        fh.close()
        
def cell_capacity_fig(call_capacity_dir):
    
    data = pd.read_csv(call_capacity_dir)
    data = data.astype('str')
    
    Ia_SP = (data.iloc[:,2].replace({'Ia_SP':np.nan})).astype("float").dropna(axis=0,how='all').reset_index(drop=True) * (-1)
    Ib_SP = (data.iloc[:,3].replace({'Ib_SP':np.nan})).astype("float").dropna(axis=0,how='all').reset_index(drop=True) * (-1)
    Ia1_PS = (data.iloc[:,4].replace({'Ia1_PS':np.nan})).astype("float").dropna(axis=0,how='all').reset_index(drop=True) * (-1)
    Ib1_PS = (data.iloc[:,5].replace({'Ib1_PS':np.nan})).astype("float").dropna(axis=0,how='all').reset_index(drop=True) * (-1) 
    Ia2_PS = (data.iloc[:,6].replace({'Ia2_PS':np.nan})).astype("float").dropna(axis=0,how='all').reset_index(drop=True) * (-1)  
    Ib2_PS = (data.iloc[:,7].replace({'Ib2_PS':np.nan})).astype("float").dropna(axis=0,how='all').reset_index(drop=True) * (-1) 
    Ia_S = (data.iloc[:,8].replace({'Ia_S':np.nan})).astype("float").dropna(axis=0,how='all').reset_index(drop=True) * (-1) 
    Ia_P = (data.iloc[:,9].replace({'Ia_P':np.nan})).astype("float").dropna(axis=0,how='all').reset_index(drop=True) * (-1) 
    Ib_P = (data.iloc[:,10].replace({'Ib_P':np.nan})).astype("float").dropna(axis=0,how='all').reset_index(drop=True) * (-1) 
    
    plt.figure(figsize=(15,10), dpi=300)
    plt.figure(1)
    ax1 = plt.subplot(221)
    plt.plot(Ia_SP,label='Ia_SP')
    plt.plot(Ib_SP,label='Ib_SP')
    plt.legend()
    plt.title('Series-Parallel',fontsize=10)
    plt.xlabel('Cycles',fontsize=10)
    plt.ylabel('Capacity/mAh',fontsize=10)
    ax2 = plt.subplot(222)
    plt.plot(Ia1_PS,label='Ia1_PS')
    plt.plot(Ib1_PS,label='Ib1_PS')
    plt.plot(Ia2_PS,label='Ia2_PS')
    plt.plot(Ib2_PS,label='Ib2_PS')
    plt.legend()
    plt.title('Parallel-Series',fontsize=10)
    plt.xlabel('Cycles',fontsize=10)
    plt.ylabel('Capacity/mAh',fontsize=10)
    ax3 = plt.subplot(223)
    plt.plot(Ia_S,label='Ia_S')
    plt.legend()
    plt.title('Series',fontsize=10)
    plt.xlabel('Cycles',fontsize=10)
    plt.ylabel('Capacity/mAh',fontsize=10)
    ax4 = plt.subplot(224)
    plt.plot(Ia_P,label='Ia_P')
    plt.plot(Ib_P,label='Ib_P')
    plt.legend()
    plt.title('Parallel',fontsize=10)
    plt.xlabel('Cycles',fontsize=10)
    plt.ylabel('Capacity/mAh',fontsize=10)
    plt.show(block=False)
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
if __name__ == "__main__":
  
    sg.ChangeLookAndFeel('GreenTan')      

    # ------ Menu Definition ------ #      
    menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],      
                ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],      
                ['Help', 'About...'], ]      

    # ------ Column Definition ------ #      
    column1 = [[sg.Text('Column 1', background_color='#F7F3EC', justification='center', size=(10, 1))],      
                [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],      
                [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],      
                [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]      

    layout = [      
        [sg.Menu(menu_def, tearoff=True)],      
        [sg.Text('锂离子电池容量数据处理系统', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],             
        [sg.InputCombo(('单体电池.dat转.csv', '电池组.xls转.csv','电池组放电容量及时间','单体电池放电容量计算','试验剖面绘制','单体电池放电容量'),key='func',font=('宋体',15), size=(20, 1))],                
        [sg.Text('读取路径', size=(8, 1)), sg.Input(key='read_path'), sg.FolderBrowse()],
        [sg.Text('保存路径', size=(8, 1)), sg.Input(key='save_path'), sg.FolderBrowse()],
        [sg.Text('电池组数据路径', size=(8, 1)), sg.Input('计算单体电池容量时填写',key='pack_path'), sg.FileBrowse()],
        [sg.Text('单体电池绘图', size=(8, 1)), sg.Input('绘制剖面时填写',key='cell_path'), sg.FileBrowse()],
        [sg.Submit(tooltip='Click to submit this window'), sg.Cancel()]    
    ]      

    window = sg.Window('Everything bagel', layout, default_element_size=(40, 1), grab_anywhere=False)      

    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):      
            break 
        elif values['func'] == '单体电池.dat转.csv':
            file_pretreatment_cell(values['read_path'],values['save_path'])
        elif values['func'] == '电池组.xls转.csv':
            file_pretreatment_Pack(values['read_path'],values['save_path'])
        elif values['func'] == '电池组放电容量及时间':
            capacity_and_time_pack(values['read_path'],values['save_path'])
        elif values['func'] == '单体电池放电容量计算':
            capacity_cell(values['read_path'],values['save_path'],values['pack_path'])
        elif values['func'] == '试验剖面绘制':
            cell_fig(values['cell_path'],values['read_path'])
        elif values['func'] == '单体电池放电容量':
            cell_capacity_fig(values['cell_path'])


    window.close()






    
    
    
    
    