import os
import configparser


class ReadConfig:

    iniFileName = 'File_Configs.ini'
    config_file_location = '~/src/'

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


    def get_one_section(self, section):
        """ Output values of a whole section """

        opt_values = []
        for opt in self.configParser.options(section):
            one_opt = self.configParser.get(section, opt)
            opt_values.append(one_opt)

        return opt_values


    # def get_boolean_value(self, section, option):
    #     """ Get boolean values of one option from ini file """
    #
    #     option_value = self.configParser.getboolean(section, option)
    #     return option_value
