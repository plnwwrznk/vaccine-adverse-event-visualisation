"""Testing methods in paersesympthoms"""
import pandas as pd
from source.parsesymptoms import find_symptoms, unique_symptoms, parse_symptom_columns


def test_unique_symptoms():
    """test of unique_symptoms()"""
    result = unique_symptoms(
        pd.DataFrame(["sympthom1", "sympthom1", "sympthom2"]).values
    )
    assert result == ["sympthom1", "sympthom2"]


def test_parse_symptom_columns():
    """test of parse_symptom_columns()"""
    result2 = parse_symptom_columns(
        pd.DataFrame(
            {
                "SYMPTOM1": "headache",
                "SYMPTOM2": "back pain",
                "SYMPTOM3": "high blood presure",
                "SYMPTOM4": "fever",
                "SYMPTOM5": "sadness",
            },
            index=[0],
        )
    )
    assert result2 == [
        ["headache", "back pain", "high blood presure", "fever", "sadness"]
    ]


def test_find_sympthoms():
    """test of find_SYMPTHOMS"""
    find = find_symptoms("headache", ["headache", "back pain", "high blood pressure"])
    assert find is True
