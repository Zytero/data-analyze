import datetime
import os
import urllib.request
import pandas as pd
import __main__ as main

def dir_c():
    MainDir='DataCSV'
    CurrentTime=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dir_path=os.path.join("DataCSV",f"NOAA_{CurrentTime}")
    os.makedirs(dir_path)


    for provid in range(1,28):
        url=f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?provinceID={provid}&country=UKR&yearlyTag=Weekly&type=Mean&TagCropland=crop&year1=1982&year2=2024'
        FileName=f"NOAA_ID{provid}_{CurrentTime}.csv"
        FilePath=os.path.join(dir_path,FileName)

        try:
            urllib.request.urlretrieve(url,FilePath)  
        except Exception as e: print(e)

def cleandf():
    MainDir='DataCSV'
    if not os.path.exists(MainDir):
        print(f'Директорія {MainDir} не створена')
    else:
        ls =[]

        dirs=[]
        for file in os.listdir(MainDir): 
            if os.path.isdir(os.path.join(MainDir,file)): 
                dirs.append(file)

        ###Choosing Newest directory
        if len(dirs) == 1:
            NewestDir=os.path.join(MainDir,dirs[0])
        else:
            for i in range(1,len(dirs)):
                if os.path.getctime(os.path.join(MainDir,dirs[i-1])) < os.path.getctime(os.path.join(MainDir,dirs[i])):
                    NewestDir=os.path.join(MainDir,dirs[i])
        #print(NewestDir)

        ##Creating df
        files=os.listdir(NewestDir)
        for i,file in enumerate(files):
            FilePath=os.path.join(NewestDir,file)
            df=pd.read_csv(FilePath,index_col=False,header=1)
            df["ID"]=i+1
            ls.append(df)

        df=pd.concat(ls)

    ###Rename columns
        df=df.rename(columns={' SMN': 'SMN'})
        df=df.rename(columns={' VHI<br>': 'VHI'})
        
    ###Cleaning Nan and -1
        df=df.dropna()
        df=df.drop(df.loc[df['VHI'] == -1].index)

    ###Cleaning html tags
        df['year'].replace({"<tt><pre>1982" : "1982"}, inplace=True)

        df['year'].astype('int64')
        df['week']=df['week'].astype(int)

    ###Змінюю індекси (25 з методички + Київ 26 та Севастополь 27)
        new_index={
            1:22,       #Черкаська
            2:24,       #Чернігівська
            3:23,       #Чернівецька
            4:25,       #Республіка Крим
            5:3,        #Дніпропетровська
            6:4,        #Донецька 
            7:8,        #Івано-Франківська
            8:19,       #Харківська 
            9:20,       #Херсонська
            10:21,      #Хмельницька
            11:9,       #Київська
            12:26,      #Київ
            13:10,      #Кіровоградська
            14:11,      #Луганська
            15:12,      #Львівська
            16:13,      #Миколаївська
            17:14,      #Одеська
            18:15,      #Полтавська
            19:16,      #Рівенська
            20:27,      #Севастополь
            21:17,      #Сумська
            22:18,      #Тернопільська
            23:6,       #Закарпатська
            24:1,       #Вінницька
            25:2,       #Волинська
            26:7,       #Запорізька
            27:5        #Житомирська
        }

        df=df.replace({"ID" : new_index})
        return df