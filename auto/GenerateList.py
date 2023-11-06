import json
import os.path


class GenList:
    def __init__(self, in_path="font"):
        self.path = in_path
        with open("auto/ReadMeConfig.json", "r", encoding="utf8") as conf_file:
            conf_data = conf_file.read()
            self.conf = json.loads(conf_data)['fonts']

    def dealMain(self):
        # Check main path
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
        if font_main in self.conf:
            font_conf = self.conf[font_main]
            save_text = ("| [%s](%s) | %s | %s | [%s](%s%s) | %s | %s "
                         "| [China CDN](%s) [Github](%s) | [%s](%s) | None |\n") % (
                            font_conf['name'], font_conf['repo'], font_conf['nick'],
                            font_conf['vers'], font_conf['text'], font_conf['repo'],
                            font_conf['eula'],font_conf['f_iu'], font_conf['f_cu'],
                            "https://cdn-tx1.pika.net.cn/Menu/%s.123yun.css" % font_main,
                            "https://cdn-tx1.pika.net.cn/Menu/%s.github.css" % font_main,
                            font_main, "font/%s" % font_main)
            read_file.write(save_text)


if __name__ == '__main__':
    gen = GenList()
    gen.dealMain()
