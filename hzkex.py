import os
KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01] #[128, 64, 32, 16, 8, 4, 2, 1]
HZKFILE = os.path.dirname(os.path.abspath(__file__)) + os.sep + r"font/hzk16s"
from PIL import Image, ImageDraw, ImageFont, ImageFilter 
from random import randint

def gen_dot_character():    
    text = "娜"
    result = text.encode('gb2312').hex() #转为二进制, 显示为 b'\xc4\xc8'，参数为 gb2312 gbk是一样
    # result = gb2312.hex()
    
    # 根据编码计算该字在汉字库中的位置
    area = eval('0x' + result[:2]) - 0xA0 #前两位, 区号，从0开始
    index = eval('0x' + result[2:]) - 0xA0 #后两位，位号，从0开始
    offset = (94*(area-1) + (index-1)) * 32

    # 读取HZK16汉字库文件中该字数据
    with open(HZKFILE, 'rb') as f:
        f.seek(offset)
        font_rect = f.read(32)

    # 根据读取到的HZK中数据给我们的16*16点阵赋值
    rect_list = []
    rect_str_list = []
    for k in range(16):
        tmplst = []
        tmpstr = ""
        for j in range(2):
            asc = font_rect[k*2 + j]
            # print(asc, bin(asc), str(bin(asc)).replace("0b","").zfill(8))
            tmpstr += str(bin(asc)).replace("0b","").zfill(8)
            for i in range(8):
                flag = asc & KEYS[i]
                # print(flag, end="")
                tmplst.append(flag)
        print(tmplst)
        rect_str_list.append(tmpstr)
        rect_list.append(tmplst)

    # for row in rect_list:
    for row in rect_str_list:
        # print(row)
        for i in row:
            if i=="1":
            # if i:
                print('0',end="")
            else:
                print(".", end="")
        print()

def gen_dot_character_mod(text):    
    # text = "娜"
    result = text.encode('gb2312').hex() #转为十六制, 参数为 gb2312 gbk是一样
    # 根据编码计算该字在汉字库中的位置
    # area = eval('0x' + result[:2]) - 0xA0 #前两位, 区号，从0开始
    area = int(result[:2],16) - int("A0", 16)
    index = int(result[2:],16)- int("A0", 16)
    offset = (94*(area-1) + (index-1)) * 32

    # 读取HZK16汉字库文件中该字数据
    with open(HZKFILE, 'rb') as f:
        f.seek(offset)
        font_rect = f.read(32)

    # 根据读取到的HZK中数据给我们的16*16点阵赋值
    rect_str_list = []
    for k in range(16):
        first = font_rect[2*k]
        second = font_rect[2*k+1]
        tmpstr = str(bin(first)).replace("0b","").zfill(8)+str(bin(second)).replace("0b","").zfill(8)
        rect_str_list.append(tmpstr)
    
    return rect_str_list

    

def printSeveralHanZi():
    rect_info_all = [""]*16
    strHanZi = "春风又绿江南岸"
    for item in strHanZi:
        rect_str_list = gen_dot_character_mod(item)
        indx = 0
        for i_info in rect_str_list:
            rect_info_all[indx] += i_info
            indx += 1

    for row in rect_info_all:
        for i in row:
            if i=="1":
                print('■',end="")
            else:
                print("○", end="")
        print()
    pilex(rect_info_all)

def printSeveralHanZi2():    
    strHanZi = ["亲爱的娜","天天开心一"]
    rect_info_all = [""]*16*len(strHanZi)
    indx_jj = 0
    for ihanzi in strHanZi:
        for item in ihanzi:
            rect_str_list = gen_dot_character_mod(item)
            indx = 0
            for i_info in rect_str_list:
                rect_info_all[indx+16*indx_jj] += i_info
                indx += 1
        indx_jj += 1

    for row in rect_info_all:
        for i in row:
            if i=="1":
                print('■',end="")
            else:
                print("○", end="")
        print()
    pilex(rect_info_all)

