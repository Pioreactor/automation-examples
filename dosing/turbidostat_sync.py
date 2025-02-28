from pioreactor.automations.dosing import Turbidostat
from pioreactor.pubsub import post_into
from pioreactor.utils.networking import resolve_to_address



class TurbidostatSync(Turbidostat):
    """
    Whenever this Pioreactor doses, it will trigger another Pioreactor to dose. 
    This is to compare growth rates relatively: if the other Pioreactor's culture vanishes, then it has a lower gr. Otherwise, a equal or higher gr. 

    """

    automation_name="turbidostat_sync"

    def __init__(self, other_worker: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.other_worker = other_worker


    def add_media_to_bioreactor(self, unit, experiment, ml, source_of_event, mqtt_client, logger):
        v = super().add_media_to_bioreactor(unit=unit, experiment=experiment, ml=ml, source_of_event=source_of_event, mqtt_client=mqtt_client, logger=logger)
        data = {
            "options": {"ml": ml},
            "env": {"JOB_SOURCE": f"{self.unit}/{self.job_name}"},
            "args": [],
        }
        post_into(resolve_to_address(self.other_worker), "/unit_api/jobs/run/job_name/add_media", json=data)
        return v
    
    def remove_waste_from_bioreactor(self, unit, experiment, ml, source_of_event, mqtt_client, logger):
        v = super().remove_waste_from_bioreactor(unit=unit, experiment=experiment, ml=ml, source_of_event=source_of_event, mqtt_client=mqtt_client, logger=logger)
        data = {
            "options": {"ml": ml},
            "env": {"JOB_SOURCE": f"{self.unit}/{self.job_name}"},
            "args": [],
        }
        post_into(resolve_to_address(self.other_worker), "/unit_api/jobs/run/job_name/remove_waste", json=data)
        return v
