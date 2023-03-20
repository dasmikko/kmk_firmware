import busio
import gc

import adafruit_displayio_ssd1306
import displayio
import terminalio
from adafruit_display_text import label

from kmk.extensions import Extension




class Oled(Extension):
    def __init__(
        self,
        group,
        oWidth=128,
        oHeight=64,
        flip: bool = False,
    ):
        displayio.release_displays()
        self.group = group
        self.rotation = 180 if flip else 0
        self._width = oWidth
        self._height = oHeight
        self._prevLayers = 0
        gc.collect()

    

    def updateOLED(self, sandbox):
        return

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, keyboard):
        displayio.release_displays()
        i2c = busio.I2C(keyboard.SCL, keyboard.SDA, frequency=400_000)
        self._display = adafruit_displayio_ssd1306.SSD1306(
            displayio.I2CDisplay(i2c, device_address=0x3C),
            width=self._width,
            height=self._height,
            rotation=self.rotation,
            native_frames_per_second=60
        )
        self._display.show(self.group)
        return

    def before_matrix_scan(self, sandbox):
        self.updateOLED(sandbox)
        gc.collect()
        return

    def after_matrix_scan(self, sandbox):

        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return
