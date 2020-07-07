import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import en_core_web_sm

spacy.prefer_gpu()
nlp = en_core_web_sm.load()

def get_matches(matcher, doc):
    matches = matcher(doc)
    match_ents = []
    for match_id, start, end in matches:
        start_idx = get_character_indices(doc[start])
        end_idx = get_character_indices(doc[end - 1])
        match_ents.append({
            "start": start_idx[0],
            "end": end_idx[1]
        })
    return match_ents

def get_character_indices(start_token):
    start = start_token.idx
    end = start_token.idx + len(start_token)
    return (start, end)

# def rule_based_matching(doc, match_adverbs = False, match_passives = False, match_infinitives = False, match_pronouns = False, match_comparators = False):
#     matcher = Matcher(nlp.vocab)
#     if match_adverbs:
#         adverbPattern = [{"POS": "ADV", "ORTH": {"REGEX": "\w+ly"}}]
#         matcher.add("Adverbs", None, adverbPattern)
#     if match_passives:
#         passivePattern1 = [{"LEMMA": "be"}, {"TAG": "VBD"}]
#         passivePattern2 = [{"LEMMA": "be"}, {"TAG": "VBN"}]
#         matcher.add("Passive", None, passivePattern1, passivePattern2)
#     if match_infinitives:
#         infinitivePattern1 = [{"LOWER": "be"}, {"POS": "ADJ"}, {"POS": "ADP"}]
#         infinitivePattern2 = [{"LOWER": "to"}, {"POS": "VERB"}]
#         matcher.add("Infinitive", None, infinitivePattern1, infinitivePattern2)
#     if match_pronouns:
#         pronounPattern = [{"POS": "PRON"}]
#         matcher.add("Pronoun", None, pronounPattern)
#     if match_comparators:
#         comparatorPattern1 = [{"ORTH": {"REGEX": "\w+er"}}, {"LOWER": "than"}]
#         comparatorPattern2 = [{"LOWER": "less"}, {"LOWER": "than"}]
#         comparatorPattern3 = [{"LOWER": "more"}, {"LOWER": "than"}]
#         comparatorPattern4 = [{"LOWER": "maximum"}]
#         comparatorPattern5 = [{"LOWER": "minimum"}]
#         comparatorPattern6 = [{"LOWER": "over"}]
#         matcher.add("Comparator", None, comparatorPattern1, comparatorPattern2, comparatorPattern3, comparatorPattern4,
#                     comparatorPattern5, comparatorPattern6)
#     return get_matches(matcher, doc)

def get_adverbs(doc):
    matcher = Matcher(nlp.vocab)
    adverbPattern = [{"POS": "ADV", "ORTH": {"REGEX": "\w+ly"}}]
    matcher.add("Adverbs", None, adverbPattern)
    return get_matches(matcher, doc)

def get_passives(doc):
    matcher = Matcher(nlp.vocab)
    passivePattern1 = [{"LEMMA": "be"}, {"TAG": "VBD"}]
    passivePattern2 = [{"LEMMA": "be"}, {"TAG": "VBN"}]
    matcher.add("Passive", None, passivePattern1, passivePattern2)
    return get_matches(matcher, doc)

def get_infinitives(doc):
    matcher = Matcher(nlp.vocab)
    infinitivePattern1 = [{"LOWER": "be"}, {"POS": "ADJ"}, {"POS": "ADP"}]
    infinitivePattern2 = [{"LOWER": "to"}, {"POS": "VERB"}]
    matcher.add("Infinitive", None, infinitivePattern1, infinitivePattern2)
    return get_matches(matcher, doc)

def get_pronouns(doc):
    matcher = Matcher(nlp.vocab)
    pronounPattern = [{"POS": "PRON"}]
    matcher.add("Pronoun", None, pronounPattern)
    return get_matches(matcher, doc)

def get_indefinite_articles(doc):
    phraseMatcher = PhraseMatcher(nlp.vocab, attr="LEMMA")
    indefiniteArticles = ["a", "an"]
    indefiniteArticlePatterns = [nlp(text) for text in indefiniteArticles]
    phraseMatcher.add("Indefinite Articles", None, *indefiniteArticlePatterns)
    return get_matches(phraseMatcher, doc)

