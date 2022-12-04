from . import filereader
import spacy
import os
import re

dirname = os.path.dirname(__file__)
model_path = os.path.join(dirname, "ner-models/model-best")
model = spacy.load(model_path)


def get_receipt_info_from_file(receipt_file):
    type, text = filereader.readFile(receipt_file)
    doc = model(text)
    ents = [{'text': ent.text, 'label': ent.label_}
            for ent in doc.ents]
    businessNameEnt = first(
        ents, lambda e: e['label'] == 'ORG')

    dateEnt = first(
        ents, lambda e: e['label'] == 'DATE')
    moneyEnts = list(filter(lambda e: e['label'] == 'MONEY', ents))
    parsedMoneyEnts = [amount for amount in map(
        lambda e: parseAmountText(e['text']), moneyEnts) if amount is not None]
    return {
        'business_name': businessNameEnt['text'] if businessNameEnt else receipt_file.name,
        'type': type,
        'date': dateEnt['text'] if dateEnt else None,
        'total': max(parsedMoneyEnts) if len(
            parsedMoneyEnts) > 0 else None,
        'text': text
    }


def parseAmountText(text):
    string_amount = re.sub(r"[$CADS\s]", "", text)
    if string_amount == "" or not string_amount.replace('.', '', 1).isnumeric():
        return None
    return float(string_amount)


def first(ls, filterFn):
    filteredList = list(filter(filterFn, ls))
    return filteredList[0] if len(
        filteredList) > 0 else None
