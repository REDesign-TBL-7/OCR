# To Run

Raspberry Pi:
```console
sudo apt install tesseract-ocr

sudo apt-get install libcblas-dev
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev 
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-test

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 ocr_camera.py
```

MacOS:
```console
brew install tesseract

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 ocr_camera.py
```

# To Deactivate

```console
deactivate
```
