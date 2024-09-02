from pymongo import MongoClient
import threading
import random

# Criando um banco de dados no MongoDB
client = MongoClient('localhost', 27017)  # Conecta ao MongoDB rodando localmente
db = client.Bancoiot  # Seleciona o banco de dados 'Bancoiot'
collection = db.Sensores  # Seleciona a collection 'Sensores'

# Sensores iniciais
sensores_iniciais = [
    {"nomeSensor": "Temp1", "valorSensor": None, "unidadeMedida": "C°", "sensorAlarmado": False},
    {"nomeSensor": "Temp2", "valorSensor": None, "unidadeMedida": "C°", "sensorAlarmado": False},
    {"nomeSensor": "Temp3", "valorSensor": None, "unidadeMedida": "C°", "sensorAlarmado": False}
]

# Inserindo os sensores no MongoDB, usando 'upsert' para evitar duplicação
for sensor in sensores_iniciais:
    collection.update_one(
        {"nomeSensor": sensor["nomeSensor"]},
        {"$setOnInsert": sensor},
        upsert=True
    )

def sensor_function(nome_sensor):
    # Busca o sensor no MongoDB
    sensor = collection.find_one({"nomeSensor": nome_sensor})
    
    # Verifica se o sensor já está alarmado
    if sensor["sensorAlarmado"]:
        print(f"{nome_sensor} já está alarmado. Nenhuma nova temperatura será registrada.")
        return

    # Gera uma temperatura aleatória entre 30 e 40
    temperatura = random.uniform(30, 40)

    print(f"{nome_sensor} gerou a temperatura: {temperatura:.2f}°C")

    # Atualiza o documento no MongoDB com a nova temperatura
    collection.update_one(
        {"nomeSensor": nome_sensor},
        {"$set": {"valorSensor": temperatura}}
    )

    # Verifica se a temperatura ultrapassou 38°C
    if temperatura > 38:
        collection.update_one(
            {"nomeSensor": nome_sensor},
            {"$set": {"sensorAlarmado": True}}
        )
        print(f"Atenção! Temperatura muito alta! Verificar {nome_sensor}!")

# Criando as threads para os três sensores
sensores = ["Temp1", "Temp2", "Temp3"]

threads = []
for sensor in sensores:
    t = threading.Thread(target=sensor_function, args=(sensor,))
    threads.append(t)
    t.start()

# Aguardando todas as threads terminarem
for t in threads:
    t.join()

print("Geração de temperaturas finalizada.")
