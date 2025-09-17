import cv2
import time
import os
from typing import List, Tuple, Optional

from commands.base_command import Command
from utils import constants, helpers

class CameraCaptureCommand(Command):
    """Capture an image from the webcam."""
    
    @property
    def name(self) -> str:
        return "camera_capture"
    
    def execute(self, *args) -> Tuple[bool, str]:
        try:
            # Initialize the camera
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                return False, "Could not open camera"
            
            # Capture a single frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return False, "Failed to capture image"
            
            # Generate filename with timestamp
            timestamp = helpers.get_timestamp()
            filename = f"camera_capture_{timestamp}.jpg"
            
            # Save the image
            cv2.imwrite(filename, frame)
            
            return True, f"Image captured and saved as {filename}"
            
        except Exception as e:
            # Ensure the camera is released even if an error occurs
            if 'cap' in locals():
                cap.release()
            return False, f"Error capturing image: {e}"

class CameraStreamCommand(Command):
    """Stream video from the webcam for a specified duration."""
    
    @property
    def name(self) -> str:
        return "camera_stream"
    
    def execute(self, *args) -> Tuple[bool, str]:
        duration = 10  # Default duration in seconds
        
        if args and args[0].isdigit():
            duration = int(args[0])
        
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                return False, "Could not open camera"
            
            # Get the frame dimensions
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Define the codec and create VideoWriter object
            timestamp = helpers.get_timestamp()
            output_file = f"camera_stream_{timestamp}.avi"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))
            
            start_time = time.time()
            
            while (time.time() - start_time) < duration:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Write the frame to the output file
                out.write(frame)
                
                # Display the resulting frame (optional)
                # cv2.imshow('Camera Stream', frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
            
            # Release everything when done
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            
            return True, f"Video captured and saved as {output_file}"
            
        except Exception as e:
            # Ensure resources are released even if an error occurs
            if 'cap' in locals() and cap.isOpened():
                cap.release()
            if 'out' in locals():
                out.release()
            cv2.destroyAllWindows()
            return False, f"Error during camera streaming: {e}"

def register_camera_commands(handler):
    """Register all camera-related commands with the command handler."""
    handler.register_command(CameraCaptureCommand())
    handler.register_command(CameraStreamCommand())
