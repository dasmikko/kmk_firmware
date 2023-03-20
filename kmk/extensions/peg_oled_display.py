import busio
import gc	


import adafruit_displayio_ssd1306
import displayio
import terminalio
from adafruit_display_text import label
from kmk.kmktime import ticks_diff, ticks_ms

from kmk.extensions import Extension




class Oled(Extension):
    def __init__(
        self,
        group,
        oWidth=128,
        oHeight=64,
        timeout=2000,
        flip: bool = False,
    ):
        displayio.release_displays()
        self.group = group
        self.rotation = 180 if flip else 0
        self._width = oWidth
        self._height = oHeight
        self._timeout = timeout
        self._checkpoint = ticks_ms()
        self._displayIsAwake = True
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
        
        '''
        Put the OLED to sleep after some time, to prevent premature burn-in
        '''
        if ticks_diff(ticks_ms(), self._checkpoint) > self._timeout and self._displayIsAwake == True:
            self._checkpoint = ticks_ms()
            self._display.sleep()
            self._displayIsAwake = False

        gc.collect()
        return

    def after_matrix_scan(self, sandbox):
        '''
        Wake the display on keypress and update the checkpoint
        '''
        if sandbox.matrix_update is not None and sandbox.matrix_update.pressed == True:
            self._checkpoint = ticks_ms()
            if self._displayIsAwake == False:
                self._display.wake()
                self._displayIsAwake = True
        gc.collect()
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):        
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return

