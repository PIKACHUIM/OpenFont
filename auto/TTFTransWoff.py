import os

from fontTools.ttLib import TTFont


def listDir(font_path):
    for item_file in os.listdir(font_path):
        full_path = os.path.join(font_path, item_file)
        if os.path.isdir(full_path):
            listDir(full_path)
        elif full_path.split(".")[-1] in ["woff2", "ttc", "ttf", "otf"]:
            convert(full_path)


def convert(font_path):
    # 打开TTF字体文件 -------------------------------
    font_data = TTFont(font_path, fontNumber=0)
    print("[Trans] %s" % font_path)
    # 保存到WOFF2字体 -------------------------------
    font_data.save(font_path.split(".")[0] + ".woff")
    # os.remove(font_path)


# 调用转换函数
if __name__ == '__main__':
    listDir("font/SarasaGothic")
