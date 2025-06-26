import pandas as pd

class CSVLoader():
    def __init__(self):
        self.df_ = None

    def get_shaped_data(self, file_path: str):
        """get shaped data

        Args:
            file_path (str): csv file path includes "file_name" and "qr_data" in header

        Returns:
            _type_: qr image name list, qr code image list, and error code 
        """
        self.df_ = pd.read_csv(file_path, encoding="shift-jis")
        shaped_data = self.parse_data()
        self.df_ = None
        return shaped_data
    
    def parse_data(self):
        """parse data

        Returns:
            _type_: qr image name list, qr code image list, and error code 
        """
        try:
            qr_img_name_list = self.df_['file_name']
            qr_data_list = self.df_['qr_data']
            return [qr_img_name_list, qr_data_list], None
        except KeyError as e:
            return [[], []], e