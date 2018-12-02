#!/usr/bin/python2
# -*- coding: utf-8 -*-

import jieba

filepath = '/home/linversion/Downloads/stopwords.dat.txt'
stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]


class SplitWords:

	def __init__(self, content):
		self.content = content

	def seg_sentence(self):

		sentence_seged = jieba.cut(self.content.strip())
		outstr = ''
		for word in sentence_seged:
			if word not in stopwords:
				if word != '\t':
					outstr += word
					outstr += " "
		return outstr

	def get_word_list(self):
		res_list = list(jieba.cut(self.content))  # 将分词结果转换为list
		word_list = []
		for i in res_list:
			word_list.append(i)
		return word_list


def main():
	content = '''
	毕业论文攻坚阶段，请保持手机畅通，经常查看邮件，随时和导师进行联系和沟通。随意，淡漠，不积极主动必定给自己的顺利毕业蒙上一层阴霾。
	'''
	word_list = SplitWords(content).get_word_list()    # 类型为list
	print(word_list)
	print("stopwords class：", stopwords.__class__)
	word_list2 = SplitWords(content).seg_sentence()
	print("class:", word_list2.__class__, word_list2)


if __name__ == '__main__':
	main()

