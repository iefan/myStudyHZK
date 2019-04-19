import os
import itchat
from PIL import Image, ImageDraw, ImageFont, ImageFilter 
HZKFILE = os.path.dirname(os.path.abspath(__file__)) + os.sep + r"font/hzk16s"
from hzkex import gen_dot_character_mod
from random import randint, sample
import cv2
import numpy as np

def readHeadImg():
    base_path = 'headImages'
    itchat.auto_login()
    friend_list = itchat.get_friends(update=True)
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    for friend in friend_list:
        img_data = itchat.get_head_img(userName=friend['UserName'])  # 获取头像数据
        img_name = friend['RemarkName'] if friend['RemarkName'] != '' else friend['NickName'] #if语句为真时取前面的值
        img_file = os.path.join(base_path, img_name + '.jpg') #拼接路径
        print(img_file)
        try:
            with open(img_file, 'wb') as file:
                file.write(img_data)
        except:
            pass
    itchat.logout()

def scanHeadImg():
    base_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'headImages1'
    indx = 0
    for root, _, files in os.walk(base_path):
        # print("====", root, files)
        for filename in files:
            indx += 1
            newfile = base_path + os.sep + str(indx)+".jpg"
            os.rename(os.path.join(root, filename),newfile)
            # print(filename)
            # print(os.path.join(root, filename))
            # print(newfile)

def makeImg(): 
    pixSize = 16   
    width = 40
    height = 40
    image_w = width * pixSize
    image_h = height * pixSize
    base_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'headImages1'
    image = Image.new('RGB', (image_w, image_h), (200,200,200))
    # 创建Draw对象:
    # draw = ImageDraw.Draw(image)
    pos_x = 0
    pos_y = 0
    for indx in range(pixSize*pixSize):
        im = Image.open(base_path + os.sep + str(indx+1) + ".jpg")
        thumb = im.resize((width,height), Image.ANTIALIAS)
        i_row = indx % pixSize
        i_col = indx // pixSize
        pos_x = i_row * width
        pos_y = i_col * height
        print(indx, (pos_x,pos_y,pos_x+width,pos_y+height))
        image.paste(thumb, (pos_x,pos_y,pos_x+width,pos_y+height))
    image.save(os.path.dirname(os.path.abspath(__file__))+os.sep+'code1.png', 'png')

def makeFontImg(text="福"):
    # text = "有"
    rect_list = gen_dot_character_mod(text)
    # print(rect_list)
    # ceshi_str_lst = [rect_list,]
    imgcount = 0
    for item in rect_list:
        imgcount += item.count('1')

    imgNumList = sample(range(1,261), imgcount)
    

    rows_img_num = 16
    width = 40
    height = 40
    image_w = width * rows_img_num
    image_h = height * rows_img_num
    base_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'headImages1'
    image = Image.new('RGB', (image_w, image_h), (randint(161,255),randint(161,255),randint(161,255)))
    # 创建Draw对象:
    # draw = ImageDraw.Draw(image)
    
    # 输出文字:
    indx = 0
    icount = 0
    for irow in rect_list:
        for i in irow:
            if i=="1":
                # im = Image.open(base_path + os.sep + str(indx+1) + ".jpg")
                im = Image.open(base_path + os.sep + str(imgNumList[icount]) + ".jpg")
                thumb = im.resize((width,height), Image.ANTIALIAS)
                i_row = indx % rows_img_num
                i_col = indx // rows_img_num
                pos_x = i_row * width
                pos_y = i_col * height
                # print(pos_x,pos_y,pos_x+width,pos_y+height)
                image.paste(thumb, (pos_x,pos_y,pos_x+width,pos_y+height))
                icount += 1
            indx += 1
    
    image.save(os.path.dirname(os.path.abspath(__file__))+os.sep+ text +'.png', 'png')
    print(text, 'over')

def genNineFonts():
    strlsg = "有你们的日子真好！"
    for itext in strlsg:
        makeFontImg(itext)


def makeFontImg_cv():
    base_path = os.path.dirname(os.path.abspath(__file__))
    img_bg = cv2.imread(base_path + os.sep + "code1.png")

    img1 = np.zeros_like(img_bg)    # 创建画布
    img1.fill(255)
    # 252,236,239
    # print(len(img1), len(img1[0]), len(img1[0]))
    for i in range(img_bg.shape[0]):
        for j in range(img_bg.shape[1]):
            img1[i][j] = [252,236,239]            
    # for item in img1:
    #     for j_item in item:
    #         j_item = [252,236,239]
    #         # print(j_item[0], len(j_item))
    # print(img1)
    img2 = cv2.imread(base_path + os.sep + "me.jpg")
    img2 = cv2.resize(img2, (200,200), interpolation=cv2.INTER_AREA) #设置为同样大小
    
    # 把logo放在中心区域
    # 计算画面中心区域
    center_x, center_y = img1.shape[:2]
    rows, cols = img2.shape[:2]
    center_posx = (center_x-rows)//2
    center_posy = (center_y-cols)//2
    roi = img1[center_posx:center_posx+rows, center_posy:center_posy+cols]
    # print(rows, cols, type(roi),img1.shape)

    # 创建掩膜
    img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # 保留除logo外的背景
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    dst = cv2.add(img1_bg, img2)  # 进行融合
    img1[center_posx:center_posx+rows, center_posy:center_posy+cols] = dst  # 融合后放在原图上

    
    # cv2.imshow('img_add',img1)

    dst = cv2.addWeighted(img1, 0.7, img_bg, 0.3, 0)    
    cv2.imshow('img_add',dst)
    # cv2.namedWindow('addImage')
    cv2.waitKey()
    cv2.destroyAllWindows()
    # print(dst)
    


if __name__ == "__main__":
    makeFontImg_cv()
    # genNineFonts()
    # makeFontImg()
    # makeImg()
    # scanHeadImg()