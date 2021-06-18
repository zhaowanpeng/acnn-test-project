### AIPP模板

```
# AIPP的配置以aipp_op开始，标识这是一个AIPP算子的配置，aipp_op支持配置多个
aipp_op {
#========================= 全局设置（start） ===========================
# aipp_mode指定了AIPP的模式，必须配置
# 类型：enum
# 取值范围：dynamic/static，dynamic 表示动态AIPP，static 表示静态AIPP
# aipp_mode: 

# related_input_rank参数为可选，标识对模型的第几个输入做AIPP处理，从0开始，默认为0。例如模型有两个输入，需要对第2个输入做AIPP，则配置related_input_rank为1。
# 类型: 整型
# 配置范围 >= 0
# related_input_rank: 0
 
#========================= 全局设置（end） =============================

#========================= 动态AIPP需设置，静态AIPP无需设置（start） ======
# 输入图像最大的size，动态AIPP必须配置（如果为动态batch场景，N为最大档位数的取值）
# 类型：int
# max_src_image_size: 0
# 若输入图像格式为YUV400_U8，则max_src_image_size>=N * src_image_size_w * src_image_size_h * 1。
# 若输入图像格式为YUV420SP_U8，则max_src_image_size>=N * src_image_size_w * src_image_size_h * 1.5。
# 若输入图像格式为XRGB8888_U8，则max_src_image_size>=N * src_image_size_w * src_image_size_h * 4。
# 若输入图像格式为RGB888_U8，则max_src_image_size>=N * src_image_size_w * src_image_size_h * 3。

# 是否支持旋转，保留字段，暂不支持该功能
# 类型：bool
# 取值范围：true/false，true表示支持旋转，false表示不支持旋转
# support_rotation: false
#========================= 动态AIPP需设置，静态AIPP无需设置（end） =======

#========================= 静态AIPP需设置，动态AIPP无需设置 （start）======
# 输入图像格式，可选
# 类型: enum
# 取值范围：YUV420SP_U8、XRGB8888_U8、RGB888_U8、YUV400_U8
# input_format :
# 说明：模型转换完毕后，在对应的*.om模型文件中，上述参数分别以1、2、3、4枚举值呈现。

# 原始图像的宽度、高度
# 类型：int32
# 取值范围 & 约束：宽度取值范围为[2,4096]或0；高度取值范围为[1,4096]或0，对于YUV420SP_U8类型的图像，要求原始图像的宽和高取值是偶数
# src_image_size_w :0
# src_image_size_h :0
# 说明：请根据实际图片的宽、高配置src_image_size_w和src_image_size_h；只有crop，padding功能都没有开启的场景，src_image_size_w和src_image_size_h才能取值为0或不配置，该场景下会取网络模型输入定义的w和h，并且网络模型输入定义的w取值范围为[2,4096]，h取值范围为[1,4096]。
# C方向的填充值，保留字段，暂不支持该功能
# 类型： float16
# 取值范围：[-65504, 65504]
# cpadding_value :0.0

#========= crop参数设置（配置样例请参见AIPP配置 > Crop/Padding配置说明） =========
# AIPP处理图片时是否支持抠图
# 类型：bool
# 取值范围：true/false，true表示支持，false表示不支持
# crop :false

# 抠图起始位置水平、垂直方向坐标，抠图大小为网络输入定义的w和h
# 类型：int32
# 取值范围 & 约束： [0,4095]、对于YUV420SP_U8类型的图像，要求取值是偶数
# 说明：load_start_pos_w<src_image_size_w，load_start_pos_h<src_image_size_h
# load_start_pos_w :0
# load_start_pos_h :0

# 抠图后的图像size
# 类型：int32
# 取值范围 & 约束： [0,4096]、load_start_pos_w + crop_size_w <= src_image_size_w、load_start_pos_h + crop_size_h <= src_image_size_h
# crop_size_w :0
# crop_size_h :0
说明：若开启抠图功能，并且没有配置padding，该场景下crop_size_w和crop_size_h才能取值为0或不配置，此时抠图大小（crop_size[W|H]）的宽和高取值来自模型文件--input_shape中的宽和高，并且--input_shape中的宽和高取值范围为[1,4096]。

# 抠图约束如下：
# 若input_format取值为YUV420SP_U8，则crop_size_w、crop_size_h、load_start_pos_w、load_start_pos_h必须为偶数。
# 若input_format取值为其他值，对crop_size_w、crop_size_h、load_start_pos_w、load_start_pos_h无约束。
# 若开启抠图功能，则src_image_size[W|H] >= crop_size[W|H]+load_start_pos[W|H]。


#================================== resize参数设置 ================================
# AIPP处理图片时是否支持缩放，保留字段，暂不支持该功能
# 类型：bool
# 取值范围：true/false，true表示支持，false表示不支持
resize :false
 
# 缩放后图像的宽度和高度，保留字段，暂不支持该功能
# 类型：int32
# 取值范围 & 约束：resize_output_h：[16,4096]或0；resize_output_w：[16,1920]或0；resize_output_w/resize_input_w∈[1/16,16]、resize_output_h/resize_input_h∈[1/16,16]
resize_output_w :0
resize_output_h :0
# 说明：若开启了缩放功能，并且没有配置padding，该场景下resize_output_w和resize_output_h才能取值为0或不配置，此时缩放后图像的宽和高取值来自模型文件--input_shape中的宽和高，并且--input_shape中的高取值范围为[16,4096]，宽取值范围为[16,1920]。


#======== padding参数设置（配置样例请参见AIPP配置 > Crop/Padding配置说明） =========
# AIPP处理图片时padding使能开关
# 类型：bool
# 取值范围：true/false，true表示支持，false表示不支持
# padding :false
 
# H和W的填充值，静态AIPP配置（left_padding_size、right_padding_size、top_padding_size、bottom_padding_size 取值范围为[0,32]）
# 类型： int32
# left_padding_size :0
# right_padding_size :0
# top_padding_size :0
# bottom_padding_size :0
# AIPP经过padding后，输出的H和W要与模型需要的H和W保持一致，其中W取值要<=1080。


#================================ rotation参数设置 ==================================
# AIPP处理图片时的旋转角度，保留字段，暂不支持该功能
# 类型：uint8
# 范围：{0, 1, 2, 3} 0不旋转，1顺时针90°，2顺时针180°，3顺时针270°
# rotation_angle :0


#========= 色域转换参数设置（配置样例请参见AIPP配置 > 色域转换配置说明） =============
# 色域转换开关，静态AIPP配置
# 类型：bool
# 取值范围：true/false，true表示开启色域转换，false表示关闭
# csc_switch :false

# R通道与B通道交换开关/U通道与V通道交换开关
# 类型：bool
# 取值范围：true/false，true表示开启通道交换，false表示关闭
# rbuv_swap_switch :false

# RGBA->ARGB, YUVA->AYUV交换开关
# 类型：bool
# 取值范围：true/false，true表示开启，false表示关闭
# ax_swap_switch :false

# 单行处理模式（只处理抠图后的第一行）开关，保留字段，暂不支持该功能
# 类型：bool
# 取值范围：true/false，true表示开启单行处理模式，false表示关闭
# single_line_mode :false

# 若色域转换开关为false，则本功能不起作用。
# 若输入图片通道数为4，则忽略A通道或X通道。
# YUV转BGR：
# | B |   | matrix_r0c0 matrix_r0c1 matrix_r0c2 | | Y - input_bias_0 |
# | G | = | matrix_r1c0 matrix_r1c1 matrix_r1c2 | | U - input_bias_1 | >> 8
# | R |   | matrix_r2c0 matrix_r2c1 matrix_r2c2 | | V - input_bias_2 |
# BGR转YUV：
# | Y |   | matrix_r0c0 matrix_r0c1 matrix_r0c2 | | B |        | output_bias_0 |
# | U | = | matrix_r1c0 matrix_r1c1 matrix_r1c2 | | G | >> 8 + | output_bias_1 |
# | V |   | matrix_r2c0 matrix_r2c1 matrix_r2c2 | | R |        | output_bias_2 |

# 3*3 CSC矩阵元素
# 类型：int16
# 取值范围：[-32677 ,32676] 
# matrix_r0c0 :298
# matrix_r0c1 :516
# matrix_r0c2 :0
# matrix_r1c0 :298
# matrix_r1c1 :-100
# matrix_r1c2 :-208
# matrix_r2c0 :298
# matrix_r2c1 :0
# matrix_r2c2 :409

# RGB转YUV时的输出偏移
# 类型：uint8
# 取值范围：[0, 255]
# output_bias_0 :16
# output_bias_1 :128
# output_bias_2 :128

# YUV转RGB时的输入偏移
# 类型：uint8
# 取值范围：[0, 255]
# input_bias_0 :16
# input_bias_1 :128
# input_bias_2 :128


#============================== 减均值、乘系数设置 =================================
# 计算规则如下：
# 当uint8->uint8时，本功能旁路
# 当uint8->fp16时，pixel_out_chx(i) = [pixel_in_chx(i) – mean_chn_i – min_chn_i] * var_reci_chn

# 每个通道的均值
# 类型：uint8
# 取值范围：[0, 255]
# mean_chn_0 :0
# mean_chn_1 :0
# mean_chn_2 :0
# mean_chn_3 :0

# 每个通道的最小值
# 类型：float16
# 取值范围：[0, 255]
# min_chn_0 :0.0
# min_chn_1 :0.0
# min_chn_2 :0.0
# min_chn_3 :0.0

# 每个通道的方差
# 类型：float16
# 取值范围：[-65504, 65504]
# var_reci_chn_0 :1.0
# var_reci_chn_1 :1.0
# var_reci_chn_2 :1.0
# var_reci_chn_3 :1.0
}

#========================= 静态AIPP需设置，动态AIPP无需设置 （end）=====

```



