import json
import os.path

FONT_TYPE = {
    "ttf": "truetype",
    "otf": "opentype",
    "woff2": "woff2",
    "otf.woff2": "woff2",
    "ttf.woff2": "woff2",
    "woff": "woff",
}
URLS_LIST = {
    "123yun": "https://vip.123pan.cn/1814096936/CDN-123CLOUD/font",
    "github": "https://github.com/PIKACHUIM/OpenFont/raw/main/font"
}


class GenList:
    def __init__(self,
                 in_path="font",
                 in_menu="menu"):
        self.path = in_path
        self.menu = in_menu
        with open("auto/ReadMeConfig.json", "r",
                  encoding="utf8") as conf_file:
            conf_data = conf_file.read()
            self.conf = json.loads(conf_data)['fonts']

    def dealMain(self):
        # Check main path ======================================================
        if not os.path.exists(self.path):
            print("[ERROR] Can not find path %s" % self.path)
            return False
        if not os.path.isdir(self.path):
            print("[ERROR] path %s is not dir!" % self.path)
            return False
        # Create Header
        with open("auto/ReadMeHeader.md", "r") as f:
            head_data = f.read()
        with open("README.MD", "w") as read_file:
            read_file.write(head_data)
            # Create CSS
            for font_main in os.listdir(self.path):
                self.createMD(font_main, read_file)

    def createMD(self, font_main, read_file):
        # createMD ===========================================================================
        if font_main in self.conf:
            font_conf = self.conf[font_main]
            # Markdown ========================================================================
            save_text = ("| [%s](%s) | %s | %s | [%s](%s%s) | %s | %s "
                         "| [China CDN](%s) [Github](%s) | [%s](%s) | None |\n") % (
                            font_conf['name'], font_conf['repo'], font_conf['nick'],
                            font_conf['vers'], font_conf['text'], font_conf['repo'],
                            font_conf['eula'], font_conf['f_iu'], font_conf['f_cu'],
                            "https://cdn-tx1.pika.net.cn/Menu/%s.123yun.css" % font_main,
                            "https://cdn-tx1.pika.net.cn/Menu/%s.github.css" % font_main,
                            font_main, "font/%s" % font_main)
            read_file.write(save_text)
            self.dealFont(font_main)

    def dealFont(self, font_main):
        if not os.path.exists(self.menu):
            os.makedirs(self.menu)
        font_path = os.path.join(self.path, font_main)
        # Dir check ==========================================================================
        if not os.path.exists(font_path):
            print("[ERROR] Can not find path %s" % font_path)
            return False
        if not os.path.isdir(font_path):
            print("[ERROR] path %s is not dir!" % font_path)
            return False
        font_maps = {
            # "Sub Name": {
            #     "Font Name": []
            # }
        }
        # Deal each file =====================================================================
        for font_subs in os.listdir(font_path):
            subs_path = os.path.join(font_path, font_subs)
            if font_subs not in font_maps:
                font_maps[font_subs] = {}
            if not os.path.isdir(subs_path):
                continue
            for font_name in os.listdir(subs_path):
                font_name = font_name.replace(font_subs, "")
                font_name = font_name.replace("-", " ")
                if font_name[0] == " ":
                    font_name = font_name[1:]
                temp_name = font_name.split(".")
                main_name = temp_name[0]
                subs_name = font_name.replace(main_name + ".", "")
                if main_name not in font_maps[font_subs]:
                    font_maps[font_subs][main_name] = []
                font_maps[font_subs][main_name].append(subs_name)
        # Process File =======================================================================
        for urls_item in URLS_LIST:
            with open("%s/%s.%s.css" % (
                    self.menu, font_main, urls_item
            ), "w") as save_file:
                for font_subs in font_maps:
                    for font_name in font_maps[font_subs]:
                        font_type = font_maps[font_subs][font_name]
                        # temp_text = self.conf[font_main]['name'].replace("*", "")
                        temp_text = "%s %s" % (
                            font_subs.replace("-", " "), font_name)
                        font_text = ('@font-face {\n\tfont-family: "%s";\n' % temp_text)
                        counter = 0
                        for item_type in font_type:
                            if item_type in FONT_TYPE:
                                if counter > 0:
                                    font_text += ",\n"
                                counter += 1
                                font_text += '\tsrc: url("%s/%s/%s/%s-%s.%s") format("%s")' % (
                                    URLS_LIST[urls_item], font_main,
                                    font_subs, font_subs, font_name,
                                    item_type, FONT_TYPE[item_type]
                                )
                        font_text += ";\n}\n"
                        if counter > 0:
                            print(font_text)
                            save_file.write(font_text)


if __name__ == '__main__':
    gen = GenList()
    gen.dealMain()