def pilex(ceshi_str_lst):
    pixOne = 13
    height = len(ceshi_str_lst)
    width = len(ceshi_str_lst[0])
    for item in ceshi_str_lst:
        # print(len(item), '--')
        if width < len(item):
            width = len(item)
    width = width
    # print(height, width)
    width = pixOne * width
    height = pixOne * height
    image = Image.new('RGB', (width, height), (255,255,255))
    font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 30)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    
    # 输出文字:
    indx_j = 0
    for item in ceshi_str_lst:
        indx_i = 0        
        for i in item:
            if i=="1":
                draw.text((pixOne*indx_i, pixOne*indx_j), "■", font=font, fill=(randint(1,20),randint(1,20),randint(1,20)))
            else:
                draw.text((pixOne*indx_i, pixOne*indx_j), "○", font=font, fill=(150,150,150))
            indx_i += 1
        indx_j += 1

    # for t in range(4):
    #     draw.text((20 * t, 10), "8", font=font, fill=(0,0,0))

    # 模糊:
    # image = image.filter(ImageFilter.BLUR)
    image.save(os.path.dirname(os.path.abspath(__file__))+os.sep+'code.png', 'png')
    print("save successful!")


if __name__ == "__main__":
    # pilex()
    printSeveralHanZi2()

# # 初始化16*16的点阵位置，每个汉字需要16*16=256个点来表示
# # rect_list = []*16
# # rect_list = []
# # for i in range(16):
# #     rect_list.append([])

# rect_list = [[] for i in range(16)]
# text = "娜"
# # text = "中"

# # 获取中文编码
# gb2312 = text.encode('gb2312') #转为二进制, 显示为 b'\xc4\xc8'，参数为 gb2312 gbk是一样
# # hex_str = binascii.b2a_hex(gb2312) #转为十六进制，但是显示为二进制，‘娜’显示为 b'd4de'
# # result = str(hex_str, encoding="utf-8") #去掉前面的'b'显示, 'd4de'

# result = str(gb2312).replace('\\x', "").replace("b'","").replace("'", "") #将二进制数据清洗成4位字符
# # 根据编码计算“娜”在汉字库中的位置
# # 按照区位的顺序排列的。
# # 前一个字节为该汉字的区号，后一个字节为该字的位号。
# # 每一个区记录94个汉字，位号则为该字在该区中的位置。
# # DOS前辈们经过艰辛的努力，将制作好的字模放到了一个个标准的库中以免去后辈的麻烦，这就是点阵字库文件。
# # 一般我们使用16*16的点阵宋体字库，所谓16*16，是每一个汉字在纵、横各16点的区域内显示的。不过后来又有了HZK12、HZK24，HZK32和HZK48字库及黑体、楷体和隶书字库。虽然汉字库种类繁多，但都是按照区位的顺序排列的。前一个字节为该汉字的区号，后一个字节为该字的位号。每一个区记录94个汉字，位号则为该字在该区中的位置。
# # 因此，汉字在汉字库中的具体位置计算公式为：94*(区号-1)+位号-1。减1是因为数组是以0为开始而区号位号是以1为开始的。这仅为以汉字为单位该汉字在汉字库中的位置，那么，如何得到以字节为单位得到该汉字在汉字库中的位置呢？只需乘上一个汉字字模占用的字节数即可，即：(94*(区号-1)+位号-1)*一个汉字字模占用字节数，而按每种汉字库的汉字大小不同又会得到不同的结果。以16*16点阵字库为例，计算公式则为：(94*(区号-1)+(位号-1))*32。汉字库文该从该位置起的32字节信息即记录了该字的字模信息。
# area = eval('0x' + result[:2]) - 0xA0 #前两位, 区号，从0开始
# index = eval('0x' + result[2:]) - 0xA0 #后两位，位号，从0开始
# offset = (94*(area-1) + (index-1)) * 32

# font_rect = None

# import os
# # print(os.getcwd())
# # print(os.path.dirname(os.path.abspath(__file__)))
# HZKFILE = os.path.dirname(os.path.abspath(__file__)) + os.sep + "HZK16"
# # print(HZKFILE)
# # print(os.path.exists(HZKFILE))
# #读取HZK16汉字库文件中“娜”字数据
# with open(HZKFILE, 'rb') as f:
#     f.seek(offset)
#     font_rect = f.read(32)

# # 根据读取到的HZK中数据给我们的16*16点阵赋值
# for k in range(len(font_rect)//2):
#     row_list = rect_list[k]
#     for j in range(2):
#         for i in range(8):
#             asc = font_rect[k*2 + j]
#             flag = asc & KEYS[i]
#             row_list.append(flag)

# for row in rect_list:
#     for i in row:
#         if i:
#             print('0',end="")
#         else:
#             print(".", end="")
#     print()