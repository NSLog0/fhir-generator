import fhirclient.models.observation as ob
import fhirclient.models.meta as mt
import fhirclient.models.codeableconcept as cc
import fhirclient.models.fhirreference as ref
import fhirclient.models.fhirdate as fd
import fhirclient.models.resource as rs
from datetime import datetime


class BloodPressureGenerator:
    def __init__(self, p_id, n_id, normal, low):
        self.p_id = p_id
        self.n_id = n_id
        self.normal = normal
        self.low = low

    def get_result(self):
        self.__model = ob.Observation(self.init_value())
        self.__model.meta = self.meta()
        self.__model.category = self.category()
        self.__model.subject = self.subject()
        self.__model.effectiveDateTime = self.effective_date_time()
        self.__model.performer = self.performer()
        self.__model.component = self.component()
        self.__model.device = self.device()

        return self.__model

    def meta(self):
        return mt.Meta({"profile":
                        ["http://hl7.org/fhir/StructureDefinition/vitalsigns"]})

    def profile(self):
        return {"profile": ["http://hl7.org/fhir/StructureDefinition/vitalsigns"]}

    def category(self):
        return [cc.CodeableConcept({
            "coding": [{
                "system": "http://hl7.org/fhir/observation-category",
                "code": "vital-signs",
                "display": "Vital Signs"
            }]
        })]

    def subject(self):
        return ref.FHIRReference({"reference": "Patient/{}".format(self.p_id)})

    def effective_date_time(self):
        return fd.FHIRDate(str(datetime.now()))

    def performer(self):
        return [ref.FHIRReference({"reference":
                                   "Practitioner/{}".format(self.n_id)})]

    def component(self):
        interpre_low = cc.CodeableConcept({
            "coding": [{
                "system": "http://hl7.org/fhir/v2/0078",
                "code": "L",
                "display": "low"
            }],
            "text": "Below low normal"
        })

        interpre_normal = cc.CodeableConcept({
            "coding": [{
                "system": "http://hl7.org/fhir/v2/0078",
                "code": "N",
                "display": "normal"
            }],
            "text": "Normal"
        })

        code_normal = cc.CodeableConcept({
            "coding": [{
                "system": "http://loinc.org",
                "code": "8480-6",
                "display": "Systolic blood pressure"
            }, {
                "system": "http://snomed.info/sct",
                "code": "271649006",
                "display": "Systolic blood pressure"
            }, {
                "system": "http://acme.org/devices/clinical-codes",
                "code": "bp-s",
                "display": "Systolic Blood pressure"
            }]
        })

        code_low = cc.CodeableConcept({
            "coding": [{
                "system": "http://loinc.org",
                "code": "8462-4",
                "display": "Diastolic blood pressure"
            }]
        })

        v1 = ob.ObservationComponent({
            "valueQuantity": {
                "value": float(self.normal),
                "unit": "mmHg",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]"
            },
            "code": code_normal.as_json(),
            "interpretation": interpre_normal.as_json()
        })

        v2 = ob.ObservationComponent({
            "valueQuantity": {
                "value": float(self.low),
                "unit": "mmHg",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]"
            },
            "code": code_low.as_json(),
            "interpretation": interpre_low.as_json()
        })

        return [v1, v2]

    def device(self):
        return ref.FHIRReference({"reference": "DeviceMetric/manual"})

    def init_value(self):
        return {
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "85354-9",
                    "display": "Bood pressure panel with all children optional"
                }],
                "text": "Blood pressure systolic & diastolic"
            },
            "status": "final"
        }
