import fhirclient.models.observation as ob
import fhirclient.models.meta as mt
import fhirclient.models.codeableconcept as cc
import fhirclient.models.fhirreference as ref
import fhirclient.models.fhirdate as fd
import fhirclient.models.resource as rs
import fhirclient.models.quantity as q
import fhirclient.models.identifier as idn

from datetime import datetime


class AVPUGenerator:
    def __init__(self, p_id, n_id, val):
        self.p_id = p_id
        self.n_id = n_id
        self.val = val

    def get_result(self):
        self.__model = ob.Observation(self.init_value())
        self.__model.meta = self.meta()
        self.__model.category = [self.category()]
        self.__model.valueCodeableConcept = self.value_codeable_concept()
        self.__model.subject = self.subject()
        self.__model.effectiveDateTime = self.effective_date_time()
        self.__model.performer = self.performer()
        self.__model.device = self.device()
        self.__model.code = self.code()

        return self.__model

    def identifier(self):
        return idn.Identifier(
            {
                "use": "official",
                "system": "http://hl7.org/fhir/sid/us-ssn",
                "value": "xxxxx"
            }
        )

    def value_codeable_concept(self):
        return cc.CodeableConcept({
            "coding": [self.mapping(self.val.lower())]
        })

    def meta(self):
        return mt.Meta({"profile":
                        ["http://hl7.org/fhir/StructureDefinition/vitalsigns"]})

    def subject(self):
        return ref.FHIRReference({"reference": "Patient/{}".format(self.p_id)})

    def effective_date_time(self):
        return fd.FHIRDate(str(datetime.now()))

    def performer(self):
        return [ref.FHIRReference({"reference":
                                   "Practitioner/{}".format(self.n_id)})]

    def device(self):
        return ref.FHIRReference({"reference": "DeviceMetric/example"})

    def code(self):
        return cc.CodeableConcept({
            "coding": [
                {
                    "system": "https://r.details.loinc.org/LOINC",
                    "code": "67775-7",
                    "display": "Level of responsiveness"
                }
            ],
            "text": "Level of responsiveness"
        })

    def category(self):
        return cc.CodeableConcept({
            "coding": [
                {
                    "system": "http://hl7.org/fhir/observation-category",
                    "code": "activity",
                    "display": "Activity"
                }
            ],
            "text": "Activity"
        })

    def init_value(self):
        return {
            "code": {
                "coding": [
                    {
                        "system": "https://r.details.loinc.org/LOINC",
                        "code": "67775-7",
                        "display": "Level of responsiveness"
                    }
                ]
            },
            "status": "final"
        }

    def mapping(self, key):
        return {
            "alert": {
                "system": "http://snomed.info/sct",
                "code": "3326001",
                "display": "Alert"
            },
            "verbal": {
                "system": "http://snomed.nfo/sct",
                "code": "3326003",
                "display": "Verbal"
            },
            "pain": {
                "system": "http://snomed.info/sct",
                "code": "3326005",
                "display": "Painful"
            },
            "unresponsive": {
                "system": "http://snomed.info/sct",
                "code": "3326007",
                "display": "Unresponsive"
            },
            "uncheck": {
                "system": "http://snomed.info/sct",
                "code": "unknow",
                "display": "Uncheck"
            }
        }[key]
