"""
Download MobileNet-SSD model files for ball detection.
"""
import os
import urllib.request

# Create models directory
models_dir = "models"
if not os.path.exists(models_dir):
    os.makedirs(models_dir)
    print(f"Created directory: {models_dir}")

# Download prototxt file
prototxt_url = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt"
prototxt_path = os.path.join(models_dir, "MobileNetSSD_deploy.prototxt")

print(f"Downloading {prototxt_url}...")
urllib.request.urlretrieve(prototxt_url, prototxt_path)
print(f"Saved to {prototxt_path}")

# Download caffemodel file (~23MB)
model_url = "https://github.com/chuanqi305/MobileNet-SSD/raw/master/mobilenet_iter_73000.caffemodel"
model_path = os.path.join(models_dir, "MobileNetSSD_deploy.caffemodel")

print(f"Downloading {model_url} (this may take a moment, ~23MB)...")
urllib.request.urlretrieve(model_url, model_path)
print(f"Saved to {model_path}")

print("\n✅ Model files downloaded successfully!")
print(f"  - {prototxt_path}")
print(f"  - {model_path}")
