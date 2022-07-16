# MedicalImageScriptDemo
## Description
Some simple medical image processing python script. Wish these code can help you.

[Chinese Blog](https://www.cnblogs.com/WAoyu/tag/%E5%8C%BB%E5%AD%A6%E5%BD%B1%E5%83%8F/)

## Category
### 1. raw2mha
Raw volume data to mha format.
### 2. mha2jpg
Mha volume data to jpg slice. 
### 3. resample
Resample volume to specified physical size.

### 4. lungSeg
Use traditional image processing method to get lung mask from thoracic volume.

<img src = "lungSeg/seg.jpg">

### 5. hairRemoval
Use traditional image processing to remove hair from skin image.

<img src = "hairRemoval/show.jpg">

### 6. readDicom
Read dicom and visualization.

<img src = "readDicom/show.jpg">

### 7. volumeRenderingQT
Volume rendering by using VTK, UI by using PyQT5

<img src = "volumeRenderingQT/bone.jpg" width="45%">
<img src = "volumeRenderingQT/lung.jpg" width="45%">

### 8. NiftyRegPythonWrapper
NiftyReg is a nice medical image registration tools, see: http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftyReg

Sometimes, we want to do batch operation, we can use python to control the process. I have already built a NiftyReg in windows platform, the bin files are in the win_bin.

### 9. Nonfinite-modality data augmentation for brain image registration
This is our published paper for brain image registration. We synthesize some "brain" image to augment the exist deep learning-based brain image registration method. Please see: https://doi.org/10.1016/j.compbiomed.2022.105780 and the relative repo is https://github.com/MangoWAY/SMIBID_BrainRegistration

### 10. Hierarchical anatomical structure-aware based thoracic CT images registration
This is our published paper for thoracic CT images registration. We used the structure-aware based strategy and FFD-based framework to register the thoracic CT images. Please see: https://doi.org/10.1016/j.compbiomed.2022.105876 and the relative repo is https://github.com/heluxixue/Structure_Aware_Registration
## Useful resources

1. Use Deep learning method to segment lung, it is a good work can be directly used to your data. see: https://github.com/JoHof/lungmask

2. If you want to get some test data, you can see: https://www.dicomlibrary.com/ download dicom data, and convert to any format.

3. A very nice medical image processing,visualization software, ``3DSlicer``: https://www.slicer.org/

4. A nice biomedical imaging competition site, you can find a lot of medical dataset: https://grand-challenge.org/

5. If you work on thoracic volume (lung), you can use Dir-lab data: https://med.emory.edu/departments/radiation-oncology/research-laboratories/deformable-image-registration/index.html

6. If you study in medical image registration, for modern implement (auto-diff and GPU speed-up), use Air-lab: https://github.com/airlab-unibas/airlab

## Cite
If you think my work can help, you can cite my work. ♥️
```
@software{Aoyu_Medical_Image_Script,
  author = {Wang, Aoyu},
  month = {5},
  title = {{Medical Image Script Demo}},
  url = {https://github.com/MangoWAY/medicalImageScriptDemo},
  version = {0.1},
  year = {2022}
}

```
For paper
```
@article{HE2022105780,
title = {Nonfinite-modality data augmentation for brain image registration},
journal = {Computers in Biology and Medicine},
volume = {147},
pages = {105780},
year = {2022},
issn = {0010-4825},
doi = {https://doi.org/10.1016/j.compbiomed.2022.105780},
url = {https://www.sciencedirect.com/science/article/pii/S0010482522005479},
author = {Yuanbo He and Aoyu Wang and Shuai Li and Yikang Yang and Aimin Hao},
keywords = {Nonfinite-modality, Data augmentation, Improved 3D VAE, Brain image registration}
}
```
```
@article{HE2022105876,
  title = {Hierarchical anatomical structure-aware based thoracic CT images registration},
  journal = {Computers in Biology and Medicine},
  pages = {105876},
  year = {2022},
  issn = {0010-4825},
  doi = {https://doi.org/10.1016/j.compbiomed.2022.105876},
  url = {https://www.sciencedirect.com/science/article/pii/S001048252200628X},
  author = {Yuanbo He and Aoyu Wang and Shuai Li and Aimin Hao},
  keywords = {Thoracic CT registration, Anatomical structure-aware strategy, Deformation ability-aware dissimilarity metric, Motion pattern-aware regularization, A novel hierarchical strategy}
  }
```
