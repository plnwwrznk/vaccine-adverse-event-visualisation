"""Parsing symptoms"""
import re
import pandas as pd


def unique_symptoms(column):
    """return unique symptoms in column with symptoms list"""
    return sorted(list(map(str, list(set({a for b in column.tolist() for a in b})))))


def parse_symptom_columns(dataset):
    """parse 5 symptoms columns into one list"""
    mylist = dataset[
        ["SYMPTOM1", "SYMPTOM2", "SYMPTOM3", "SYMPTOM4", "SYMPTOM5"]
    ].values.tolist()
    newlist = [[x for x in y if str(x) != "nan"] for y in mylist]
    return newlist


def list_matching_symptoms(symp_string, column):
    """return list of all symptoms containing provided string"""
    unique = unique_symptoms(column)
    reg = re.compile(".*" + symp_string + ".*")
    return list(filter(reg.match, unique))


def find_symptoms(symptom, symptoms):
    """check if symptoms contain provided string"""
    for sym in symptoms:
        if symptom in sym:
            return True
    return False


def find_most_frequent_symptoms(dataframe, num):
    """return num most frequent symptoms in given dataframe"""
    symptoms = pd.Series([a for b in dataframe["SYMPTOMS"] for a in b])
    symptoms = symptoms.value_counts().head(n=num)
    return symptoms
