"""Parsing symptoms"""
import re
import pandas as pd


def unique_symptoms(column):
    """Return unique symptoms from symptoms list
    Parameters
        ----------
        column : dataframe
            dataframe with one column containing symptoms lists
    Returns
        -------
        list
            list containing unique symptoms"""
    return sorted(list(map(str, list(set({a for b in column.tolist() for a in b})))))


def parse_symptom_columns(dataset):
    """Parse 5 symptoms columns into one list from the provided dataset

    Parameters
        ----------
        dataset : DataFrame
            dataframe containing 5 columns with symptoms
    Returns
        -------
        List
            list containing symptoms concatenated to lists"""
    mylist = dataset[
        ["SYMPTOM1", "SYMPTOM2", "SYMPTOM3", "SYMPTOM4", "SYMPTOM5"]
    ].values.tolist()
    newlist = [[x for x in y if str(x) != "nan"] for y in mylist]
    return newlist


def list_matching_symptoms(symp_string, column):
    """return list of all symptoms containing provided string from the provided column
    Parameters
        ----------
        symp_string : string
            String used to match the symptoms
        column : dataframe
            dataframe with one column containing lists of symptoms
    Returns
        -------
        List
            list containing symptoms matching the provided string"""
    unique = unique_symptoms(column)
    reg = re.compile(".*" + symp_string + ".*")
    return list(filter(reg.match, unique))


def find_symptoms(symptom, symptoms):
    """check if symptoms list contain provided symptom
        Parameters
        ----------
        symptom : string
            name of the searched symptom
        symptoms : list
            list of symptoms
    Returns
        -------
        Boolean
            returns true if the symptom is found in list"""
    for sym in symptoms:
        if symptom in sym:
            return True
    return False


def find_most_frequent_symptoms(dataframe, num):
    """return most frequent symptoms in given dataframe
    Parameters
        ----------
        dataframe : DataFrame
            dataframe with symptoms column
        num : integer
            number of symptoms to be returned
    Returns
        -------
        Series
            series containing most frequent symptoms names with occurence counts"""
    symptoms = pd.Series([a for b in dataframe["SYMPTOMS"] for a in b])
    symptoms = (
        symptoms.value_counts()
        .head(n=num)
        .rename_axis("symptom")
        .reset_index(name="count")
    )
    return symptoms
