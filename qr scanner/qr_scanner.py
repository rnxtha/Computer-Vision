"""
QR Code Scanner - Computer Vision Project
Scans and decodes QR codes from camera feed or images
"""

import cv2
import numpy as np
from pyzbar import pyzbar
import argparse
import os
import sys


class QRCodeScanner:
    """QR Code Scanner class for detecting and decoding QR codes"""
    
    def __init__(self):
        self.camera = None
        
    def decode_qr_from_image(self, image_path):
        """
        Decode QR code from an image file
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            list: List of decoded QR code data
        """
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found.")
            return []
        
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image '{image_path}'.")
            return []
        
        # Decode QR codes
        decoded_objects = pyzbar.decode(image)
        
        results = []
        if decoded_objects:
            print(f"\nFound {len(decoded_objects)} QR code(s) in '{image_path}':")
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                qr_type = obj.type
                print(f"  - Type: {qr_type}, Data: {data}")
                results.append({
                    'data': data,
                    'type': qr_type,
                    'rect': obj.rect,
                    'polygon': obj.polygon
                })
        else:
            print(f"No QR codes found in '{image_path}'.")
        
        return results
    
    def draw_qr_boxes(self, image, decoded_objects):
        """
        Draw bounding boxes around detected QR codes
        
        Args:
            image: OpenCV image
            decoded_objects: List of decoded QR code objects
            
        Returns:
            image: Image with drawn boxes
        """
        for obj in decoded_objects:
            # Get the bounding box points
            points = obj.polygon
            if len(points) == 4:
                # Draw the bounding box
                pts = np.array(points, dtype=np.int32)
                cv2.polylines(image, [pts], True, (0, 255, 0), 2)
            
            # Draw the data text
            rect = obj.rect
            data = obj.data.decode('utf-8')
            cv2.putText(image, data, (rect.left, rect.top - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return image
    
    def scan_from_camera(self, camera_index=0, show_preview=True, save_output=False):
        """
        Scan QR codes from camera feed
        
        Args:
            camera_index (int): Camera device index (default: 0)
            show_preview (bool): Whether to show live preview window
            save_output (bool): Whether to save detected QR codes to file
        """
        # Initialize camera
        self.camera = cv2.VideoCapture(camera_index)
        
        if not self.camera.isOpened():
            print(f"Error: Could not open camera {camera_index}.")
            return
        
        print("Camera opened successfully!")
        print("Press 'q' to quit, 's' to save current frame")
        print("Point the camera at a QR code...")
        
        detected_codes = set()  # Track unique QR codes
        
        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("Error: Failed to read frame from camera.")
                break
            
            # Decode QR codes in the frame
            decoded_objects = pyzbar.decode(frame)
            
            # Draw boxes around detected QR codes
            if decoded_objects:
                frame = self.draw_qr_boxes(frame, decoded_objects)
                
                # Print detected codes
                for obj in decoded_objects:
                    data = obj.data.decode('utf-8')
                    if data not in detected_codes:
                        detected_codes.add(data)
                        print(f"\nQR Code detected: {data}")
            
            # Show preview
            if show_preview:
                cv2.imshow('QR Code Scanner - Press Q to quit', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s') and decoded_objects:
                # Save current frame
                filename = f"qr_scan_{len(detected_codes)}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Frame saved as '{filename}'")
        
        # Cleanup
        self.camera.release()
        cv2.destroyAllWindows()
        
        if detected_codes:
            print(f"\nTotal unique QR codes detected: {len(detected_codes)}")
            if save_output:
                self._save_detected_codes(detected_codes)
    
    def scan_from_image(self, image_path, show_result=True, save_result=False):
        """
        Scan QR codes from an image file
        
        Args:
            image_path (str): Path to the image file
            show_result (bool): Whether to show the image with detected QR codes
            save_result (bool): Whether to save the annotated image
        """
        # Read and decode
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image '{image_path}'.")
            return
        
        decoded_objects = pyzbar.decode(image)
        
        # Print detected QR codes
        if decoded_objects:
            print(f"\nFound {len(decoded_objects)} QR code(s) in '{image_path}':")
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                qr_type = obj.type
                print(f"  - Type: {qr_type}, Data: {data}")
            # Draw boxes
            image = self.draw_qr_boxes(image, decoded_objects)
        else:
            print(f"No QR codes found in '{image_path}'.")
        
        # Show result
        if show_result:
            cv2.imshow('QR Code Scanner - Result', image)
            print("\nPress any key to close the window...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        # Save result
        if save_result and decoded_objects:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = f"{base_name}_detected.jpg"
            cv2.imwrite(output_path, image)
            print(f"Annotated image saved as '{output_path}'")
    
    def _save_detected_codes(self, codes, filename="detected_qr_codes.txt"):
        """Save detected QR codes to a text file"""
        with open(filename, 'w') as f:
            f.write("Detected QR Codes:\n")
            f.write("=" * 50 + "\n")
            for i, code in enumerate(codes, 1):
                f.write(f"{i}. {code}\n")
        print(f"Detected codes saved to '{filename}'")


def main():
    """Main function to handle command-line arguments"""
    parser = argparse.ArgumentParser(
        description='QR Code Scanner - Scan QR codes from camera or images'
    )
    parser.add_argument(
        '--mode',
        choices=['camera', 'image'],
        default='camera',
        help='Scanning mode: camera or image (default: camera)'
    )
    parser.add_argument(
        '--image',
        type=str,
        help='Path to image file (required if mode is image)'
    )
    parser.add_argument(
        '--camera-index',
        type=int,
        default=0,
        help='Camera device index (default: 0)'
    )
    parser.add_argument(
        '--no-preview',
        action='store_true',
        help='Disable preview window (camera mode)'
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save output (detected codes or annotated images)'
    )
    
    args = parser.parse_args()
    
    # Create scanner instance
    scanner = QRCodeScanner()
    
    # Execute based on mode
    if args.mode == 'camera':
        scanner.scan_from_camera(
            camera_index=args.camera_index,
            show_preview=not args.no_preview,
            save_output=args.save
        )
    elif args.mode == 'image':
        if not args.image:
            print("Error: --image argument is required when using image mode.")
            parser.print_help()
            sys.exit(1)
        scanner.scan_from_image(
            image_path=args.image,
            show_result=not args.no_preview,
            save_result=args.save
        )


if __name__ == "__main__":
    main()

