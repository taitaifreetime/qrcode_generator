import qrcode
from PIL import Image

class QRGenerator():
    def generate(self, text: str) -> Image:
        """generate qr code image

        Args:
            text (str): qr code data

        Returns:
            Image: qr code image
        """
        qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L, 
                box_size=10, 
                border=4, 
            )
        qr.add_data(text)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white')
        return qr_img