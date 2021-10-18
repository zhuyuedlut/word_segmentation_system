import jieba
from preprocess.text_splitter import TextSplitter
from preprocess import text_normalize

def _test_jieba_dl_cut():
    content = "正在意大利度蜜月的“脸谱”创始人扎克伯格与他华裔妻子的一举一动都处于媒体的追踪之下"
    jieba.enable_paddle()
    words = jieba.cut(content, use_paddle=True)
    print(' '.join(words))

def read_raw_data(f_name='data/news_tensite_xml.smarty.dat'):
    with open(f_name, 'r', encoding='gb18030') as f:
        for line in f:
            line.strip()
            if not line:
                continue
            if '<content>' in line and '</content>' in line:
                content = line.replace('<content>', '').replace('</content>', '').strip()
                if not content:
                    continue
                yield content

def gen_train_data():
    text_splitter = TextSplitter()
    jieba.enable_paddle()
    out = open('data/train_data.txt', 'w', encoding='utf-8')

    for line in read_raw_data():
        for sent in text_splitter.split_sentence_for_seg(line):
            if sent in text_splitter.stops[2:-2]:
                continue
            sent = text_normalize.string_q2b(sent)

            labels = []
            word = jieba.cut(sent, use_paddle=True)
            for word in words:
                if len(word) == 1:
                    labels.append('S')
                else:
                    labels += ['B'] + ['M'] + (len(word) - 2) + ['E']

            out.write()