def get_vague_adjectives(doc, vague_adjectives = ["ancillary", "relevant", "routine", "common", "generic", "significant", "flexible", "expandable", "typical", "sufficient", "adequate", "appropriate", "efficient", "effective", "proficient", "reasonable", "customary"]):
    phraseMatcher = PhraseMatcher(nlp.vocab, attr="LEMMA")
    vagueAdjectivePatterns = [nlp(text) for text in vague_adjectives]
    phraseMatcher.add("Vague Adjectives", None, *vagueAdjectivePatterns)
    return get_matches(phraseMatcher, doc)

def get_escape_clauses(doc, escape_clauses = ["greater than", "so far as is possible", "as possible", "as little as possible", "where possible", "as much as possible", "if it should prove necessary", "if necessary", "to the extent necessary", "as appropriate", "as required", "to the extent practical", "if practicable"]):
    phraseMatcher = PhraseMatcher(nlp.vocab, attr="LEMMA")
    escapeClausesPatterns = [nlp(text) for text in escape_clauses]
    phraseMatcher.add("Escape Clauses", None, *escapeClausesPatterns)
    return get_matches(phraseMatcher, doc)

def get_comparators(doc):
    matcher = Matcher(nlp.vocab)
    comparatorPattern1 = [{"ORTH": {"REGEX": "\w+er"}}, {"LOWER": "than"}]
    comparatorPattern2 = [{"LOWER": "less"}, {"LOWER": "than"}]
    comparatorPattern3 = [{"LOWER": "more"}, {"LOWER": "than"}]
    comparatorPattern4 = [{"LOWER": "maximum"}]
    comparatorPattern5 = [{"LOWER": "minimum"}]
    comparatorPattern6 = [{"LOWER": "over"}]
    matcher.add("Comparator", None, comparatorPattern1, comparatorPattern2, comparatorPattern3, comparatorPattern4, comparatorPattern5, comparatorPattern6)
    return get_matches(matcher, doc)

def get_open_ended_clauses(doc, open_ended_clauses = ["including but not limited to", "etc", "and so on"]):
    phraseMatcher = PhraseMatcher(nlp.vocab, attr="LEMMA")
    openEndedPatterns = [nlp(text) for text in open_ended_clauses]
    phraseMatcher.add("Open Ended Clauses", None, *openEndedPatterns)
    return get_matches(phraseMatcher, doc)

def get_not_terms(doc, not_terms = ["not"]):
    phraseMatcher = PhraseMatcher(nlp.vocab, attr="LEMMA")
    notPatterns = [nlp(text) for text in not_terms]
    phraseMatcher.add("Negations", None, *notPatterns)

def get_vague_quantifiers(doc, vague_quantifiers = ["allowable", "completely", "prompt", "fast", "minimum", "maximum", "optimum", "some"]):
    exactMatcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    vagueQuantifiersPatterns = [nlp(text) for text in vague_quantifiers]
    exactMatcher.add("Vague Quantifiers", None, *vagueQuantifiersPatterns)
    return get_matches(exactMatcher, doc)

def get_universal_quantifiers(doc, universal_quantifiers =  ["both", "any", "all"]):
    exactMatcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    universalPatterns = [nlp(text) for text in universal_quantifiers]
    exactMatcher.add("Universal Quantifiers", None, *universalPatterns)
    return get_matches(exactMatcher, doc)

def get_obliques(doc):
    exactMatcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    obliques = ["/"]
    obliquePatterns = [nlp(text) for text in obliques]
    exactMatcher.add("Obliques", None, *obliquePatterns)
    return get_matches(exactMatcher, doc)

def get_temporal_dependencies(doc, temporal_dependencies=["eventually", "before", "when", "after", "as", "once", "earliest", "latest", "instantaneous", "simultaneous", "while", "at last"]):
    phraseMatcher = PhraseMatcher(nlp.vocab, attr="LEMMA")
    temporalPatterns = [nlp(text) for text in temporal_dependencies]
    phraseMatcher.add("Temporal Dependencies", None, *temporalPatterns)
    return get_matches(phraseMatcher, doc)