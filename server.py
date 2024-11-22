from flask import Flask
from sensor_reader import read_sensor_data, send_data
from threading import Thread
import time

app = Flask(__name__)
with app.app_context():
    def start_background_task():
        Thread(target=monitor_sensors, daemon=True).start()

          
            
# Funcao para monitorar sensores
def monitor_sensors():
    while True:
        sensor_data = read_sensor_data()
        if sensor_data is not None:
            print('Dados lidos dos sensores:', sensor_data)
            send_data(sensor_data)           
       
                      
@app.route('/')
def index():
    return 'Raspberry-Pi Flask Server ON'

if __name__ == "__main__":
    start_background_task()
    app.run(host="0.0.0.0", port=5000)


