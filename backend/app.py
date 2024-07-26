from flask import Flask, request, session , g , jsonify
from flask_cors import CORS
from pymongo import MongoClient
from flask_session import Session
from flask_bcrypt import Bcrypt
from torchvision import models, transforms
from PIL import Image
import torch

import cv2
from pathlib import Path
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

dataset_dir = Path("animals")


app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.secret_key = 'agirsenseisthebest'

num_classes = 10
model = models.resnet18(pretrained=True)
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load('plant_disease_model_1_latest.pt', map_location=torch.device('cpu')))
model.eval()

MONGO_URI = ""
client = MongoClient(MONGO_URI)
db = client.get_database("PROJECT")
collection = db.get_collection("Recieved_data")
collection1 = db.get_collection('Information')
collection2 = db.get_collection('Plant_information')


@app.route('/api/dashboard', methods=['GET'])
def data():
    if request.method == 'GET':
        device_id = 'ab01'
        if device_id:
            data = collection.find_one({"device_id": device_id})
            if data:
                return {"temperature": data["current_temperature"] ,"humidity": data["current_humidity"] , "light": data["current_light_intensity"] , "soil": data["current_soil_moisture"] , "speed": data["current_wind_speed"] , "time": data["current_time"] , "n": data["current_nitrogen"] , "p": data["current_phosphorus"], "k": data["current_potassium"],
                        "temperature1": data["previous_temperature"] ,"humidity1": data["previous_humidity"] , "light1": data["previous_light_intensity"] , "soil1": data["previous_soil_moisture"] , "speed1": data["previous_wind_speed"] , "time1": data["previous_time"] , "n1": data["previous_nitrogen"] , "p1": data["previous_phosphorus"] , "k1": data["previous_potassium"] ,
                        "temperature2": data["previous1_temperature"] ,"humidity2": data["previous1_humidity"] , "light2": data["previous1_light_intensity"] , "soil2": data["previous1_soil_moisture"] , "speed2": data["previous1_wind_speed"] , "time2": data["previous1_time"] , "n2": data["previous1_nitrogen"] , "p2": data["previous1_phosphorus"], "k2": data["previous1_potassium"] ,
                        "temperature3": data["previous2_temperature"] ,"humidity3": data["previous2_humidity"] , "light3": data["previous2_light_intensity"] , "soil3": data["previous2_soil_moisture"] , "speed3": data["previous2_wind_speed"] , "time3": data["previous2_time"] , "n3": data["previous2_nitrogen"] , "p3": data["previous2_phosphorus"] , "k3": data["previous2_potassium"] , 
                        "temperature4": data["previous3_temperature"] ,"humidity4": data["previous3_humidity"] , "light4": data["previous3_light_intensity"] , "soil4": data["previous3_soil_moisture"] , "speed4": data["previous3_wind_speed"] , "time4": data["previous3_time"] , "n4": data["previous3_nitrogen"] , "p4": data["previous3_phosphorus"] , "k4": data["previous3_potassium"] , 
                        "temperature5": data["previous4_temperature"] ,"humidity5": data["previous4_humidity"] , "light5": data["previous4_light_intensity"] , "soil5": data["previous4_soil_moisture"] , "speed5": data["previous4_wind_speed"] , "time5": data["previous4_time"] , "n5": data["previous4_nitrogen"] , "p5": data["previous4_phosphorus"] , "k5": data["previous4_potassium"] ,
                        "temperature6": data["previous5_temperature"] ,"humidity6": data["previous5_humidity"] , "light6": data["previous5_light_intensity"] , "soil6": data["previous5_soil_moisture"] , "speed6": data["previous5_wind_speed"] , "time6": data["previous5_time"] , "n6": data["previous5_nitrogen"] , "p6": data["previous5_phosphorus"] , "k6": data["previous_potassium"] ,
                        "latitude": data["latitude"] , "longitude": data["longitude"]}
            else:
                return {"message": "data not found for this device_id"}, 404
        else:
            return {"message": "Device_id parameter is missing"}, 400
    else:
        return "Method not allowed", 405
    

