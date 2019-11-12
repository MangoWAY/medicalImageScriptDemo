import SimpleITK as itk
import numpy as np


vec = itk.ReadImage("vec.mha")
vec:np.ndarray = itk.GetArrayFromImage(vec)


case10T00 = np.loadtxt("case10_dirLab300_T00_xyz.txt")
case10T50 = np.loadtxt("case10_dirLab300_T50_xyz.txt")
# f+v-m

sum = 0


for i in range(300):
    F = case10T00[i].astype('int')
    M = case10T50[i].astype('int')
    V = vec[F[2]][F[1]][F[0]]
    V[0] =V[0]/0.97
    V[1] =V[1]/0.97
    V[2] =V[2]/2.5
    print(F,M,V)
    sum = sum+ np.linalg.norm((F+V-M))
print(sum/300)

"""
f = itk.ReadImage("case10_T00.img.mha")
m = itk.ReadImage("case10_T50.img.mha")
w = itk.ReadImage("warpcase10.mha")
"""
def deal():
    rootdir = "E:\\1CTdata\\dirlab\\4DCT\\Case10Pack\\Images"
    mhadir = ""
    if not os.path.exists(os.path.join(rootdir,"mha")):
        mhadir = os.path.join(rootdir,"mha")
        os.makedirs(mhadir)
    for i in range(10):
        raw = "case10_T%s0.img"%str(i)
        raw2mha(os.path.join(rootdir,raw),os.path.join(mhadir,raw+".mha"),(120,512,512),(0.97,0.97,2.5))