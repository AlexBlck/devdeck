import logging
import os

from pulsectl import pulsectl

from devdeck_core.controls.deck_control import DeckControl


class VolumeLevelControl(DeckControl):

    def __init__(self, key_no, **kwargs):
        self.pulse = None
        self.volume = None
        self.__logger = logging.getLogger('devdeck')
        super().__init__(key_no, **kwargs)

    def initialize(self):
        if self.pulse is None:
            self.pulse = pulsectl.Pulse('VolumeLevelControl')
        self.volume = float(self.settings['volume']) / 100
        self.__render_icon()

    def pressed(self):
        outputs = self.__get_output()
        if outputs is None:
            return
        for output in outputs:
            self.pulse.volume_set_all_chans(output, self.volume)
        self.__render_icon()

    def __get_output(self):
        sinks = self.pulse.sink_list()
        return sinks

    def __render_icon(self):
        with self.deck_context() as context:
            sink = self.__get_output()[0]
            if sink is None:
                with context.renderer() as r:
                    r \
                        .text('OUTPUT \nNOT FOUND') \
                        .color('red') \
                        .center_vertically() \
                        .center_horizontally() \
                        .font_size(85) \
                        .text_align('center') \
                        .end()
                return

            with context.renderer() as r:
                r.text("{:.0f}%".format(round(self.volume, 2) * 100)) \
                    .center_horizontally() \
                    .end()
                r.image(os.path.join(os.path.dirname(__file__), "../assets/font-awesome", 'volume-up-solid.png')) \
                    .width(380) \
                    .height(380) \
                    .center_horizontally() \
                    .y(132) \
                    .end()
                if round(self.volume, 2) == round(sink.volume.value_flat, 2):
                    r.colorize('red')

    def settings_schema(self):
        return {
            'volume': {
                'type': 'integer'
            }
        }
