#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
from emailparser import EmailParser
from splitwords import SplitWords
from trainmodule import TrainModule

class JudgeMail:
	'''
	calculate the possibility of being a spam
	'''

	def __init__(self, mail_file, is_given_mail=False):
		self.mail_file = mail_file	#邮件文件路径
		self.is_given_mail = is_given_mail

		self.train_module = TrainModule()

		self.P_SPAM = 0.5	# 先验概率为0.5
		self.P_NORMAL = 1 - self.P_SPAM

		self.P_SPAM_WORD = 0.4  # 词语未出现在模型中，p(s|w)设为0.4

		self.P_IS_SPAM_LIMIT = 0.9	# 判断阀值

		self.train_module.set_dic_word_freq()	# 开始训练模型

	def judge(self):
		mail_content = EmailParser(self.mail_file, self.is_given_mail).get_mail_content()	#获取邮件内容，得到str类型

		res_list = SplitWords(mail_content).get_word_list()	# 将邮件分词得到一个list
		word_list = list(set(res_list))	# 去除重复的词
		for i in \
[';', ':', ',', '.', '?', '!', '(', ')', ' ', '/', '@',\
'+', '-', '=', '*', '“', '”', \
 '；', '：', '，', '。', '？', '！', '（', '）', '　', '、']:
			if i in word_list:	#去除标点符号
				word_list.remove(i)

		word_freq = []
		for word in word_list:	#遍历每个词，计算三个概率
			if word in self.train_module.dic_word_freq:	# 该词出现在模型中
				p_w_n = self.train_module.dic_word_freq[word][0]  # 读取在正常邮件中的概率
				p_w_s = self.train_module.dic_word_freq[word][1]  # 读取在垃圾邮件中的概率
				p_s_w = p_w_s * self.P_SPAM / (p_w_s * self.P_SPAM + p_w_n * self.P_NORMAL)  # 该词的p(s|w)

				word_freq.append((word, p_s_w))
			else:
				word_freq.append((word, self.P_SPAM_WORD))

		word_freq_most = sorted(word_freq, key = lambda x:x[1], reverse=True)[:15]  # 取15个特征向量，取p(s|w)最大的15个

		p = 1.0
		rest_p = 1.0
		k = 1.0
		for i in word_freq_most:
			print(i[0], i[1])
			k *= 1.0 / i[1] - 1

		p_spam = 1 / (1 + k)
		mail_type = ''
		
		if p_spam > self.P_IS_SPAM_LIMIT:  # 后验概率大于0.9则为垃圾邮件
			mail_type = 'spam'
		else:
			mail_type = 'normal'

		self.train_module.update(mail_type, word_list)  # 判断完后更新模型
		return p_spam

def main():
	fp = open(sys.argv[1], 'r')	# 邮件路径需要输入
	p = JudgeMail(fp, True).judge()
	fp.close()

	print('SPAM: p = ', p)	# 输出该邮件为垃圾邮件的概率

if __name__ == '__main__':
	main()

