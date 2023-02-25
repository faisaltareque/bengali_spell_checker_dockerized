import codecs
import gc

class SpellChecker:
    def __init__(self):
        words_list = []
        with codecs.open('vocab.txt', mode='r', encoding='utf-8') as f:
            for item in f:
                words_list.append(item.split(' ')[0])                
        words_dictionary = {}
        for i, word in enumerate(words_list):
            words_dictionary[word] = i
        del words_list
        gc.collect()
        self.letters = 'ঁংঃঅআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ়ঽািীুূৃৄেৈোৌ্ৎৗড়ঢ়য়'
        self.words_dictionary = words_dictionary

        
    def edits_distance_1(self, word:str):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in self.letters]
        inserts = [L + c + R for L, R in splits for c in self.letters]
        return set(deletes + transposes + replaces + inserts)


    def edits_distance_2(self, word:str):
        edits2_list = []
        for e1 in self.edits_distance_1(word):
            for e2 in self.edits_distance_1(e1):
                edits2_list.append(e2)
        return set(edits2_list)


    def known_word(self, words:list):
        known_list = []
        for item in words:
            if item in self.words_dictionary:
                known_list.append(item)
        return set(known_list)
    
        
    def top_K_candidates(self, word, K):
        candidates = self.candidates(word)
        candidates_list = []
        for item in candidates:
            candidates_list.append((self.words_dictionary[item], item))
        candidates_list.sort(reverse=False)
        if K > len(candidates_list):
            K = len(candidates_list)
        return [item[1] for item in candidates_list[:K]]   
     

    def candidates(self, word):
        return (self.known_word([word]) or self.known_word(self.edits_distance_1(word)) or self.known_word(self.edits_distance_2(word)) or [word])