import ahocorasick


class AC:
    patterns = []
    trie = None

    @classmethod
    def build(cls):
        with open('awesome/data/patterns.txt', 'r', encoding='utf-8') as f:
            while True:
                pattern = f.readline()
                if not pattern:
                    break
                cls.patterns.append(pattern.strip('\n'))

        cls.trie = ahocorasick.Automaton()
        for index, word in enumerate(cls.patterns):
            cls.trie.add_word(word, (index, word))
        cls.trie.make_automaton()
