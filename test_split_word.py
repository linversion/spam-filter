import os
import re
import collections
from splitwords import SplitWords
import sys


class TestSplitWord:

    """docstring for ClassName"""
    def __init__(self):
        self.wordlist = {'normal': [], 'spam': []}
        self.mail_count = {'normal': 0, 'spam': 0}

    def test_split_word(self):

        fp = open(r'/home/linversion/Downloads/1', encoding='gbk').read()
        mail_content = fp[fp.index('\n\n')::]

        print("content class:", mail_content.__class__, mail_content)   # mail_content为str类型
#       try:
#            mail_content = mail_content.decode('gbk').encode('utf-8')
#       except:
#            print("error in encode file")
#       mail_content = re.findall(u'[\u4e00-\u9fff]+', mail_content)
#       mail_content = re.sub('\s+', '', mail_content)
        p = re.compile(u'[\u4e00-\u9fa5]')

        mail_content_list = re.findall(p, mail_content)
        print("type", mail_content_list.__class__)

        mail_content = "".join(mail_content_list)
#       res_list = SplitWords(mail_content).get_word_list()
        res_content = SplitWords(mail_content).seg_sentence()
        word_list = list(set(res_content))

        self.wordlist['normal'].extend(word_list)
        self.mail_count['normal'] += 1
        print(word_list)    #word_list是一个数组


def main():
    TestSplitWord().test_split_word()


if __name__ == '__main__':
    main()