# plant-disease-detection-with-cnn-and-whatsapp
Image Based Disease Detection for banana leaf with WhatsApp integration using CNN and keras-TensorFlow backend! 


## diseases of banana crops
- BUNCHY_TOP
  ![BUNCHY_TOP](https://raw.githubusercontent.com/soorajpazeekal/plant-disease-detection-with-cnn-and-whatsapp/main/valid/BUNCHY_TOP/001.jpg)
- CORDANA
  ![CORDANA](https://raw.githubusercontent.com/soorajpazeekal/plant-disease-detection-with-cnn-and-whatsapp/main/valid/CORDANA/001.jpg)
- PANAMA
  ![PANAMA](https://raw.githubusercontent.com/soorajpazeekal/plant-disease-detection-with-cnn-and-whatsapp/main/valid/PANAMA/001.jpg)
- SIGATOKA
  ![SIGATOKA](https://raw.githubusercontent.com/soorajpazeekal/plant-disease-detection-with-cnn-and-whatsapp/main/valid/SIGATOKA/001.jpg)

## Model training.
If you need to train a new Model with own data, please refer notebook with this repo.

## Installation

First clone this repo
second add user credentials
account_sid = ""
auth_token = ""

```bash
git clone https://github.com/soorajpazeekal/plant-disease-detection-with-cnn-and-whatsapp.git
```
If docker available:
```bash
docker build -t plant_python_demo:1.0 .
```
```bash
docker run -p 5000:5000 my-python-app:1.0
or
docker run -d --restart always -p 5000:5000 <image-id>
``
```bash
conda create -n myenv python=3.8
```
```python
pip install -r requirements.txt
```
```bash
sudo apt-get install ffmpeg libsm6 libxext6  -y
```
```python
python app.py
```

## Screenshots
![alt text](https://github.com/soorajpazeekal/plant-disease-detection-with-cnn-and-whatsapp/blob/main/screenshot-poc.gif)
