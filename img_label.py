import cv2
import numpy as np
import random
import glob

def draw_bbx(img, bbox):
    color = (255, 0, 0)
    cv2.line(img, tuple(bbox[0][::-1]), tuple(bbox[1][::-1]), color, 2)
    cv2.line(img, tuple(bbox[1][::-1]), tuple(bbox[2][::-1]), color, 2)
    cv2.line(img, tuple(bbox[2][::-1]), tuple(bbox[3][::-1]), color, 2)
    cv2.line(img, tuple(bbox[3][::-1]), tuple(bbox[0][::-1]), color, 2)
    pass

def Write_Text(file_name,contant):
    with open(file_name,"a+") as f:
        f.writelines(contant)
        f.writelines("\n")

def cal_connected(img):
    num_TCBP, label_TCBP = cv2.connectedComponents(img)
    bbox = []

    for i in range(1, num_TCBP ):
        cnt = np.argwhere(label_TCBP == i)
        rect = cv2.minAreaRect(cnt) #求最小外接矩形
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        bbox.append(box)
        print(bbox)
    return bbox


img_list=glob.glob('./ts/*')
for img_path in img_list:
    name = img_path.split('/')[-1].split('.')[0]
    yuantu = cv2.imread('./img/'+name+'.jpg')
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    bbbox = cal_connected(img)
    annotations=[]
    for bbox in bbbox:

        # x,y,w,h,a1,a2,a3,a4,r
        h,w = bbox[:,0].max()-bbox[:,0].min(),bbox[:,1].max()-bbox[:,1].min()

        y,x = h//2+bbox[:,0].min(),w//2+bbox[:,1].min()
        cv2.circle(yuantu, tuple((x,y)), 4, (125, 125, 255), thickness=4)

        #目标框,逆时针,a1为,上边点到左边长度,a2右边点到上边长度,a3下边点到右边长度,a4左边点到下边长度
        a1 = (bbox[np.where(bbox[:,0]==bbox[:,0].min())][0][1]-bbox[:,1].min())/w
        a2 = (bbox[np.where(bbox[:,1]==bbox[:,1].min())][0][0]-bbox[:,0].min())/h
        a3 = (bbox[:,1].max()-bbox[np.where(bbox[:,0]==bbox[:,0].max())][0][1])/w
        a4 = (bbox[:,0].max()-bbox[np.where(bbox[:,1]==bbox[:,1].max())][0][0])/h

        v1 = bbox[np.where(bbox[:,0]==bbox[:,0].min())][0]
        v2 = bbox[np.where(bbox[:,1]==bbox[:,1].min())][0]
        v3 = bbox[np.where(bbox[:,0]==bbox[:,0].max())][0]
        v4 = bbox[np.where(bbox[:,1]==bbox[:,1].max())][0]

        cv2.circle(yuantu, tuple(v1[::-1]), 2, (0, 0, 255), thickness=4)
        cv2.circle(yuantu, tuple(v2[::-1]), 2, (0, 0, 255), thickness=4)
        cv2.circle(yuantu, tuple(v3[::-1]), 2, (0, 0, 255), thickness=4)
        cv2.circle(yuantu, tuple(v4[::-1]), 2, (0, 0, 255), thickness=4)

        x_min,x_max,y_min,y_max = bbox[:,1].min(),bbox[:,1].max(),bbox[:,0].min(),bbox[:,0].max()
        b1,b2,b3,b4 = (y_min,x_min),(y_max,x_min),(y_max,x_max),(y_min,x_max)

        draw_bbx(yuantu,[b1,b2,b3,b4])

        cv2.imwrite('./'+name+'.jpg',yuantu)

        x1,y1 ,x2,y2= bbox[:,1].min(),bbox[:,0].min(),bbox[:,1].max(),bbox[:,0].max()

        annotation = [x1,y1,x2,y2,a1,a2,a3,a4,juguang,0]
        annotations=annotations+annotation

        file_name = img_path.split('/')[-1].split('.')[0]+'.txt'

        Write_Text(file_name,np.str(annotations).strip('[]'))
