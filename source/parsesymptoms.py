"""Parsing symptoms"""
import re


def unique_symptoms(column):
    """return unique symptoms in column with symptoms list"""
    return sorted(list(map(str, list(set([a for b in column.tolist() for a in b])))))


def parse_symptom_columns(dataset):
    """parse 5 symptoms columns into one list"""
    mylist = dataset[["SYMPTOM1", "SYMPTOM2", "SYMPTOM3", "SYMPTOM4", "SYMPTOM5"]].values.tolist()
    newlist = [[x for x in y if str(x) != 'nan'] for y in mylist]
    return newlist


def parse_symptom_columns_str(dataset):
    """parse 5 symptoms columns into one string"""
    mylist = parse_symptom_columns(dataset)
    newlist = [", ".join(y) for y in mylist]
    return newlist


def list_matching_symptoms(symp_string, column):
    """return list of all symptoms containing provided string"""
    unique = unique_symptoms(column)
    r = re.compile(".*"+symp_string+".*")
    return list(filter(r.match, unique))


def find_symptoms(symptom, symptoms_string):
    """check if symptoms contain provided string"""
    return symptom in symptoms_string


