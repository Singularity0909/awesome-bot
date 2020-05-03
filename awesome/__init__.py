import ahocorasick

patterns = ['傻逼', 'nmsl']
trie = ahocorasick.Automaton()
for index, word in enumerate(patterns):
    trie.add_word(word, (index, word))
trie.make_automaton()
