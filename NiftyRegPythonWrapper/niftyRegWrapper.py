import os
import subprocess

class NiftyRegWarpper():

    def __init__(self,bin_path = ''):
        if bin_path == '':
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            bin_path = os.path.join(cur_dir,"win_bin")
        self.bin_path = bin_path

    # Block matching algorithm for global registration and can be used to get affine matrix
    # Please see the wiki to find how to use: http://cmictig.cs.ucl.ac.uk/wiki/index.php/Reg_aladin
    def reg_aladin(self,source_path, target_path,affine_path):
        args = [os.path.join(self.bin_path, 'reg_aladin'),
                                            '-ref', target_path,
                                            '-flo', source_path,
                                            '-aff', affine_path]
        p = subprocess.Popen(args)
        p.wait()

    # FFD registration, Fast Free-Form Deformation algorithm for non-rigid registration.
    # see: http://cmictig.cs.ucl.ac.uk/wiki/index.php/Reg_f3d
    def reg_f3d(self,source_path, target_path, warp_path = None, cpp_path = None):
        args = [os.path.join(self.bin_path, 'reg_f3d'),
                                            '-ref', target_path,
                                            '-flo', source_path,
                                            '-maxit','1000',
                                            '-ln','1']
        if warp_path != None:
            args.append('-res')
            args.append(warp_path)
        if cpp_path!=None:
            args.append('-cpp')
            args.append(cpp_path)
        print(args)
        p = subprocess.Popen(args)
        p.wait()
    
    # http://cmictig.cs.ucl.ac.uk/wiki/index.php/Reg_resample
    def reg_resample(self,source_path, target_path,cpp_path, warp_path,inter = '0'):
        args = [os.path.join(self.bin_path, 'reg_resample'),
                                            '-ref', target_path,
                                            '-flo', source_path,
                                            '-res', warp_path,
                                            '-trans', cpp_path,
                                            '-inter', inter]
        p = subprocess.Popen(args)
        p.wait()

    # http://cmictig.cs.ucl.ac.uk/wiki/index.php/Reg_transform
    def reg_transform(self,source_path, transform, disp):
        args = [os.path.join(self.bin_path, 'reg_transform'),
                                            '-ref', source_path,
                                            '-disp', transform, disp]
        p = subprocess.Popen(args)
        p.wait()