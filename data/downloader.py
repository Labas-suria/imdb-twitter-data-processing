
class Downloader:

    def __init__(self, path_destin, data_source={}) -> None:
        """
        

        :param path_destin:
        :param data_source:
        """
        self.path_destin = path_destin
        self.data_url = data_source
