# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 16:55:02 2020

@author: dykua

Using tf-hub for neural style transfer
"""
import tensorflow as tf
import tensorflow_hub as hub
import PIL.Image
from sys import platform as _platform
import cv2
import numpy as np

def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)

def style_transfer(frame, style_path, hub_module):
    style_image = cv2.imread(style_path)
    content_image = frame.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = style_image.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = tf.image.resize(style_image, (256, 256))
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]
    
    return np.array(tensor_to_image(stylized_image))


class style_transfer_cam():
    def __init__(self, img_size = (400, 300)):
        
        self._platform = _platform
        
        self.cam_size = img_size 
            
        self.hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
        
    def run(self, feed = cv2.VideoCapture(0), style_path='./style_images/mosaic.jpg', write_to = None):
        
        interval = int( 1000/feed.get(cv2.CAP_PROP_FPS) )
        cam_w= int(feed.get(cv2.CAP_PROP_FRAME_WIDTH))
        cam_h= int(feed.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        if write_to is not None:
            codec = cv2.VideoWriter_fourcc(*'DIVX') # *'MP4V', *'DIVX', ... platform dependent
            writer= cv2.VideoWriter(write_to, codec, 30)
            
        while True:

            ret, frame = feed.read() 
            #reading the frame
            frame = cv2.resize(frame, self.cam_size)
        
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            frameClone = frame.copy()
            
            # apply special effect
            frameClone = style_transfer(frameClone, style_path = style_path, hub_module=self.hub_module)
            
            cv2.imshow('Camera View', frameClone)
            
            if self._platform in ['linux', 'linux2']:
                try:
                    import pyfakewebcam
                except ImportError:
                    print("pyfakewebcam is not installed.")
                    exit(1)
    
                stream = pyfakewebcam.FakeWebcam('/dev/video2')
                out_stream = cv2.resize(frameClone, (cam_w, cam_h))
                stream.schedule_frame(out_stream[..., ::-1])
            
            if cv2.waitKey(interval) & 0xFF == ord('q'):
                break
        
        feed.release()
        if write_to is not None:
            writer.release()
        cv2.destroyAllWindows()
        
    def transfer_image(self, source_path, style_path='./style_images/alvin.jpg', 
                       write_to = None):
        
        source_image = cv2.imread(source_path)
        stylized = style_transfer(source_image, style_path = style_path, hub_module=self.hub_module)
        cv2.imshow('Stylized', stylized)
        if write_to is not None:
            cv2.imwrite(write_to, stylized)
        return stylized

if __name__ == '__main__':
    st_cam = style_transfer_cam()
    st_cam.run()
    
    # source_path = r'C:\Users\dykua\Pictures\Saved Pictures\IMG_20200729_135406.jpg'
    # st_cam.transfer_image(source_path)


