import fhirclient.models.observation as ob
import fhirclient.models.meta as mt
import fhirclient.models.codeableconcept as cc
import fhirclient.models.fhirreference as ref
import fhirclient.models.fhirdate as fd
import fhirclient.models.resource as rs
import fhirclient.models.quantity as q
from datetime import datetime


class GlucoseGenerator:
    def __init__(self, p_id, n_id, val):
        self.p_id = p_id
        self.n_id = n_id
        self.val = val

    def get_result(self):
        self.__model = ob.Observation(self.init_value())
        self.__model.meta = self.meta()
        self.__model.category = self.category()
        self.__model.subject = self.subject()
        self.__model.effectiveDateTime = self.effective_date_time()
        self.__model.performer = self.performer()
        self.__model.device = self.device()
        self.__model.referenceRange = self.ref_range()
        self.__model.interpretation = self.interpretation()
        self.__model.valueQuantity = self.value()

        return self.__model

    def meta(self):
        return mt.Meta({"profile":
                        ["http://hl7.org/fhir/StructureDefinition/vitalsigns"]})

    def category(self):
        return [cc.CodeableConcept({
            "coding": [
                {
                    "system": "http://hl7.org/fhir/observation-category",
                    "code": "vital-signs",
                    "display": "Vital Signs"
                }
            ]
        })]

    def subject(self):
        return ref.FHIRReference({"reference": "Patient/{}".format(self.p_id)})

    def effective_date_time(self):
        return fd.FHIRDate(str(datetime.now()))

    def performer(self):
        return [ref.FHIRReference({"reference":
                                   "Practitioner/{}".format(self.n_id)})]

    def value(self):
        return q.Quantity({
            "value": float(self.val),
            "unit": "mmol/l",
            "system": "http://unitsofmeasure.org",
            "code": "mmol/L"
        })

    def ref_range(self):
        low = {"low": {
            "value": float(self.val),
            "unit": "mmol/l",
            "system": "http://unitsofmeasure.org",
            "code": "mmol/L"
        }}

        high = {"high": {
            "value": float(self.val),
            "unit": "mmol/l",
            "system": "http://unitsofmeasure.org",
            "code": "mmol/L"
        }}

        return [ob.ObservationReferenceRange(low),
                ob.ObservationReferenceRange(high)]

    def interpretation(self):
        return cc.CodeableConcept({
            "coding": [
                {
                    "system": "http://hl7.org/fhir/v2/0078",
                    "code": "H",
                    "display": "High"
                }
            ]
        })

    def device(self):
        return ref.FHIRReference({"reference": "DeviceMetric/manual"})

    def init_value(self):
        return {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "15074-8",
                        "display": "Glucose [Moles/volume] in Blood"
                    }
                ]
            },
            "status": "final"
        }
