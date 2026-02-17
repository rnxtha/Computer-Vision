# QR Code Scanner - Computer Vision Project

A Python-based QR code scanner that can detect and decode QR codes from both camera feeds and image files.

## Features

- 📷 **Camera Scanning**: Real-time QR code detection from webcam/camera feed
- 🖼️ **Image Scanning**: Decode QR codes from image files (JPG, PNG, etc.)
- 🎯 **Visual Feedback**: Draws bounding boxes around detected QR codes
- 💾 **Save Results**: Option to save detected QR codes and annotated images
- 🔍 **Multiple Codes**: Detects multiple QR codes in a single image

## Installation

### Prerequisites

- Python 3.7 or higher
- A webcam (for camera mode)

### Install Dependencies

1. Install Python packages:
```bash
pip install -r requirements.txt
```

2. **Windows Users**: Install ZBar library:
   - Download from: https://github.com/mchehab/zbar/releases
   - Or use: `pip install pyzbar` (may require additional system libraries)

3. **Linux Users**: Install ZBar:
```bash
sudo apt-get install libzbar0
```

4. **macOS Users**: Install ZBar:
```bash
brew install zbar
```

## Usage

### Camera Mode (Default)

Scan QR codes from your webcam in real-time:

```bash
python qr_scanner.py --mode camera
```

Or simply:
```bash
python qr_scanner.py
```

**Controls:**
- Press `q` to quit
- Press `s` to save current frame

**Options:**
- `--camera-index N`: Use camera device N (default: 0)
- `--no-preview`: Disable preview window
- `--save`: Save detected QR codes to file

### Image Mode

Scan QR codes from an image file:

```bash
python qr_scanner.py --mode image --image path/to/image.jpg
```

**Options:**
- `--image PATH`: Path to the image file (required)
- `--no-preview`: Don't show result window
- `--save`: Save annotated image with detected QR codes

### Examples

1. **Scan from camera with save option:**
```bash
python qr_scanner.py --mode camera --save
```

2. **Scan from image:**
```bash
python qr_scanner.py --mode image --image qr_code.png
```

3. **Scan from image and save annotated result:**
```bash
python qr_scanner.py --mode image --image qr_code.png --save
```

4. **Use different camera:**
```bash
python qr_scanner.py --mode camera --camera-index 1
```

## Programmatic Usage

You can also use the QRCodeScanner class in your own Python scripts:

```python
from qr_scanner import QRCodeScanner

# Create scanner instance
scanner = QRCodeScanner()

# Scan from image
results = scanner.decode_qr_from_image('qr_code.png')
for result in results:
    print(f"Found QR code: {result['data']}")

# Scan from camera
scanner.scan_from_camera(camera_index=0, show_preview=True)
```

## Output

- **Console**: Prints detected QR code data to console
- **Visual**: Shows bounding boxes around detected QR codes
- **Files**: 
  - `detected_qr_codes.txt`: List of all detected QR codes (when using --save in camera mode)
  - `*_detected.jpg`: Annotated images with QR code boxes (when using --save in image mode)

## Troubleshooting

### Camera not opening
- Check if camera is being used by another application
- Try different camera indices: `--camera-index 1`, `--camera-index 2`, etc.
- On Windows, ensure camera permissions are granted

### No QR codes detected
- Ensure good lighting
- QR code should be clearly visible and not blurry
- Try adjusting camera distance from QR code
- Check if image quality is sufficient

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- On Linux, install system libraries: `sudo apt-get install libzbar0`
- On macOS, install via Homebrew: `brew install zbar`

## Project Structure

```
qr scanner/
├── qr_scanner.py      # Main scanner script
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## License

This project is open source and available for educational purposes.

