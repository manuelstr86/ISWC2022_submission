import xml.etree.ElementTree as ET


class XmlConfigDegari(object):

    def __init__(self, xml_file_name):
        self.tree = ET.parse(xml_file_name)
        self.root = self.tree.getroot()
        self.prototypes_path = ""
        self.imma_json_path = ""

    # setter prototypes path
    def set_prototypes_path(self, prototypes_path_par):
        self.prototypes_path = prototypes_path_par

    # setter imma json path
    def set_imma_json_path(self, imma_json_path_par):
        self.imma_json_path = imma_json_path_par

    def get_prototypes_path(self):
        return self.prototypes_path

    def get_imma_json_path(self):
        return self.imma_json_path

    def parseConfig(self):
        for config_items in self.root:
            self.prototypes_path = config_items.find("prototypes_path").text
            self.imma_json_path = config_items.find("imma_json_path").text


def main():
    degariConfig = XmlConfigDegari("degariConfig.xml")
    degariConfig.parseConfig()

    print("imma_json_path: " + degariConfig.get_imma_json_path())
    print("prototypes_path: " + degariConfig.get_prototypes_path())


if __name__ == '__main__':
    main()
