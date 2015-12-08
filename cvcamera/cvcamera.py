# coding:utf-8
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock

import cv2
import numpy as np


class CvCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(CvCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def map(self, buffer):  # -> Buffer
        def max_contours(contours):
            if len(contours) == 0:
                return None
            max_c = contours[0]
            for c in contours:
                if cv2.contourArea(max_c) < cv2.contourArea(c):
                    max_c = c
            return max_c

        #gray = cv2.cvtColor(buffer, cv2.COLOR_BGR2GRAY)

        #gray = np.float32(gray)
        #dst = cv2.cornerHarris(gray, 2, 3, 0.04)

        #result is dilated for marking the corners, not important
        #dst = cv2.dilate(dst, None)

        # Threshold for an optimal value, it may vary depending on the image.
        #buffer[dst > 0.01*dst.max()] = [0, 0, 255]
        imgray = cv2.cvtColor(buffer,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,127,255,0)
        im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        max_c = max_contours(contours)
        if max_c is not None:
            cv2.drawContours(buffer, [max_c], 0, (0,255,0), 3)
        return buffer

    def update(self, dt):
        ret, frame = self.capture.read()  # Lee de la camara la imagen actual / ret indica si es null la captura.
        if ret:
            # convert it to texture
            buf = cv2.flip(frame, 0)  # Le da la vuelta a la imagen.
            buf_str = self.map(buf).tostring()
            # hsv_buf = cv2.cvtColor(buf, cv2.COLOR_BGR2YCrCb)  # Cambia el espacio de color
            # Por defecto la imagen obtenido esta en el espacio de color BGR
            # Para cambiarlo al YCrCb cv2.COLOR_BGR2YCrCb
            # Para ponerlo en escala de grises COLOR_BGR2GRAY
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf_str, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

    def take_screenshot(self):  # -> Optional[Image]
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.flip(frame, 0).tostring()  # Le da la vuelta a la imagen.
            image_texture = Texture.create(size=frame.shape, colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            return Image(texture=image_texture)
        else:
            return None
