import matplotlib.pyplot as plt
import numpy as np


def style1(colors):
    # 创建一个白色背景的图
    fig, ax = plt.subplots(figsize=(8, 2), facecolor='white')

    # 绘制颜色块
    for i, color in enumerate(colors):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))

    # 去除坐标轴
    ax.set_xlim(0, len(colors))
    ax.set_ylim(0, 1)
    ax.axis('off')

    # 显示图像
    plt.savefig('style5.pdf')


# 定义8种中国风颜色--style 1
colors = [
        "#3A5FCD",  # 青花蓝
        "#E74C3C",  # 朱砂红
        "#27AE60",  # 翡翠绿
        "#CBA135",  # 香槟金
        "#8B4513",  # 茶棕色
        "#78A478",  # 竹绿
        "#5D4F70",  # 烟灰紫
        "#964B00"   # 红豆沙
]

# 定义8种中国风颜色--style 2
color_hex = [
    "#2E86C1",  # 宝石蓝
    "#E74C3C",  # 鲜艳红
    "#2ECC71",  # 翠绿色
    "#F1C40F",  # 金色
    "#E67E22",  # 橙色
    "#9B59B6",  # 鲜紫色
    "#1ABC9C",  # 亮青色
    "#D35400"   # 亮棕色
]

# 定义8种中国风颜色--style 3
color_hex2 = [
    "#2E86C1",  # 宝石蓝
    "#E74C3C",  # 鲜艳红
    "#2ECC71",  # 翠绿色
    "#E67E22",  # 橙色
    "#9B59B6",  # 紫色
    "#1ABC9C",  # 青色
    "#8E44AD",  # 深棕色
    "#C0392B"   # 暗红色
]

# 定义8种中国风颜色--style 4
color_hex3 = [
    "#2E86C1",  # 宝石蓝
    "#2ECC71",  # 翠绿色
    "#E67E22",  # 橙色
    "#1ABC9C",  # 青色
    "#2F4F4F",  # 深灰色
    "#000000",  # 黑色
    "#8B4513",  # 深褐色
    "#708090"   # 石板灰
]

# 定义8种中国风颜色--style 5
color_hex = [
    "#4F81BD",  # 柔和蓝
    "#F79646",  # 浅橙色
    "#9BBB59",  # 柔和绿
    "#8064A2",  # 紫灰色
    "#4BACC6",  # 深灰色
    "#C0504D",  # 柔和紫
    "#1F497D",  # 青蓝色
    "#A9A9A9"   # 浅灰色
]
style1(color_hex)