@app.route('/api/fieldbot', methods=['GET'])
def fieldbot():
    if request.method == 'GET':
        device_id = 'ab01'
        if device_id:
            data = collection.find_one({"device_id": device_id})
            if data:
                return {
                    "temperature": data["current_temperature"],
                    "humidity": data["current_humidity"],
                    "light": data["current_light_intensity"],
                    "soil": data["current_soil_moisture"],
                    "speed": data["current_wind_speed"],
                    "time": data["current_time"],
                    "n": data["current_nitrogen"],
                    "p": data["current_phosphorus"],
                    "k": data["current_potassium"],
                    "water_level": data["current_water_level"],  

                    "temperature1": data["previous_temperature"],
                    "humidity1": data["previous_humidity"],
                    "light1": data["previous_light_intensity"],
                    "soil1": data["previous_soil_moisture"],
                    "speed1": data["previous_wind_speed"],
                    "time1": data["previous_time"],
                    "n1": data["previous_nitrogen"],
                    "p1": data["previous_phosphorus"],
                    "k1": data["previous_potassium"],
                    "water_level1": data["previous_water_level"],  

                    "temperature2": data["previous1_temperature"],
                    "humidity2": data["previous1_humidity"],
                    "light2": data["previous1_light_intensity"],
                    "soil2": data["previous1_soil_moisture"],
                    "speed2": data["previous1_wind_speed"],
                    "time2": data["previous1_time"],
                    "n2": data["previous1_nitrogen"],
                    "p2": data["previous1_phosphorus"],
                    "k2": data["previous1_potassium"],
                    "water_level2": data["previous1_water_level"], 

                    "temperature3": data["previous2_temperature"],
                    "humidity3": data["previous2_humidity"],
                    "light3": data["previous2_light_intensity"],
                    "soil3": data["previous2_soil_moisture"],
                    "speed3": data["previous2_wind_speed"],
                    "time3": data["previous2_time"],
                    "n3": data["previous2_nitrogen"],
                    "p3": data["previous2_phosphorus"],
                    "k3": data["previous2_potassium"],
                    "water_level3": data["previous2_water_level"], 

                    "temperature4": data["previous3_temperature"],
                    "humidity4": data["previous3_humidity"],
                    "light4": data["previous3_light_intensity"],
                    "soil4": data["previous3_soil_moisture"],
                    "speed4": data["previous3_wind_speed"],
                    "time4": data["previous3_time"],
                    "n4": data["previous3_nitrogen"],
                    "p4": data["previous3_phosphorus"],
                    "k4": data["previous3_potassium"],
                    "water_level4": data["previous3_water_level"], 

                    "temperature5": data["previous4_temperature"],
                    "humidity5": data["previous4_humidity"],
                    "light5": data["previous4_light_intensity"],
                    "soil5": data["previous4_soil_moisture"],
                    "speed5": data["previous4_wind_speed"],
                    "time5": data["previous4_time"],
                    "n5": data["previous4_nitrogen"],
                    "p5": data["previous4_phosphorus"],
                    "k5": data["previous4_potassium"],
                    "water_level5": data["previous4_water_level"], 

                    "temperature6": data["previous5_temperature"],
                    "humidity6": data["previous5_humidity"],
                    "light6": data["previous5_light_intensity"],
                    "soil6": data["previous5_soil_moisture"],
                    "speed6": data["previous5_wind_speed"],
                    "time6": data["previous5_time"],
                    "n6": data["previous5_nitrogen"],
                    "p6": data["previous5_phosphorus"],
                    "k6": data["previous5_potassium"],
                    "water_level6": data["previous5_water_level"],

                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                    "fire": data["fire_status"],
                    "gas" : data["gas_status"],
                    "phvalue" : data["ph_value"],
                    "irrigation" : data["irrigation"],
                    "irrigationtime" : data["irrigation_time"]
                }
            else:
                return {"message": "data not found for this device_id"}, 404
        else:
            return {"message": "Device_id parameter is missing"}, 400
    else:
        return "Method not allowed", 405
    


@app.route('/api/cropdoctor', methods=['GET'])
def cropdoctor():
    if request.method == 'GET':
        device_id = 'ab01'
        if device_id:
            data = collection.find_one({"device_id": device_id})
            if data:
                return {
                    "temperature": data["current_temperature"],
                    "humidity": data["current_humidity"],
                    "light": data["current_light_intensity"],
                    "soil": data["current_soil_moisture"],
                    "speed": data["current_wind_speed"],
                    "time": data["current_time"],
                    "n": data["current_nitrogen"],
                    "p": data["current_phosphorus"],
                    "k": data["current_potassium"],
                    "water_level": data["current_water_level"],  

                    "temperature1": data["previous_temperature"],
                    "humidity1": data["previous_humidity"],
                    "light1": data["previous_light_intensity"],
                    "soil1": data["previous_soil_moisture"],
                    "speed1": data["previous_wind_speed"],
                    "time1": data["previous_time"],
                    "n1": data["previous_nitrogen"],
                    "p1": data["previous_phosphorus"],
                    "k1": data["previous_potassium"],
                    "water_level1": data["previous_water_level"], 
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                    "fire": data["fire_status"],
                    "gas" : data["gas_status"],
                    "phvalue" : data["ph_value"],
                    "irrigation" : data["irrigation"],
                    "irrigationtime" : data["irrigation_time"]
                }
            else:
                return {"message": "data not found for this device_id"}, 404
        else:
            return {"message": "Device_id parameter is missing"}, 400
    else:
        return "Method not allowed", 405

    

@app.route('/api/data', methods=['GET'])
def get_data():
    data = list(collection2.find())
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data)



@app.route('/predict', methods=['POST'])
def predict():
    image_file = request.files['image']
    image = Image.open(image_file)
    image_tensor = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        prediction = predicted.item()

    return jsonify({'prediction': prediction})
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
