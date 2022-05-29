"""Reading from data files"""
# pylint: disable=E1101
import glob
from itertools import repeat
import pandas as pd


def read_w_parameters(file, fields):
    """function to read from multiple csv files with parameters"""
    return pd.read_csv(file, encoding="iso-8859-1", usecols=fields, low_memory=False)


columns_data = [
    "VAERS_ID",
    "RECVDATE",
    "STATE",
    "AGE_YRS",
    "SEX",
    "DIED",
    "DATEDIED",
    "L_THREAT",
    "ER_VISIT",
    "HOSPITAL",
    "HOSPDAYS",
    "VAX_DATE",
    "ONSET_DATE",
    "NUMDAYS",
    "CUR_ILL",
    "PRIOR_VAX",
    "ALLERGIES",
]
columns_vax = [
    "VAERS_ID",
    "VAX_TYPE",
    "VAX_MANU",
    "VAX_LOT",
    "VAX_DOSE_SERIES",
    "VAX_ROUTE",
    "VAX_SITE",
    "VAX_NAME",
]
columns_symptoms = [
    "VAERS_ID",
    "SYMPTOM1",
    "SYMPTOMVERSION1",
    "SYMPTOM2",
    "SYMPTOMVERSION2",
    "SYMPTOM3",
    "SYMPTOMVERSION3",
    "SYMPTOM4",
    "SYMPTOMVERSION4",
    "SYMPTOM5",
    "SYMPTOMVERSION5",
]


def read_vax_data():
    """function to load data from vax files"""

    vaersdata = pd.concat(
        map(read_w_parameters, glob.glob("data/*VAERSDATA.csv"), repeat(columns_data)),
        ignore_index=True,
    )
    vaersdata["RECVDATE"] = pd.to_datetime(vaersdata["RECVDATE"])
    vaersdata["RECVYEAR"] = pd.DatetimeIndex(vaersdata["RECVDATE"]).year

    vaersvax = (
        pd.concat(
            map(
                read_w_parameters, glob.glob("data/*VAERSVAX.csv"), repeat(columns_vax)
            ),
            ignore_index=True,
        )
        .replace({"VAX_NAME": r"\(SEASONAL\)"}, {"VAX_NAME": "SEASONAL"}, regex=True)
        .replace({"VAX_NAME": r"\(H1N1\)"}, {"VAX_NAME": "H1N1"}, regex=True)
        .replace(
            {"VAX_NAME": r"\(H1N1 \(MONOVALENT\)"},
            {"VAX_NAME": "MONOVALENT"},
            regex=True,
        )
        .replace({"VAX_NAME": r"\(COVID19"}, {"VAX_NAME": ""}, regex=True)
        .replace({"VAX_NAME": r"\)\)"}, {"VAX_NAME": ")"}, regex=True)
    )
    vaersvax["BRAND"] = (
        vaersvax["VAX_NAME"].replace(regex={r".* \(": ""}).replace(regex={r"\)": ""})
    )
    vaersvax["VAX_TYPE"] = vaersvax["VAX_NAME"].replace(regex={r" \(.*\)$": ""})

    vaerssymptoms = pd.concat(
        map(
            read_w_parameters,
            glob.glob("data/*VAERSSYMPTOMS.csv"),
            repeat(columns_symptoms),
        ),
        ignore_index=True,
    )
    data_vax1 = pd.merge(vaersdata, vaerssymptoms, on="VAERS_ID")
    data_vax = pd.merge(data_vax1, vaersvax, on="VAERS_ID")

    return data_vax
