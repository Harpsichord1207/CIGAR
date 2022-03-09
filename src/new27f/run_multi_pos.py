# -*- coding: utf-8 -*-
import pathlib
import subprocess
import sys


max_x_angle, max_y_angle, max_z_angle = 0.15, 0.15, 0.15

w, h = 50, 50


for pos_file in pathlib.Path(__file__).parent.joinpath('pos').iterdir():

    cmd = "opencv_createsamples -img {} ".format(pos_file.resolve())
    cmd += "-bg bg.txt "
    cmd += "-info info/{}.lst ".format(pos_file.name)
    cmd += "-pngoutput info "
    cmd += "-maxxangle {} ".format(max_x_angle)
    cmd += "-maxyangle {} ".format(max_y_angle)
    cmd += "-maxzangle {} ".format(max_z_angle)
    cmd += "-num 600"
    print('==' * 20)
    print('Start to execute: {}'.format(cmd))
    subprocess.call(cmd, shell=True, stderr=sys.stderr, stdout=sys.stdout)


# 合并多个.lst文件
# opencv_createsamples -info info/pz.lst -num 3000 -w 60 -h 60 -vec positives.vec
# opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos 1800 -numNeg 900 -numStages 15 -w 60 -h 60
