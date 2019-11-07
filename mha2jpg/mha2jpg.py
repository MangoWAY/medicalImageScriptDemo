import SimpleITK as sitk
import numpy as np
import cv2
import os

def mha2jpg(mhaPath,outFolder,windowsCenter,windowsSize):
    
    """
    The function can output a group of jpg files by a specified mha file.
    Args:
        mhaPath:mha file path.
        outfolder:The folder that the jpg files are saved.
        windowsCenter:the CT windows center.
        windowsSize:the CT windows size.
    Return:void

    """
    image = sitk.ReadImage(mhaPath)
    img_data = sitk.GetArrayFromImage(image)
    channel = img_data.shape[0]

    if not os.path.exists(outFolder):
        os.makedirs(outFolder)


    low = windowsCenter-windowsSize/2
    high = windowsCenter+windowsSize/2

    for s in range(channel):
        slicer = img_data[s,:,:]
        slicer[slicer<low] = low
        slicer[slicer>high] = high
        slicer = slicer-low
        img = cv2.normalize(slicer, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        cv2.imwrite(os.path.join(outFolder,str(s)+'.jpg'),img)

def main():
    mha = input("Enter the mha path:")
    out = input("Enter the out folder:")
    wc = int(input("Enter the windows center:"))
    ws = int(input("Enter the windows size:"))
    mha2jpg(mha,out,wc,ws)

if __name__ == "__main__":
    main()








