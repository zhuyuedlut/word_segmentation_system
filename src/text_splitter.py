import math
import re


class TextSplitter(object):
    def __init__(self, stops='([，。？?！!；;：:\n ])'):
        self.stops = stops
        self.re_split_sentence = re.compile(self.stops)

    def split_sentence_for_seq(self, context, max_len=512):
        sentence = []

        for sent in self.re_split_sentence(context):
            if not sent:
                continue
            for i in range(math.ceil(len(sent) / max_len)):
                sent_segment = sent[i * max_len:(i + 1) * max_len]
                sentence.append(sent_segment)

        return sentence


if __name__ == '__main__':
    text_splitter = TextSplitter()
    content = '我是谁。我在哪里。你又是谁？119.2 。29,220.20元！你说：”我很好！是吗?”'
    print('split sentence for seg\n')
    for i, sent in enumerate(text_splitter.split_sentence_for_seg(content)):
        print('sent:{} {}'.format(i, sent))
    print('\n')