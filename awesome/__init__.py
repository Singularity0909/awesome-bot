import ahocorasick


patterns = []
with open('awesome/data.txt', 'r', encoding='UTF-8') as f:
    while True:
        pattern = f.readline()
        if not pattern:
            break
        patterns.append(pattern.strip('\n'))

trie = ahocorasick.Automaton()
for index, word in enumerate(patterns):
    trie.add_word(word, (index, word))
trie.make_automaton()
