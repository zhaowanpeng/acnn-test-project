# -*- coding:utf-8 -*-
import sys
# sys.path.append("../../../../common")
# sys.path.append("../")
import os
import numpy as np
import acl
import atlas_utils.utils as utils
from PIL import Image, ImageDraw, ImageFont
from atlas_utils.acl_dvpp import Dvpp
import atlas_utils.constants as const
from atlas_utils.acl_model import Model
from atlas_utils.acl_image import AclImage
from atlas_utils.acl_resource import AclResource

MODEL_WIDTH = 64
MODEL_HEIGHT = 64

def pre_process(image, dvpp):
    """preprocess"""
    image_input = image.copy_to_dvpp()
    yuv_image = dvpp.jpegd(image_input)
    print("decode jpeg end")
    resized_image = dvpp.crop_and_paste(yuv_image, image.width, image.height, MODEL_WIDTH, MODEL_HEIGHT)
    print("resize yuv end")
    return resized_image

def main():

    acl_resource = AclResource()
    acl_resource.init()
    model = Model("../model/hwmodel.om")
    dvpp = Dvpp(acl_resource)

    imgs = os.listdir("../data/")

    for imgname in imgs:
        image_file="../data/"+imgname
        print(image_file)
        image = AclImage(image_file)
        resized_image = pre_process(image, dvpp)
        result = model.execute([resized_image,])
        print(result)



if __name__ == '__main__':
    main()