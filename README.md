# Interactive Asteroid Destroyer Game (Projector Wall Edition)

An interactive game designed for **Projector Walls**. Use a **White Object** (like a paper ball, phone screen, or white cloth) to aim and destroy asteroids on the big screen!

## 🎮 Features

- **Object Tracking**: Uses Computer Vision to track bright white objects.
- **Designed for Projectors**: High contrast tracking works well in dark rooms.
- **Debug Mode**: Press **'D'** to see exactly what the camera sees (Picture-in-Picture).
- **No Special Hardware**: Just a webcam and a white object.

## 🚀 How to Play

1. **Setup**:
   - Connect your **Webcam**.
   - Project your computer screen onto the **Wall**.
   - Point the webcam at the **Wall** (so it sees the projected image).

2. **Run the Game**:
   ```bash
   python asteroid_game.py
   ```

3. **Aim & Destroy**:
   - Hold a **White Object** (paper, light, etc.).
   - Move it over the asteroids on the wall.
   - The green cursor will follow your object.
   - Destroy asteroids to score points!

## 🛠️ Controls

| Key | Action |
|-----|--------|
| SPACE | Start Game / Restart |
| F | Toggle Fullscreen |
| D | **Toggle Debug View** (See camera output) |
| ESC | Quit |

## ⚙️ Configuration

Edit `config.py` to tune tracking if needed:
- `TRACK_COLOR_LOWER`: Adjust sensitivity to light/color.
- `MIN_CONTOUR_AREA`: Adjust how big the object needs to be.
- `CAMERA_INDEX`: Change if you have multiple cameras.

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
