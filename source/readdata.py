"""Reading from data files"""
# pylint: disable=E1101
import glob
from itertools import repeat
import pandas as pd
from source import parsesymptoms as symp


columns_data = [
    "VAERS_ID",
    "RECVDATE",
    "AGE_YRS",
    "SEX",
    "DIED",
    "ER_VISIT",
    "HOSPITAL",
    "HOSPDAYS",
    "VAX_DATE",
]
columns_vax = [
    "VAERS_ID",
    "VAX_TYPE",
    "VAX_NAME",
]
columns_symptoms = [
    "VAERS_ID",
    "SYMPTOM1",
    "SYMPTOM2",
    "SYMPTOM3",
    "SYMPTOM4",
    "SYMPTOM5",
]


def read_w_parameters(file, fields):
    """Read from multiple csv files selecting only provided column names
    Parameters
        ----------
        file : str
            name of the file
        fields : list
            List of column names
    Returns
        -------
        DataFrame
            dataframe containing selected columns from the file
    """
    return pd.read_csv(file, encoding="iso-8859-1", usecols=fields, low_memory=False)


def read_vax_data():
    """Function to load data from all vax files
    Returns
        -------
        DataFrame
            dataframe containing data from all the VAERS data in data folder"""

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
    vaerssymptoms["SYMPTOMS"] = symp.parse_symptom_columns(vaerssymptoms)
    data_vax1 = pd.merge(vaersdata, vaerssymptoms, on="VAERS_ID")
    data_vax1["check"] = data_vax1["SYMPTOMS"].map(
        lambda x: symp.find_symptoms("No adverse event", x)
    )
    data_vax2 = data_vax1[~data_vax1["check"]].drop("check", axis=1)
    data_vax = pd.merge(data_vax2, vaersvax, on="VAERS_ID")

    return data_vax
