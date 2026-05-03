import numpy as np
import pandas as pd
import cv2
import pytesseract
import spacy
import re
import string
import warnings

warnings.filterwarnings('ignore')

# Load trained NER model
model_ner = spacy.load('./output/model-best/')

# Clean raw text extracted by OCR
def cleanText(txt):
    whitespace = string.whitespace
    punctuation = "!#$%&'()*+:;<=>?[\\]^`{|}~"
    txt = str(txt)
    txt = txt.translate(str.maketrans('', '', whitespace))
    txt = txt.translate(str.maketrans('', '', punctuation))
    return txt.strip()

# Clean specific entity types
def parser(text, label):
    text = text.strip()
    if label == 'PHONE':
        text = re.sub(r'\D', '', text)
    elif label == 'EMAIL':
        text = re.sub(r'[^a-zA-Z0-9@._\-]', '', text)
    elif label == 'WEB':
        text = re.sub(r'[^a-zA-Z0-9:/._\-]', '', text)
    elif label in ('NAME', 'DES'):
        text = re.sub(r'[^a-zA-Z ]', '', text).title()
    elif label == 'ORG':
        text = re.sub(r'[^a-zA-Z0-9 &,.]', '', text).title()
    return text

# ID generator for bounding box grouping
class groupgen:
    def __init__(self):
        self.id = 0
        self.text = ''
    def getgroup(self, text):
        if self.text == text:
            return self.id
        else:
            self.id += 1
            self.text = text
            return self.id

grp_gen = groupgen()

def getPredictions(image):
    # --- OCR with tuned config ---
    custom_config = r'--oem 3 --psm 6'
    tess_data = pytesseract.image_to_data(image, config=custom_config, lang='eng')
    
    # --- Convert to DataFrame ---
    rows = list(map(lambda x: x.split('\t'), tess_data.strip().split('\n')))
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df = df[df['text'].notna()]
    df['text'] = df['text'].apply(cleanText)
    df = df.query('text != "" ').copy()

    # --- Join all clean text for NER model ---
    content = " ".join(df['text'])
    doc = model_ner(content)
    doc_json = doc.to_json()

    # --- Token Processing ---
    tokens_df = pd.DataFrame(doc_json['tokens'])
    tokens_df['token'] = tokens_df.apply(lambda x: doc_json['text'][x['start']:x['end']], axis=1)
    labels_df = pd.DataFrame(doc_json['ents'])[['start', 'label']]
    tokens_df = pd.merge(tokens_df, labels_df, how='left', on='start')
    tokens_df.fillna('O', inplace=True)

    # --- Match tokens back to OCR words using start offset logic ---
    df['end'] = df['text'].apply(lambda x: len(x)+1).cumsum() - 1
    df['start'] = df.apply(lambda x: x['end'] - len(x['text']), axis=1)
    merge_df = pd.merge(df, tokens_df[['start', 'token', 'label']], on='start', how='inner')

    # --- Bounding Box Setup ---
    merge_df = merge_df[merge_df['label'] != 'O'].copy()
    merge_df['label'] = merge_df['label'].apply(lambda x: x[2:])
    merge_df['group'] = merge_df['label'].apply(grp_gen.getgroup)

    for col in ['left', 'top', 'width', 'height']:
        merge_df[col] = merge_df[col].astype(int)
    merge_df['right'] = merge_df['left'] + merge_df['width']
    merge_df['bottom'] = merge_df['top'] + merge_df['height']

    # --- Aggregate Boxes by Group ---
    box_groups = merge_df.groupby('group').agg({
        'left': 'min',
        'top': 'min',
        'right': 'max',
        'bottom': 'max',
        'label': lambda x: x.unique()[0],
        'token': lambda x: ' '.join(x)
    }).reset_index()

    # --- Draw Boxes ---
    img_bb = image.copy()
    for _, row in box_groups.iterrows():
        l, t, r, b = int(row['left']), int(row['top']), int(row['right']), int(row['bottom'])
        label = row['label']
        cv2.rectangle(img_bb, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(img_bb, label, (l, t - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

    # --- Entity Aggregation ---
    entity_map = dict(NAME=[], ORG=[], DES=[], PHONE=[], EMAIL=[], WEB=[])
    prev_label = None
    for _, row in merge_df.iterrows():
        label = row['label']
        token = parser(row['token'], label)
        if label not in entity_map:
            continue
        if prev_label == label and label in ['NAME', 'ORG', 'DES']:
            entity_map[label][-1] += " " + token
        else:
            entity_map[label].append(token)
        prev_label = label

    return img_bb, entity_map
