# -*- coding: utf-8 -*-
from __future__ import annotations

from pioreactor.config import config
from pioreactor.automations.dosing.base import DosingAutomationJobContrib
from pioreactor.structs import DosingEvent
from msgspec.json import decode

__plugin_name__ = "pioreactor_as_sink"
__plugin_author__ = "Cam DP"
__plugin_summary__ = "This Pioreactors will be the sink for other Pioreactor's waste. This automation controls removing that waste."

class PioreactorAsSink(DosingAutomationJobContrib):

    automation_name = "pioreactor_as_sink"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.desired_volume = config.getfloat("bioreactor", "initial_volume_ml")

    def _update_dosing_metrics(self, message) -> None:
        dosing_event = decode(message.payload, type=DosingEvent)
        self._update_liquid_volume(dosing_event)

    def start_passive_listeners(self):
        super().start_passive_listeners()
        self.subscribe_and_callback(
            self._update_dosing_metrics,
            "pioreactor/+/+/dosing_events", # listen to any pioreactors dosing events and update.
        )

    def execute(self):
        if self.liquid_volume > self.desired_volume:
            self.execute_io_action(waste_ml=self.liquid_volume - self.desired_volume)
