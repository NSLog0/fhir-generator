# -*- coding: utf-8 -*-
import json
import os.path

from .oximiterGenerator import OximiterGenerator as ox
from .heartRateGenerator import HeartRateGenerator as hr
from .bloodPressureGenerator import BloodPressureGenerator as bp
from .glucoseGenerator import GlucoseGenerator as gl
from .respiratoryGenerator import RespiratoryGenerator as rs
from .temperatureGenerator import TemperatureGenerator as tm
from .avpuGenerator import AVPUGenerator as avpu


def build(values):
    val = values
    if type(values) is bytes:
        val = json.loads(values.decode("ASCII"))

    rpath = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(rpath, 'templates/bundle_upload.json')

    with open(file) as f:
        data = json.load(f)

    arrs = []
    if 'oximiter' in val:
        arrs.append({"resource": ox(val['patientId'], val['practtionerId'],
                                    val['oximiter']).get_result().as_json()})

    if 'heartRate' in val:
        arrs.append({"resource": hr(val['patientId'], val['practtionerId'],
                                    val['heartRate']).get_result().as_json()})

    if 'glucose' in val:
        arrs.append({"resource": gl(val['patientId'], val['practtionerId'],
                                    val['glucose']).get_result().as_json()})

    if 'bloodPressure' in val:
        arrs.append({"resource": bp(val['patientId'], val['practtionerId'],
                                    val['bloodPressure']['normal'],
                                    val['bloodPressure']['low']).get_result().as_json()})
    if 'temperature' in val:
        arrs.append({"resource": tm(val['patientId'], val['practtionerId'],
                                    val['temperature']).get_result().as_json()})

    if 'respiratory' in val:
        arrs.append({"resource": rs(val['patientId'], val['practtionerId'],
                                    val['respiratory']).get_result().as_json()})
    if 'avpu' in val:
        arrs.append({"resource": avpu(val['patientId'], val['practtionerId'],
                                      val['avpu']).get_result().as_json()})

    data['entry'] = arrs

    return data
