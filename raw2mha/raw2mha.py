import SimpleITK as itk
import numpy as np
import os



def raw2mha(inpath,outpath,size,spacing,intype='uint16',outtype='uint16'):
    """
    parameter:
    inpath:raw file path
    outpath:raw out file path
    size:raw file size(z,y,x) such as (94,256,256)
    spacing:raw file pixel spacing.
    intype:raw file data type,default is uint16
    """
    data = np.fromfile(inpath,dtype=intype)
    data = data.reshape(size)
    data = data.astype(outtype)
    img:itk.Image = itk.GetImageFromArray(data)
    img.SetSpacing(spacing)
    s = itk.ImageFileWriter()
    s.SetFileName(outpath)
    s.Execute(img)



def main():
    filepath = "test.raw"
    datatype = 'uint16'
    size = (94,256,256)
    spacing = (0.97,0.97,2.5)
    outname = "test.mha"
    raw2mha(filepath,outname,size,spacing,datatype)



    
if __name__ == "__main__":
    main()




