import json
import os.path
import markdown2
import codecs

FONT_TYPE = {
    "ttf": "truetype",
    "otf": "opentype",
    "woff2": "woff2",
    "otf.woff2": "woff2",
    "ttf.woff2": "woff2",
    "woff": "woff",
    "ttc": "truetype",
}
URLS_LIST = {
    "123yun": "https://vip.123pan.cn/1814096936/CDN-123CLOUD/font",
    "github": "https://font.52pika.cf/font",
    "gitees": "https://pikachuim.gitee.io/openfont/font",
    "smarts": ""
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
        with open("README.MD", "w", encoding="utf8") as read_file:
            read_file.write(head_data)
            # Create CSS
            for font_main in os.listdir(self.path):
                self.createMD(font_main, read_file)
        with open("README.MD", "r", encoding="utf8") as read_file:
            read_text = read_file.read()
        # with open("index.html", "w") as save_file:
        #     save_file.write(
        #         markdown2.markdown(read_text)
        #     )

    def createMD(self, font_main, read_file):
        # createMD ===========================================================================
        if font_main in self.conf:
            font_conf = self.conf[font_main]
            # Markdown ========================================================================
            save_text = ("| [%s](%s) | %s | %s | [%s](%s%s) | %s | %s "
                         "| [Github](%s) [Gitee](%s) [CDN](%s)| [%s](%s) |\n") % (
                            font_conf['name'], font_conf['repo'], font_conf['nick'],
                            font_conf['vers'], font_conf['shot'], font_conf['repo'],
                            font_conf['eula'], font_conf['f_iu'], font_conf['f_cu'],
                            "https://font.52pika.cf/menu/%s.github.css" % font_main,
                            "https://font.52pika.cf/menu/%s.gitees.css" % font_main,
                            "https://font.52pika.cf/menu/%s.123yun.css" % font_main,
                            font_main, "font/%s" % font_main)
            read_file.write(save_text)
            font_maps = self.dealFont(font_main)
            self.dealFile(font_main, font_maps)
            self.dealPage(font_main, font_maps)

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
        return font_maps

    def dealFile(self, font_main, font_maps):
        # Process File =======================================================================
        for urls_item in URLS_LIST:
            with open("%s/%s.%s.css" % (
                    self.menu, font_main, urls_item
            ), "w") as save_file:
                for font_subs in font_maps:
                    for font_name in font_maps[font_subs]:
                        font_type = font_maps[font_subs][font_name]
                        temp_text = "%s %s" % (font_subs.replace("-", " "), font_name)
                        font_text = ('@font-face {\n\tfont-family: "%s";\n' % temp_text)
                        counter = 0
                        for item_type in font_type:
                            if item_type in FONT_TYPE:
                                for urls_loop in URLS_LIST:
                                    urls_path = URLS_LIST[urls_loop]
                                    if urls_item != "smarts":
                                        if urls_loop != urls_item:
                                            continue
                                    elif urls_loop == urls_item or urls_loop == "123yun":
                                        continue
                                    if counter > 0:
                                        font_text += ",\n"
                                    counter += 1
                                    font_text += '\tsrc: url("%s/%s/%s/%s-%s.%s") format("%s")' % (
                                        urls_path, font_main,
                                        font_subs, font_subs, font_name.replace(" ", "-"),
                                        item_type, FONT_TYPE[item_type]
                                    )
                        font_text += ";\n}\n"
                        if counter > 0:
                            print(font_text)
                            save_file.write(font_text)

    def dealPage(self, font_main, font_maps):
        save_data = ""
        show_data = ('<link rel="stylesheet" '
                     'href="https://pikachuim.gitee.io/openfont/menu/'
                     '{}.smarts.css">\n').format(font_main)
        show_data += ('<link rel="stylesheet" '
                      'href="https://font.52pika.cf/menu/'
                      '{}.smarts.css">\n\n').format(font_main)
        show_temp = ('<h3 style="font-family: \'{1}\', serif;">{1}</h3>\n'
                     '<p style="font-family: \'{1}\', serif;">'
                     'The quick brown fox jumps over a lazy dog.<br />\n\n'
                     '因过竹院逢僧话，偷得浮生半日闲。————瞿士雅</p>\n\n')
        for font_subs in font_maps:
            for font_name in font_maps[font_subs]:
                temp_text = "%s %s" % (
                    font_subs.replace("-", " "), font_name)
                save_data += "\tfont-family: '%s', serif;\n" % temp_text
                show_data += show_temp.format(
                    font_main, temp_text)
        with open("auto/FontSubPages.md", "r",
                  encoding="utf8") as temp_file:
            temp_text = temp_file.read()
        save_text = temp_text.format(
            "",
            self.conf[font_main]['name'].replace("*", ""),
            self.conf[font_main]['repo'],
            self.conf[font_main]['text'],
            self.conf[font_main]['eula'],
            self.conf[font_main]['vers'],
            self.conf[font_main]['f_iu'],
            self.conf[font_main]['f_cu'],
            self.conf[font_main]['m_cl'],
            self.conf[font_main]['m_an'],
            font_main, save_data, show_data
        )
        with open("%s/%s/README.MD" % (
                self.path, font_main
        ), "w", encoding="utf8") as save_file:
            save_file.write(save_text)
        # with open("%s/%s/index.html" % (
        #         self.path, font_main
        # ), "w", encoding="utf8") as save_file:
        #     save_file.write(
        #         markdown2.markdown(save_text)
        #     )


if __name__ == '__main__':
    gen = GenList()
    gen.dealMain()
