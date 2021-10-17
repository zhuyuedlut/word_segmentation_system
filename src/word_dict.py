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
                # 当前的添加的词性被添加过，直接覆盖之前的词频
                if pair[0] == pos:
                    self._total_freq -= pair[1]
                    word_freq -= pair[1]
                else:
                    pos_freq_pairs.append(pair)

            pos_freq_pairs.append((pos, freq))

            self._total_freq += freq
            word_freq += freq

            self._dict[word] = (word_freq, tuple(sorted(pos_freq_pairs, key=lambda x: x[1], reverse=True)))

        # 将当前词的前缀词都添加到_dict，设置value为None
        # 便于词图构建时的判断
        # 比如 "台湾同乡会"，前缀为"台" "台湾" "台湾同" "台湾同乡"
        for i in range(len(word) - 1):
            pre_fix = word[:i + 1]
            if pre_fix not in self._dict:
                self._dict[pre_fix] = None

    def delete_word(self, word):
        if word in self._dict:
            self._dict.pop(word)

    def freq(self, word):
        return self._dict[word][0] if word in self._dict and self._dict[word] else None

    def pos(self, word):
        return self._dict[word][1] if word in self._dict and self._dict[word] else None

    def first_pos_tag(self, word):
        return self._dict[word][1][0][0] if word in self._dict and self._dict[word] else 'x'

    def is_in(self, word):
        return word in self._dict

    def get_total_freq_log(self):
        return self._total_freq_log

    def __str__(self):
        return json.dumps(
            {
                'dict': self._dict,
                'total_freq': self._total_freq,
                'total_word': self._total_word,
                'total_freq_log': self._total_freq_log
            },
            ensure_ascii=False)


if __name__ == '__main__':
    word_dict = WordDict('core_dict.txt')
    print(word_dict.freq('今天'))
    print(word_dict.is_in('老狼'))
    print(word_dict.pos('今天'))



