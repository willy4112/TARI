# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 10:35:12 2022

@author: CCW
"""

import os
import PIL.Image as Image

def resize_by_width(infile, image_size):
    im = Image.open(infile)
    (x, y) = im.size
    lv = round(x / image_size,2) + 0.01
    x_s = int(x // lv)
    y_s = int(y // lv)
    print('x_s', x_s, y_s)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    return out

def get_new_img_xy(infile, image_size):
    im = Image.open(infile)
    (x,y) = im.size
    lv = round(x / image_size,2) + 0.01
    x_s = x // lv
    y_s = y // lv
    return x_s, y_s

def image_compose(image_colnum, image_size, image_rownum, image_names, image_save_path, x_new, y_new):
    to_image = Image.new('RGB', (image_colnum*x_new, image_rownum*y_new))
    total_num = 0
    for y in range(1, image_rownum+1):
        for x in range(1, image_colnum+1):
            from_image = resize_by_width(image_names[image_colnum*(y-1)+x-1], image_size)
            to_image.paste(from_image, ((x-1)*x_new,(y-1)*y_new))
            total_num += 1
            if total_num == len(image_names):
                break
    return to_image.save(image_save_path)

def get_image_list_fullpath(dir_path):
    file_name_list = os.listdir(dir_path)
    image_fullpath_list = []
    for file_name_one in file_name_list:
        file_one_path = os.path.join(dir_path, file_name_one)
        if os.path.isfile(file_one_path):
            image_fullpath_list.append(file_one_path)
        else:
            img_path_list = get_image_list_fullpath(file_one_path)
            image_fullpath_list.extend(img_path_list)
    return image_fullpath_list

def merge_images(image_dir_path, image_size, image_colnum):
    image_fullpath_list = get_image_list_fullpath(image_dir_path)
    print('image_fullpath_list', len(image_fullpath_list),image_fullpath_list)
    
    image_save_path = r'{}.jpg'.format(image_dir_path)
    image_rownum_yu = len(image_fullpath_list) % image_colnum
    if image_rownum_yu == 0:
        image_rownum = len(image_fullpath_list) // image_colnum
    else:
        image_rownum = len(image_fullpath_list) // image_colnum + 1
    
    x_list = []
    y_list = []
    for img_file in image_fullpath_list:
        img_x, img_y = get_new_img_xy(img_file, image_size)
        x_list.append(img_x)
        y_list.append(img_y)
    
    print('x_list', sorted(x_list))
    print('y_list', sorted(y_list))
    x_new = int(x_list[len(x_list) // 5 * 4])
    y_new = int(y_list[len(y_list) // 5 * 4])
    print('x_new','y_new',x_new,y_new)
    image_compose(image_colnum, image_size, image_rownum, image_fullpath_list, image_save_path, x_new, y_new)

if __name__ == '__main__':
    # 要合併的圖集資料夾
    image_dir_path = r'E:\下載\MAIZSIM WEA\wea file\addH2O\rcp45_norESM1-M\秋作'
    # 個別小圖的大小
    image_size = 128
    # 一row有幾個
    image_colnum = 10
    merge_images(image_dir_path, image_size, image_colnum)
