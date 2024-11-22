import serial
import time
import requests
import json
import os
from datetime import datetime, date, timedelta
from pydantic import BaseModel
from typing import List

# Configurando a porta serial de leitura do arduino
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

BACKEND_URL = "http://192.168.0.121:8000/api/data"
HEADERS = {"Content-Type":"application/json"}

class SensorData(BaseModel):
    sensor_type: str
    measure_type: str
    measure_value: str
    timestamp: str
    
    def to_dict(self):
        return {
            "sensor_type": self.sensor_type,
            "measure_type": self.measure_type,
            "measure_value": self.measure_value,
            "timestamp": self.timestamp
        }
    

class PackageData(BaseModel):
    data: List[SensorData]

def read_sensor_data():
    
    data_list = []
    
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            time.sleep(5)
            while ser.in_waiting > 0:

                line = ser.readline().decode('utf-8').strip()
                
                if line:
                    parts = line.split(" ")
                    sensor_type = parts[0]
                    
                    # Processamento das linhas
                    if sensor_type == "NTC":
                        # Arrumando formatacao dos dados
                        temperature = parts[1].replace("Â°C", "")
                        
                        # Encapsulando dados
                        data_list.append(SensorData(
                            sensor_type="NTC",
                            measure_type="TEMPERATURA",
                            measure_value=temperature,
                            timestamp=datetime.now().isoformat()
                        ))

                    elif sensor_type == "HIGR":
                        humidity = parts[1].replace("%", "")
                        data_list.append(SensorData(
                            sensor_type="HIGR",
                            measure_type="UMIDADE",
                            measure_value=humidity,
                            timestamp=datetime.now().isoformat()
                        ))
                    
                    elif sensor_type == "MQ7":
                        co_level = parts[1].replace("ppm", "")
                        data_list.append(SensorData(
                            sensor_type="MQ7",
                            measure_type="CO",
                            measure_value=co_level,
                            timestamp=datetime.now().isoformat()
                        ))
                    
                    elif sensor_type == "LDR":  # MUS = modulo de umidade de solo
                        lum = parts[1].replace("%", "")
                        data_list.append(SensorData(
                            sensor_type="LDR",
                            measure_type="LUMINOSIDADE",
                            measure_value=lum,
                            timestamp=datetime.now().isoformat()
                        ))
                        
        return data_list
                
            
    except Exception as e:
        print(f"Erro durante a leitura de dados do sensor")
        return None
    

def send_data(data_list):
    package = PackageData(data=data_list)  
    try:
        response = requests.post(BACKEND_URL, json=package.dict(), headers=HEADERS)
        response.raise_for_status()
        print('Dados enviados com sucesso:', response.status_code)
    except requests.RequestException as e:
        print(f'\033[91m Erro ao enviar dados para o backend: {e} \033[00m')
    
    
def main():
    
    while True:
        # Leitura dos dados dos sensores
        sensor_data = read_sensor_data()
        
        # Salva os dados dos sensores no arquivo JSON diï¿½rio
        if sensor_data:
            # send_data(sensor_data)
            print(sensor_data)


        # Intervalo de leitura (exemplo: a cada minuto)
        time.sleep(10)
    
if __name__ == "__main__":
    main()
        
