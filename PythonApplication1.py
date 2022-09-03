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
        IAM_TOKEN = 't1.9euelZrNnpmeyMyZzJSPzZiYj8uRi-3rnpWazZCVk5HHioqNjcfKzJSZmc3l8_dUaTNn-e8FFnd0_d3z9xQYMWf57wUWd3T9.3T9ASscPCfVc234MJQfDeKNnnx1xNh8i4fQGNS2FzgapI-dm8_d4XJ1HgABhARP5IJBxT02Duw7QbRqXkEkqCQ'
        folder_id = 'b1gde4q7t9i82jubdolu'
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

    '''
    # Trying to use API from Lingvo:

    def translate_ru(self, text):
        from collections.abc import Mapping
        import requests
        URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
        URL_TRANSLATE = 'https://developers.lingvolive.com/api/v1/Translation'
        KEY = 'OWQwMmYyZTMtNTZhZi00NmIxLTgwNzYtOGM4MzgxOTEzYzdhOjkyODlhZjkyZmMzOTQ4NTJhZDI1OThjNmJkNzEwOTYy'

        headers_auth = {'Authorization' : 'Basic ' + KEY}
        auth = requests.post(URL_AUTH, headers=headers_auth)
        if auth.status_code == 200:
            token = auth.text
            print("token:", token)
            headers_translate = {
                'Authorization' : 'Bearer ' + token
            }
            params = {
                'text' : text,
                'srcLang' : 1033,
                'dstLang' : 1049
            }
            print(headers_translate)
            print(params)
            r = requests.get(URL_TRANSLATE, headers = headers_translate, params=params)

            print("r: ", r)
            print("HERE\n")
            res = r.json()
            print("res: ", res)

            try:
                ans = res['Translation']['Translation']
                print("ans: ", ans)

                self.ui.textBrowser.setText(ans)
            except:
                pass
'''

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GetText()
    window.show()
    sys.exit(app.exec_())