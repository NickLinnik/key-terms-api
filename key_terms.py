from string import punctuation
from lxml import etree

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import pos_tag

from sklearn.feature_extraction.text import TfidfVectorizer


class KeyTerms:
    vectorizer = TfidfVectorizer(input='content', use_idf=True, lowercase=True,
                                 analyzer='word', ngram_range=(1, 1))

    def __init__(self, hash_map: dict, key_terms_num: int = 5):
        if key_terms_num is None:
            key_terms_num = 5

        self.corpora = hash_map
        self.tokens = self._tokenize()
        self.lemmatized = self._lemmatize()
        self.cleaned = self._clean()
        self.keywords = self._tfidf_sort(key_terms_num)

    @staticmethod
    def from_xml(filepath, key_terms_num: int = None):
        corpus = etree.parse(filepath).getroot()[0]
        return KeyTerms({elem[0].text: elem[1].text for elem in corpus}, key_terms_num)

    def _tokenize(self):
        return {head: word_tokenize(text.lower()) for head, text in self.corpora.items()}

    def _lemmatize(self):
        lemmatizer = WordNetLemmatizer()
        return {head: list(map(lambda token: lemmatizer.lemmatize(token), text))
                for head, text in self.tokens.items()}

    def _clean(self):
        useless_tokens = set(list(punctuation) + stopwords.words('english'))
        return {head: list(filter(lambda token:
                                  token not in useless_tokens and pos_tag([token])[0][1] == 'NN',
                                  text))
                for head, text in self.lemmatized.items()}

    def _tfidf_sort(self, quantity: int):
        corpora_texts = list(map(lambda token_list: ' '.join(token_list), self.cleaned.values()))
        tfidf_matrix = KeyTerms.vectorizer.fit_transform(corpora_texts).toarray()
        tfidf_scores = []
        terms = KeyTerms.vectorizer.get_feature_names_out()
        for i, vector in enumerate(tfidf_matrix):
            tfidf_scores.append(list(map(lambda index:
                                         (terms[index], tfidf_matrix[i, index]), range(vector.size))))
            tfidf_scores[i].sort(key=lambda token: (token[1], token[0]), reverse=True)
        return {head: [term[0] for term in text[:quantity]] for head, text in
                zip(self.cleaned.keys(), tfidf_scores)}

    def prettify(self):
        return '\n'.join([f"{key}:\n{' '.join(value)}\n" for key, value in self.keywords.items()])


if __name__ == '__main__':
    print(KeyTerms.from_xml('test_news.xml').prettify())
