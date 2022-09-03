from PyQt5.QtWidgets import QDialog, QFileDialog, QMainWindow, QApplication, QPushButton
import sys
from ui_main import Ui_GetText

class GetText(QMainWindow, Ui_GetText):
    def __init__(self):
        super(GetText, self).__init__()
        self.ui = Ui_GetText()
        self.ui.setupUi(self)
        self.ui.AddPicture.clicked.connect(self.add_picture)
        self.ui.pushButton.clicked.connect(self.insert_picture)
        self.ui.pushButton_2.clicked.connect(self.copy)

    # Copy button functionality
    def copy(self):
        c = QApplication.clipboard()
        if c != None:
            c.setText(self.text)

    # Paste picture from clipboard
    def insert_picture(self):
        import pytesseract
        from PIL import Image, ImageGrab
        img = ImageGrab.grabclipboard()
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.text = pytesseract.image_to_string(img) # Can add: lang='rus'
        self.ui.label.setText(self.text)
        self.translate_ru(self.text)
        
    # Upload picture as file
    def add_picture(self):
        path = QFileDialog.getOpenFileName(self, "Open File", None, "*.png *.jpg")
        print(path)
        self.get_result(path)

    def get_result(self, path):
        import pytesseract
        from PIL import Image
        img = Image.open(path[0])
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.text = pytesseract.image_to_string(img) # lang='rus'
        
        self.ui.label.setText(self.text)
        self.translate_ru(self.text)

    # Using the translater API from Yandex
    def translate_ru(self, text):
        import requests

        # !!! If you want to use this API, you need to get IAM_TOKEN, folder_id
        #     You can do it by following the link:  https://cloud.yandex.ru/docs/translate/operations/translate
        IAM_TOKEN = 'enter individual data'
        folder_id = 'enter individual data'
        target_language = 'ru'

        body = {
            "targetLanguageCode": target_language,
            "texts": text,
            "folderId": folder_id,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(IAM_TOKEN)
        }

        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
            json = body,
            headers = headers
        )
        res = response.json()
        res = res['translations'][0]['text']
        self.ui.textBrowser.setText(res)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GetText()
    window.show()
    sys.exit(app.exec_())