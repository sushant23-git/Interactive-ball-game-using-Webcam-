# Interactive Asteroid Destroyer Game (Projector Wall Edition)

An interactive game designed for **Projector Walls**. Use a **Ball** (tennis ball, soccer ball, basketball, or any sports ball) to aim and destroy asteroids on the big screen!

## 🎮 Features

- **ML-Based Ball Detection**: Uses **MobileNet-SSD** deep learning model to detect actual ball objects
- **Smart Object Recognition**: Trained on thousands of images - specifically recognizes sports balls
- **High Accuracy**: Less false positives compared to color/shape detection
- **Universal Ball Support**: Works with tennis balls, soccer balls, basketballs, and more
- **Real-time Performance**: Runs on CPU with 30+ FPS
- **Designed for Projectors**: Works well in various lighting conditions
- **Debug Mode**: Press **'D'** to see ML detection boxes and confidence scores
- **No GPU Required**: Runs on any computer with a webcam


https://github.com/user-attachments/assets/4074c287-9943-4957-b3a8-88d5fab8f98e


## 🚀 How to Play

1. **Setup**:
   - Connect your **Webcam**
   - Project your computer screen onto the **Wall**
   - Point the webcam at the **Wall** (so it sees the projected image)
   - Get any **sports ball** (tennis, soccer, basketball, etc.)

 2. **Run the Game**:
   ```bash
   python asteroid_game.py
   ```
   Note: On first run, the game will download the MobileNet-SSD model (~23MB)

3. **Aim & Destroy**:
   - Hold your **ball** in front of the projected wall
   - Move it over the asteroids
   - The green cursor will track your ball
   - Destroy asteroids to score points!

## 🛠️ Controls

| Key | Action |
|-----|--------|
| SPACE | Start Game / Restart |
| F | Toggle Fullscreen |
| D | **Toggle Debug View** (See ML detection boxes) |
| ESC | Quit |

## ⚙️ Configuration

Edit `config.py` to customize detection:
- `CONFIDENCE_THRESHOLD`: Adjust detection sensitivity (0.0-1.0, default: 0.3)
- `USE_COLOR_FILTER`: Enable additional color filtering after ML detection
- `MODEL_PROTOTXT` / `MODEL_WEIGHTS`: Path to model files
- `CAMERA_INDEX`: Change if you have multiple cameras

## 📦 Requirements

- Python 3.10+ (Works with 3.11, 3.12, 3.13)
- OpenCV
- Pygame
- Numpy

```bash
pip install -r requirements.txt
```

---
**Enjoy your Interactive Wall! 🎮 walls**
