import cv2
def DHR(imgpath,outpath):
    
    src = cv2.imread(imgpath)
    grayScale = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY )
    cv2.imwrite("grey.jpg",grayScale)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(10,10))
    blackhat = cv2.morphologyEx(grayScale, cv2.MORPH_BLACKHAT, kernel)
    cv2.imwrite("blackhat.jpg",blackhat)
    ret,thresh2 = cv2.threshold(blackhat,10,255,cv2.THRESH_BINARY)
    cv2.imwrite("threshold.jpg",thresh2)
    dst = cv2.inpaint(src,thresh2,1,cv2.INPAINT_TELEA)
    cv2.imwrite(outpath, dst, [int(cv2.IMWRITE_JPEG_QUALITY), 100])