### DVPP干了什么

使用DVPP进行数据预处理后，由于DVPP各组件基于处理速度和内存占用量的考虑，对输出图片有诸多限制，如输出图片需要长宽对齐，输出格式必须为YUV420SP等，但模型输入通常为RGB或BGR，且输入图片尺寸各异。因此，提供AIPP（Artificial Intelligence Pre-Processing）功能，AIPP用于在AI Core上完成图像预处理，包括改变图像尺寸、色域转换（转换图像格式）、减均值/乘系数（改变图像像素），数据处理之后再进行真正的模型推理。

### 为什么用AIPP

使用DVPP进行数据预处理后，由于DVPP各组件基于处理速度和内存占用量的考虑，对输出图片有诸多限制，如输出图片需要长宽对齐，输出格式必须为YUV420SP等，但模型输入通常为RGB或BGR，且输入图片尺寸各异。因此，提供AIPP（Artificial Intelligence Pre-Processing）功能，AIPP用于在AI Core上完成图像预处理，包括改变图像尺寸、色域转换（转换图像格式）、减均值/乘系数（改变图像像素），数据处理之后再进行真正的模型推理。

### 静态AIPP

模型转换时设置AIPP模式为静态，同时设置AIPP参数，模型生成后，AIPP参数值被保存在离线模型中，每次模型推理过程采用固定的AIPP预处理参数（无法修改）。

如果使用静态AIPP方式，多batch情况下共用同一份AIPP参数。

### 动态AIPP

模型转换时仅设置AIPP模式为动态，每次模型推理前，根据需求，在执行模型前设置动态AIPP参数值，然后在模型执行时可使用不同的AIPP参数。动态AIPP在根据业务要求改变预处理参数的场合下使用（如不同摄像头采用不同的归一化参数，输入图片格式需要兼容YUV420和RGB等）。设置动态AIPP参数值的接口请参见《[应用软件开发指南](https://support.huaweicloud.com/asdevg-c-cann/atlasdevelopment_01_0001.html)》手册中的“AscendCL API参考>模型加载与执行>aclmdlSetInputAIPP”章节。

如果使用动态AIPP方式，多batch使用不同的参数，体现在动态参数结构体中，每个batch可以配置不同的crop等参数。关于动态参数结构体，请参见[动态AIPP的参数输入结构](https://support.huaweicloud.com/tg-Inference-cann/atlasatc_16_0068.html)。