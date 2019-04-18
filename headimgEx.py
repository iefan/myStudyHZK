import os
import itchat
from PIL import Image, ImageDraw, ImageFont, ImageFilter 
HZKFILE = os.path.dirname(os.path.abspath(__file__)) + os.sep + r"font/hzk16s"
from hzkex import gen_dot_character_mod
from random import randint, sample

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
    width = 40
    height = 40
    image_w = width * 15
    image_h = height * 15
    base_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'headImages1'
    image = Image.new('RGB', (image_w, image_h), (200,200,200))
    # 创建Draw对象:
    # draw = ImageDraw.Draw(image)
    pos_x = 0
    pos_y = 0
    for indx in range(15*15):
        im = Image.open(base_path + os.sep + str(indx+1) + ".jpg")
        thumb = im.resize((width,height), Image.ANTIALIAS)
        i_row = indx % 15
        i_col = indx // 15
        pos_x = i_row * width
        pos_y = i_col * height
        print(indx, (pos_x,pos_y,pos_x+width,pos_y+height))
        image.paste(thumb, (pos_x,pos_y,pos_x+width,pos_y+height))
    image.save(os.path.dirname(os.path.abspath(__file__))+os.sep+'code1.png', 'png')

def makeFontImg(text="赞"):
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

if __name__ == "__main__":
    genNineFonts()
    # makeFontImg()
    # makeImg()
    # scanHeadImg()