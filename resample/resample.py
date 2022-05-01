import SimpleITK as sitk
"""
resample
"""

def resampleVolume(outspacing,vol):
    """
    resample volume to different spacing size\n
    paras：
    outpacing：spacing size，such as [1,1,1]
    vol：sitk image\n
    return：resampled volume
    """
    outsize = [0,0,0]
    inputspacing = 0
    inputsize = 0
    inputorigin = [0,0,0]
    inputdir = [0,0,0]

    #read
    
    inputsize = vol.GetSize()
    inputspacing = vol.GetSpacing()

    transform = sitk.Transform()
    transform.SetIdentity()
    #calculate out size
    outsize[0] = int(inputsize[0]*inputspacing[0]/outspacing[0] + 0.5)
    outsize[1] = int(inputsize[1]*inputspacing[1]/outspacing[1] + 0.5)
    outsize[2] = int(inputsize[2]*inputspacing[2]/outspacing[2] + 0.5)

    #out parameters
    resampler = sitk.ResampleImageFilter()
    resampler.SetTransform(transform)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetOutputOrigin(vol.GetOrigin())
    resampler.SetOutputSpacing(outspacing)
    resampler.SetOutputDirection(vol.GetDirection())
    resampler.SetSize(outsize)
    newvol = resampler.Execute(vol)
    return newvol

    

def main():
    #read
    vol = sitk.Image(sitk.ReadImage("input.mha"))

    #resample
    newvol = resampleVolume([1,1,1],vol)

    #write
    wriiter = sitk.ImageFileWriter()
    wriiter.SetFileName("output.mha")
    wriiter.Execute(newvol)