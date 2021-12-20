import os
import pandas as pd

# 14109344 성연석

# 먼저 중복된 이름의 파일들이 많아 이름을 받아와
file_path1 = "C:/Users/TFG242/Desktop/data/Face Mask Dataset/temp/Validation/WithMask"
file_path2 = "C:/Users/TFG242/Desktop/data/Face Mask Dataset/temp/Validation/WithoutMask"
file_list_withmask = os.listdir(file_path1)
file_list_nomask = os.listdir(file_path2)


# 이를 모두 다른 이름으로 변경, 각 dat set의 이름 + 번호로 식별
i = 1
for name in file_list_withmask: 
    src = os.path.join(file_path1, name)
    dst = (f"Validation{i}.jpg")
    dst = os.path.join(file_path1, dst)
    os.rename(src, dst)
    i += 1

for name in file_list_nomask:
    src = os.path.join(file_path2, name)
    dst = (f"Validation{i}.jpg")
    dst = os.path.join(file_path2, dst)
    os.rename(src, dst)
    i += 1

# 각 data set 마다 label을 주고 csv 파일로 저장
first_list = [ (14109344, '성연석')] # append를 바로 할 수 없어 초기값 설정
train = pd.DataFrame(first_list, columns= ['Image_id', 'With_mask']) #파일이름, 마스크를 썼으면 label에 1, 안썼으면 0

for title in file_list_withmask :
    train = train.append({'Image_id' : title, 'With_mask' : int(1)}, ignore_index=True)

for title in file_list_nomask :
    train = train.append({'Image_id' : title, 'With_mask' : int(0)}, ignore_index=True)

train = train.drop(index=0, axis=0) # 첫번째 example 행 삭제
train =train.set_index("Image_id") # 인덱스 대체

train.to_csv('C:/Users/TFG242/Desktop/data/Face Mask Dataset/temp/Validation.csv')