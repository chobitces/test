import os
import configparser


class Config():
    sessions = {}
    def __init__(self,path):
        self.confpath = path.replace("\\","/") + "/config"
        self.confpath = self.confpath.replace("/application", "")
        if not os.path.exists(self.confpath):
            os.mkdir(self.confpath)
        self.confpath = self.confpath + "/config.ini"


    def load(self, section):
        """
        下载配置
        :param section:配置的名称
        :return:
        """
        tpdict = {}
        config = configparser.ConfigParser()
        config.read(self.confpath)

        for key in config[section]:  # 注意,有default会默认default的键
            tpdict[key] = config[section][key]
        print(tpdict)
        return tpdict

    def save(self, text):
        """
        保存配置
        :param text:需要保存的配置字典
        :return:
        """
        section = []
        section = section + self.read_section()
        print(text["name"],section)
        if text["name"] not in section:
            config = configparser.ConfigParser()
            config[text["name"]] = text
            with open(self.confpath, 'a') as configfile:
                config.write(configfile)	#将对象写入文件

    def read_section(self):
        """
        读取配置
        :return: 读取的所有配置
        """
        config = configparser.ConfigParser()
        config.read(self.confpath)
        sectionlist = config.sections()
        return sectionlist

    def del_section(self):
        self.confpath = self.confpath
        os.remove(self.confpath)



def test():
    tpdict1 = {"conntype": "SSH",
              "host_ip": "10.26.0.250",
              "ssh_port": "22",
              "username": "root",
              "userpassword": "root",
              "name": "10.26.0.250"}
    tpdict2 = {"conntype": "serial",
              "comport": "COM4",
              "baudrate": "115200",
              "databit": "8",
              "parity": "none",
              "stopbits": "1"}
    path  = os.getcwd()
    print(path)
    config = Config(path)
    config.del_section()

if __name__ == '__main__':
    test()