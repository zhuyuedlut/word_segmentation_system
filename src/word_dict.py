import json
import math

class WordDict(object):
    def __init__(self, dict_path, separator='\t'):
        self.dict_path = dict_path

        self._dict = {}

        self._total_freq = 0
        self._total_word = 0
        self._total_freq_log = float('-Inf')

        self._separator = separator

    def _init_dict_from_txt(self):
        with open(self.dict_path, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                strs = line.strip().split(self._separator)
                word = strs[0]
                for i in range((len(strs) - 1) // 2):
                    pos, freq = strs[2 * i + 1], int(strs[2 * i + 2])
                    self.add_word(word, pos, freq)

        self._total_freq_log = math.log(self._total_freq or self._total_freq + 1)

    def add_word(self, word, pos, freq):
        if not self._dict.get(word, None):
            self._dict[word] = (freq, ((pos, freq),))
            self._total_word += 1
            self._total_freq += freq
        else:
            pos_freq_pairs = []
            word_freq = self._dict[word][0]
            # self._dict[word]中第一个元素是freq
            # 第二个元素是一个嵌套的tuple，分别保存的词的不同的词性和其对应的频率
            for pair in self._dict[word][1]:
                # 当前的添加的词性被添加过
                if pair[0] == pos:
                    self._total_freq -= pair[1]
                    word_freq -= pair[1]
                else:
                    pos_freq_pairs.append(pair)

            pos_freq_pairs.append((pos, freq))

            self._total_freq += freq
            word_freq += freq

            self._dict[word] = (word_freq, tuple(sorted(pos_freq_pairs, key=lambda x: x[1], reverse=True)))

        for i in range(len(word) - 1):
            pre_fix = word[:i + 1]
            if pre_fix not in self._dict:
                self._dict[pre_fix] = None

    def delete_word(self, word):
        if word in self._dict:
            self._dict.pop(word)


