#!/usr/bin/python2
# -*- coding: utf-8 -*-

import jieba
import re
filepath = '/home/linversion/Downloads/stopwords.dat.txt'
stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]


class SplitWords:

	def __init__(self, content):
		self.content = content

	def seg_sentence(self):

		res_list = jieba.cut(self.content.strip())  # strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
		print(res_list)
		word_list = []
		for word in res_list:
			if word not in stopwords:
				if word != '\t':
					word_list.append(word)
		return word_list

	def get_word_list(self):
		res_list = list(jieba.cut(self.content.strip()))  # 将分词结果转换为list
		word_list = []
		for i in res_list:
			word_list.append(i)
		return word_list


def main():
	content = '''
	死亡天使（Azrael）是美国DC漫画旗下反英雄，初次登场于《蝙蝠侠：死亡天使的剑》（Batman: Sword of Azrael）第1期（1992年10月）。
	本名尚-保罗·范雷（Jean-Paul Valley），是前哥谭市义警，作为一名有心理问题的英雄经常出现在各种事件当中。
	'''
	word_list = SplitWords(content).seg_sentence()    # 类型为list
	print('1', word_list)
	content2 = re.sub(u'[^\u4e00-\u9fa5]', '', content)
	print(content2)
	word_list2 = SplitWords(content2).seg_sentence()
	print('2', word_list2)


if __name__ == '__main__':
	main()

