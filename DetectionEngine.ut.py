import unittest
import spacy
import en_core_web_sm
from DetectionEngine import get_adverbs, get_passives, get_infinitives, get_pronouns, get_indefinite_articles, get_vague_adjectives, get_escape_clauses, get_comparators, get_open_ended_clauses, get_vague_quantifiers, get_universal_quantifiers, get_obliques

class TestDetection(unittest.TestCase):
    def setUp(self):
        self.nlp = en_core_web_sm.load()

    def test_that_detecting_adverbs_works(self):
        testSentence = "I was walking quickly and slowly"
        testDoc = self.nlp(testSentence)
        testSentenceMatches = get_adverbs(testDoc)
        self.assertEqual(testSentenceMatches[0]["start"], 14)
        self.assertEqual(testSentenceMatches[0]["end"], 21)
        self.assertEqual(testSentenceMatches[1]["start"], 26)
        self.assertEqual(testSentenceMatches[1]["end"], 32)

    def test_that_detecting_passive_works(self):
        unacceptableSentence1 = "The identity of the customer shall be confirmed"
        unacceptableSentence2 = "The audio shall be recorded by the system"
        unacceptableSentence3 = "The audio shall be recorded"
        acceptableSentence1 = "The accounting system shall confirm the customer identity"
        acceptableSentence2 = "The system shall record the audio feed"
        self.assertGreater(len(get_passives(self.nlp(unacceptableSentence1))), 0)
        self.assertGreater(len(get_passives(self.nlp(unacceptableSentence2))), 0)
        self.assertGreater(len(get_passives(self.nlp(unacceptableSentence3))), 0)
        self.assertEqual(len(get_passives(self.nlp(acceptableSentence1))), 0)
        self.assertEqual(len(get_passives(self.nlp(acceptableSentence2))), 0)

    def test_that_detecting_infinitives_works(self):
        unacceptableSentence = "The weapon subsystem shall be able to store the location of each ordnance."
        acceptableSentence = "The weapon subsystem shall store the location of each ordnance."
        self.assertGreater(len(get_infinitives(self.nlp(unacceptableSentence))), 0)
        self.assertEqual(len(get_infinitives(self.nlp(acceptableSentence))), 0)

    def test_that_detecting_pronouns_works(self):
        unacceptableSentence = "The controller shall send the driver his itinrary for the day. It shall be delivered at least 8 hours prior to his shift."
        acceptableSentence = "The controller shall send the driver iterary for the day to the driver less than 8 hours prior to the driver shift."
        self.assertGreater(len(get_pronouns(self.nlp(unacceptableSentence))), 0)
        self.assertEqual(len(get_passives(self.nlp(acceptableSentence))), 0)

    def test_that_detecting_indefinite_articles_works(self):
        unacceptableSentence = "The system shall provide a time display"
        acceptableSentence = "The system shall display the current time"
        self.assertGreater(len(get_indefinite_articles(self.nlp(unacceptableSentence))), 0)
        self.assertEqual(len(get_indefinite_articles(self.nlp(acceptableSentence))), 0)

    def test_vague_adjectives(self):
        unacceptableSentence = "The system shall provide a relevant time display"
        acceptableSentence = "The system shall display the current time"
        self.assertGreater(len(get_vague_adjectives(self.nlp(unacceptableSentence))), 0)
        self.assertEqual(len(get_vague_adjectives(self.nlp(acceptableSentence))), 0)

    def test_escape_clauses(self):
        unacceptableSentence = "The system shall provide a time display so far as possible"
        acceptableSentence = "The system shall display the current time"
        self.assertGreater(len(get_escape_clauses(self.nlp(unacceptableSentence))), 0)
        self.assertEqual(len(get_escape_clauses(self.nlp(acceptableSentence))), 0)

    def test_comparators(self):
        unacceptableSentence = "The system shall provide more than 10 hours"
        acceptableSentence = "The system shall display the current time"
        self.assertGreater(len(get_comparators(self.nlp(unacceptableSentence))), 0)
        self.assertEqual(len(get_comparators(self.nlp(acceptableSentence))), 0)

    def test_open_ended_clauses(self):
        unacceptableSentence = "The system shall provide more etc"
        acceptableSentence = "The system shall display the current time"
        self.assertGreater(len(get_open_ended_clauses(self.nlp(unacceptableSentence))), 0)
        self.assertEqual(len(get_open_ended_clauses(self.nlp(acceptableSentence))), 0)

    def test_vague_quantifiers(self):
        unacceptableSentence = "The system shall provide allowable time"
        acceptableSentence = "The system shall display the current time"
        self.assertGreater(len(get_vague_quantifiers(self.nlp(unacceptableSentence))), 0)
        self.assertEqual(len(get_vague_quantifiers(self.nlp(acceptableSentence))), 0)

    def test_universal_quantifiers(self):
        unacceptableSentence = "The system shall provide all time"
        acceptableSentence = "The system shall display the current time"
        self.assertGreater(len(get_universal_quantifiers(self.nlp(unacceptableSentence))), 0)
        self.assertEqual(len(get_universal_quantifiers(self.nlp(acceptableSentence))), 0)

if __name__ == '__main__':
    unittest.main()
