from PIL import Image, ImageFont

from handright import Template, handwrite


#设置颜色
color_dic = {'black': (0, 0, 0, 255),
             'brown': (154, 141, 65, 255)}

#设置格式
siz_dic = {'whole': (3300,2048),
            'half': (2450,2048)}

# ----------------放入文字--------------------#

text_list = ['Add 5mL of DMSO via a pipette and a stir bar',
             'Heat the flask on mantle and reflux for 5min',
             'Remove the flask from hot plate and cool for 10min, room temperature',
             'Reduce the volume of the solvent in vacuum at 60-70 C before addition of acetone',
             'Transfer the solution to a 50mL beaker ',

             ]

# \n 换行转义符'Add 30mL of acetone ',
#              'Allow the beaker to stand for at least 15min',
#              'Collect the yellow precipitate and wash with small amounts of \n'
#              'Acetone (2mL 3) and Diethyl ether (2mL 3)',
#              'Suction dry and then air-dry the solid'

#-------------选择颜色------------------#

color_index = color_dic['black']

#-----------选择格式--------------#

siz = siz_dic['half']

# -------------删除所有带temp的png文件--------------#
import os

def delete_output_pngs():
    # 获取当前目录下的所有文件
    for file in os.listdir('.'):
        # 检查文件名是否包含'output'且扩展名为'.png'
        if 'output' in file and file.endswith('.png'):
            full_path = os.path.join(os.getcwd(), file)
            print(f"Deleting file: {full_path}")
            os.remove(full_path)  # 删除文件

# 调用函数
delete_output_pngs()

# ------------------设置参数------------------------#

template = Template(
    background=Image.new(mode="1", size = siz, color=1),
    font=ImageFont.truetype("font\MyFont.ttf", size=125),
    line_spacing=125,
    fill=0,  # 字体“颜色”
    left_margin=10,
    top_margin=10,  # coding: utf-8

    right_margin=10,
    bottom_margin=10,
    word_spacing=-10,
    line_spacing_sigma=0,  # 行间距随机扰动
    font_size_sigma=1,  # 字体大小随机扰动
    word_spacing_sigma=0.1,  # 字间距随机扰动
    start_chars="“（[<",  # 特定字符提前换行，防止出现在行尾
    end_chars="，。",  # 防止特定字符因排版算法的自动换行而出现在行首
    perturb_x_sigma=1,  # 笔画横向偏移随机扰动
    perturb_y_sigma=1,  # 笔画纵向偏移随机扰动
    perturb_theta_sigma=0.05,  # 笔画旋转偏移随机扰动
)

# -------------开始循环--------------------#

for j in range(len(text_list)):

    images = handwrite(text_list[j], template)

    for i, im in enumerate(images):
        assert isinstance(im, Image.Image)
        # im.show()
        im.save("temp.png".format(i))

    image = Image.open("temp.png")

    image = image.convert("RGBA")

    data = image.getdata()

    new_data = []  # 创建一个新图像数据列表，存放抠图后仅剩的像素

    for item in data:
        # 检查像素是否为白色
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            # 将白色像素替换为透明
            new_data.append((255, 255, 255, 0))

        else:
            # 将黑色像素替换为彩色
            new_data.append(color_index)



    image.putdata(new_data)  # 更新图像数据


    image.save(f'output{j}.png')