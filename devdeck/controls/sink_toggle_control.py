import logging
import os
import numpy as np
from pulsectl import pulsectl

from devdeck_core.controls.deck_control import DeckControl


class SinkToggleControl(DeckControl):

    def __init__(self, key_no, **kwargs):
        # self.names = ['Built-in Audio Analog Stereo', 'PCM2902 Audio Codec Analog Stereo']
        self.pulse = None
        self.sinks = None
        self.active_device = None
        self.__logger = logging.getLogger('devdeck')
        super().__init__(key_no, **kwargs)

    def initialize(self):
        if self.pulse is None:
            self.pulse = pulsectl.Pulse('SinkToggleControl')

        self.sinks = self.pulse.sink_list()
        self.active_device = [s for s in self.sinks if s.name == self.pulse.server_info().default_sink_name][0]
        self.old_id = np.where([s == self.active_device for s in self.sinks])[0][0]
        self.__render_icon()

    def pressed(self):
        self.sinks = self.pulse.sink_list()
        print([s for s in self.sinks])

        new_id = (self.old_id + 1) % len(self.sinks)
        new_device = self.sinks[new_id]
        self.old_id = new_id
        self.pulse.default_set(new_device)
        self.active_device = new_device
        self.__render_icon()

    def __get_mic(self):
        sources = self.pulse.source_list()

        return sources

    def __render_icon(self):
        with self.deck_context() as context:
            mic = self.__get_mic()[0]

            with context.renderer() as r:
                r \
                    .text(self.active_device.description.replace(' ', '\n')) \
                    .color('white') \
                    .center_vertically() \
                    .center_horizontally() \
                    .font_size(85) \
                    .text_align('center') \
                    .end()
            # if mic.mute == 0:
            #     with context.renderer() as r:
            #         r.image(os.path.join(os.path.dirname(__file__), "../assets/font-awesome", 'microphone.png')).end()
            # else:
            #     with context.renderer() as r:
            #         r.image(os.path.join(os.path.dirname(__file__), "../assets/font-awesome", 'microphone-mute.png')).end()

    def settings_schema(self):
        return {
        }
