# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

from cvcamera import CvCamera


class CvImage(Image):
    def __init__(self, img, **kwargs):
        super(CvImage, self).__init__(**kwargs)
        self.img = cv2.imread(img, cv2.IMREAD_COLOR)  # El segundo parametro especifica en que formato se carga.
        self.img = cv2.flip(self.img, 0)
        self.buf = self.img.tostring()
        #self.make_texture()

    def make_texture(self):
        image_texture = Texture.create(
            size=(self.img.shape[1], self.img.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(self.buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture

    def on_touch_up(self, touch):
        self.make_texture()

class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = CvCamera(capture=self.capture, fps=30)
        #img = CvImage("test.jpg")
        #label = Label(text="Esto mola")
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()