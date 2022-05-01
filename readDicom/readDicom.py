import SimpleITK as sitk
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

#https://www.dicomlibrary.com/ 
#本文从上述网站下载的dicom是一个序列有300+切片数据
dicomdir = "Dataset/dicom/data1/series-00000"
reader = sitk.ImageSeriesReader()

dicom_names = reader.GetGDCMSeriesFileNames(dicomdir)
reader.SetFileNames(dicom_names)

image = reader.Execute()

size = image.GetSize()
print("Image size:", size[0], size[1], size[2])

rawImg = sitk.GetArrayFromImage(image)
print("Max value:",np.max(rawImg),"Min value:",np.min(rawImg),rawImg.shape)

#以上代码成功读取了dicom序列文件，下面可视化几个切片看看
imgslicer = []
for i in range(4):
    #拓展维度，为了可视化
    s = np.expand_dims(rawImg[i*70,:,:],2)
    #增加通道
    s = np.repeat(s,3,2)
    #这里进行归一化，因为dicom这里有3000个level所以归一化肯定会丢失精度
    #一般的做法是给定一个区间，再归一化，其他区域就不管了，这个叫开窗
    print(s.shape)
    s = s.astype(np.float32)
    s = (s - np.min(s))/(np.max(s) - np.min(s))
    imgslicer.append(s)

# rawImg = rawImg.transpose((1,2,0))
# rawImg = np.repeat(rawImg,3,2)
# print("Max value:",np.max(rawImg),"Min value:",np.min(rawImg),rawImg.shape)
for i in range(4):
    plt.subplot(1,4,i+1)
    plt.imshow(imgslicer[i])