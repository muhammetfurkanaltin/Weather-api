import sys
from PyQt5 import QtWidgets 



from Weather import Ui_MainWindow
import requests


class myApp(QtWidgets.QMainWindow):

    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Weather App")
        


        self.initUI()
        self.ui.btn_Wea.clicked.connect(self.get_weather)

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText('Enter City Name : ')
        self.label.move(6, 20)

    def get_weather(self):
        api_key = "api_key"
        city = self.ui.input_name.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            self.display_error(f"HTTP error occurred:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
        self.ui.lbl_tmp.setText(message)
        self.ui.lbl_emoji.clear()
        self.ui.lbl_des.clear()

    def display_weather(self, data):
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_description = data["weather"][0]["description"]

        
        self.ui.lbl_tmp.setText(f"{temperature_c:.0f}°C")
        self.ui.lbl_emoji.setText(self.get_weather_emoji(temperature_c)) 
        self.ui.lbl_des.setText(weather_description)
        

    @staticmethod
    def get_weather_emoji(temperature_c):
        
        if temperature_c >= 35:
            return "🔥" 
        elif 25 <= temperature_c < 35:
            return "☀️"  
        elif 15 <= temperature_c < 25:
            return "⛅"  
        elif 5 <= temperature_c < 15:
            return "🌧️"  
        elif -5 <= temperature_c < 5:
            return "❄️"  
        elif temperature_c < -5:
            return "🧊"  
        else:
            return "🤦‍♂️"

def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec_())


app()
