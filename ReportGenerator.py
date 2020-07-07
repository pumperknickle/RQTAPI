import spacy
import en_core_web_sm
from DetectionEngine import get_adverbs, get_passives, get_infinitives, get_pronouns, get_indefinite_articles, \
    get_vague_adjectives, get_escape_clauses, get_comparators, get_open_ended_clauses, get_vague_quantifiers, \
    get_universal_quantifiers, get_obliques
from spacy import displacy
import sys
from pathlib import Path
import os
import docx
import codecs


def getTextFromDoc(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return "\n".join(fullText)


nlp = en_core_web_sm.load()
dirname = sys.argv[1]
texts = []
metrics = []
total_words = 0
total_matches = 0
all_match_ents = []

for path in Path(dirname).rglob('*'):
    if path.is_file() and not (os.path.basename(path).startswith('.')) and not (
            os.path.basename(path) == 'RQT_report.html') and not (os.path.basename(path).endswith('html')):
        if path.suffix == ".docx":
            doc_texts = getTextFromDoc(path)
            texts.append((doc_texts, path))
            continue
        with codecs.open(path, 'r', encoding='utf-8',
                         errors='ignore') as f:
            inputText = f.read()
            texts.append((inputText, path))

for inputText, reqPath in texts:
    requirements = inputText.split('\n')
    filteredReqs = list(filter(lambda x: len(x.strip()) != 0, requirements))
    total_words += len(inputText.split())
    for i in range(len(filteredReqs)):
        req = filteredReqs[i]
        infinitiveMatches = get_infinitives(nlp(req))
        total_matches += len(infinitiveMatches)
        file_match_ents = []
        for match in infinitiveMatches:
            print(match)
            file_match_ents.append({
                "start": match["start"],
                "end": match["end"],
                "label": "INFINITIVE",
            })
        all_match_ents.append({"text": req, "ents": file_match_ents.copy(), "title": str(reqPath) + " " + str(i + 1)})

metricsText = "Out of " + str(total_words) + " words, " + str(total_matches) + " potential ambiguities were detected."
metrics.append({"text": metricsText, "ents": [], "title": "Metrics"})

options = {"colors": {"INFINITIVE": "yellow"}}

html = displacy.render(metrics + all_match_ents, style="ent", manual=True, page=True, options=options)
filename = 'RQT_report.html'
file_path = os.path.join(dirname, filename)
with open(file_path, 'w') as file:
  file.write(html)

