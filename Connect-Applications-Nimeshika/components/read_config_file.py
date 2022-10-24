import os
import configparser


class ReadConfig:

    iniFileName = 'File_Configs.ini'
    config_file_location = 'src/'

    configParser = ''
    configFilePath = ''


    def __init__(self):

        #   Make ConfigParser object
        self.configParser = configparser.ConfigParser()
        self.configFilePath = os.path.join(self.config_file_location, self.iniFileName)
        self.configParser.read(self.configFilePath)



    def get_one_option(self, section, option):
        """ Output valuse of one option in a one section """

        option_value = self.configParser.get(section, option)
        return option_value
