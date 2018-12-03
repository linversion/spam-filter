#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
from splitwords import SplitWords
from trainmodule import TrainModule
import re


class JudgeMail:

	# calculate the possibility of being a spam

	def __init__(self, mail_file, is_given_mail=False):

		self.mail_content = mail_file  # 邮件文件路径

		self.is_given_mail = is_given_mail

		self.train_module = TrainModule()

		self.P_SPAM = 0.5  # 先验概率为0.5

		self.P_NORMAL = 1 - self.P_SPAM

		self.P_SPAM_WORD = 0.4		# 词语未出现在模型中，p(s|w)设为0.4

		self.P_IS_SPAM_LIMIT = 0.9		# 判断阀值

		self.train_module.set_dic_word_freq()  # 开始训练模型

	def judge(self):

		res_list = SplitWords(self.mail_content).seg_sentence()		# 将邮件分词得到一个list

		word_list = list(set(res_list))		# 去除重复的词

		word_freq = []

		for word in word_list:		# 遍历每个词，计算三个概率
			if word in self.train_module.dic_word_freq:		# 该词出现在模型中
				p_w_n = self.train_module.dic_word_freq[word][0]  # 读取在正常邮件中的概率
				p_w_s = self.train_module.dic_word_freq[word][1]  # 读取在垃圾邮件中的概率
				p_s_w = p_w_s * self.P_SPAM / (p_w_s * self.P_SPAM + p_w_n * self.P_NORMAL)

				word_freq.append((word, p_s_w))
			else:
				word_freq.append((word, self.P_SPAM_WORD))

		word_freq_most = sorted(word_freq, key=lambda x: x[1], reverse=True)[:15]  # 取15个特征向量，取p(s|w)最大的15个

		k = 1.0
		for i in word_freq_most:
			print(i[0], i[1])
			k *= 1.0 / i[1] - 1

		p_spam = 1 / (1 + k)

		if p_spam > self.P_IS_SPAM_LIMIT:   # 后验概率大于0.9则为垃圾邮件
			mail_type = 'spam'
		else:
			mail_type = 'normal'

		# self.train_module.update(mail_type, word_list)  # 判断完后更新模型
		return p_spam


def main():
	fp = open('/home/linversion/Downloads/1', encoding='gbk').read()  # 邮件路径需要输入
	mail_content = fp[fp.index('\n\n')::]  # 读取正文
	p = re.compile(u'[\u4e00-\u9fa5]')
	mail_content = "".join(re.findall(p, mail_content))
	p = JudgeMail(mail_content, True).judge()  # 输出该邮件为垃圾邮件的概率
	print('SPAM: p = ', p)


if __name__ == '__main__':
	main()

