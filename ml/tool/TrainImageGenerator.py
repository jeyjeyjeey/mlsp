# coding: utf-8
import os
from keras.preprocessing.image import ImageDataGenerator

train_data_base = 'train_data'
train_data_dir = os.path.join(train_data_base, 'melonpan')
classes = ['others']
original_img_count = 298
target_size = (244, 244)

idg = ImageDataGenerator(
    rotation_range=0.,  # 画像をランダムに回転する回転範囲（0-180）
    width_shift_range=0.,  # ランダムに水平シフトする範囲
    height_shift_range=0.,  # ランダムに垂直シフトする範囲
    shear_range=0.2,  # シアー強度（反時計回りのシアー角度（ラジアン））
    zoom_range=0.2,  # ランダムにズームする範囲
    horizontal_flip=True,  # 水平方向に入力をランダムに反転
    vertical_flip=True,  # 垂直方向に入力をランダムに反転
    # rescale=1.0 / 255, # 与えられた値をデータに積算する
)

gen = idg.flow_from_directory(
    directory=train_data_dir,
    classes=classes,
    target_size=target_size,
    batch_size=original_img_count,
    save_to_dir=os.path.join(train_data_dir, classes[0]),
    save_prefix='img',
    save_format='jpg')

for i in range(2):
    batch = gen.next()
