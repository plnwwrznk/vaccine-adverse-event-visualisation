"""Testing methods in paersesympthoms"""
import pandas as pd
from source.parsesymptoms import (
    find_symptoms,
    unique_symptoms,
    parse_symptom_columns,
    list_matching_symptoms,
)


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
                "SYMPTOM3": "high blood pressure",
                "SYMPTOM4": "fever",
                "SYMPTOM5": "sadness",
            },
            index=[0],
        )
    )
    assert result2 == [
        ["headache", "back pain", "high blood pressure", "fever", "sadness"]
    ]


def test_find_sympthoms():
    """test of find_SYMPTHOMS"""
    find = find_symptoms("headache", ["headache", "back pain", "high blood pressure"])
    assert find is True


# def test_find_most_frequent_symptoms():
#     """"test of find_most_frequent_symptoms"""
#     frame = pd.DataFrame({"SYMPTOMS": ("headache", "back pain", "high blood pressure",
#     "fever", "sadness", "headache")})
#     find_most_frequent = find_most_frequent_symptoms(frame, 1)
#     assert find_most_frequent == ("headache", 2)


def test_list_matching_symptoms():
    """test of list_matching_symptoms"""
    data = pd.DataFrame(["headache", "back pain", "high blood pressure"]).values
    result = list_matching_symptoms("headache", data)
    assert result == ["headache"]
