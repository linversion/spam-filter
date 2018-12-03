#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import collections
from splitwords import SplitWords
import sys


class TrainModule:
	"""
		use given mails to train the module
	"""

	def __init__(self):

		self.wordlist = {'normal': [], 'spam': []}    # 创建两个字典

		self.mail_count = {'normal': 0, 'spam': 0}    # 统计邮件数量的字典

		self.dic_word_freq = {}    # { 'word' : [0.1, 0.002], 'text' : [0.2, 0.001], ... }统计词频的字典

		self.PRE_DEFINED_WORD_FREQ = 0.01    # 预定义的词频为0.01

		self.WORD_FREQ_FILE = '/home/linversion/Downloads/module/freq_file.txt'    # 将词频数据写入freq_file文件

	def build_word_list(self, mail_dir):    # 遍历normal和spam邮件目录，分词更新字典
		p = re.compile(u'[\u4e00-\u9fa5]')
		for dirt in os.listdir(mail_dir):    # data文件夹下的两个目录'normal', 'spam'，os.listdir(path)返回指定路径下的文件和文件夹列表

			d = mail_dir + '/' + dirt + '/'
			print('scanning directory: ', d)

			for filename in os.listdir(d):
				print('handling file:', filename)
				fp = open(d + filename, encoding='gbk').read()    # read() 方法用于从文件读取指定的字节数，如果未给定或为负则读取所有
				mail_content = fp[fp.index('\n\n')::]
				'''
				try:
					mail_content = mail_content.decode('gbk').encode('utf-8')
				except:

					print >> sys.stderr, 'ERROR: ', filename
					continue
				'''
# 				mail_content = re.sub('\s+', ' ', mail_content)    # re.sub用于替换字符串中的匹配项，将字符串中的一个或多个空格换成一个空格
				mail_content = "".join(re.findall(p, mail_content))

				res_list = SplitWords(mail_content).seg_sentence()    # 邮件内容分词得到一个list

				word_list = list(set(res_list))		# 先转为set去除重复，再转回list

				self.wordlist[dirt].extend(word_list)    # 将结果存进wordlist中
				self.mail_count[dirt] += 1    # 记录邮件数加一

	def calc_word_freq(self, mail_type):    # 计算词频，mail_type为normal和spam
		counter = collections.Counter(self.wordlist[mail_type])    # 从字典创建Counter，Counter是一个简单的计数器，例如，统计字符出现的个数
		dic = collections.defaultdict(list)    # collections.defaultdict(list)使用起来效果和运用dict.setdefault()比较相似
		for word in list(counter):
			dic[word].append(counter[word])

		for key in dic:		# 将字典转换成{'1': [0.2], '3': [0.1], '2': [0.1]})的形式，'word':[概率]
			dic[key][0] *= 1.0 / self.mail_count[mail_type]
			dic[key][0] = round(dic[key][0], 3)
		return dic

	def build_freq_dict(self):
		print('building word frequency dict...')
		self.build_word_list('/home/linversion/Downloads/data')    # 指定邮件目录/tmp/data来构建词频字典

		dic_word_freq_in_normal = self.calc_word_freq('normal')    # 统计正常邮件的词频
		dic_word_freq_in_spam = self.calc_word_freq('spam')    # 统计垃圾邮件的词频

		dic_word_freq = dic_word_freq_in_normal    # dic_word_freq_in_normal存入dic_dic_word_freq

		for key in dic_word_freq_in_spam:    # 遍历垃圾邮件字典
			if key not in dic_word_freq:  # 该词只在垃圾邮件中出现
				dic_word_freq[key].append(self.PRE_DEFINED_WORD_FREQ)
			dic_word_freq[key].append(dic_word_freq_in_spam[key][0])

		for key in dic_word_freq:
			if len(dic_word_freq[key]) == 1:
				dic_word_freq[key].append(self.PRE_DEFINED_WORD_FREQ)
		'''
		构造字典dic_word_freq的形式为{'word':[在正常邮件中出现的概率，在垃圾邮件中出现的概率]}
		如果在任一中未出现则用PRE_DEFINED_WORD_FREQ代替
		'''
		self.dic_word_freq = dic_word_freq

	def write_freq_file(self):  # 将构造好的字典写入文件保存
		print('writing freq file...')

		dic_freq = self.dic_word_freq
		fp = open(self.WORD_FREQ_FILE, 'w')
		
		fp.write(str(self.mail_count['normal']) + ' ')
		fp.write(str(self.mail_count['spam']) + '\n')

		for key in dic_freq:
			fp.write(key)
			for v in dic_freq[key]:
				fp.write(' ' + str(v))
			fp.write('\n')

		fp.close()

	def read_freq_file(self):  # 读取字典
		if not os.path.isfile(self.WORD_FREQ_FILE):
			return False

		print('reading freq file...')

		fp = open(self.WORD_FREQ_FILE, 'r')
		word_freq_list = {}

		for line in fp.readlines():
			linelist = line.strip('\n').split(' ')

			if len(linelist) == 2:
				self.mail_count['normal'] = int(linelist[0])
				self.mail_count['spam'] = int(linelist[1])
			else:
				word_freq = {linelist[0]: [float(linelist[1]), float(linelist[2])]}
				word_freq_list.update(word_freq)

		self.dic_word_freq = word_freq_list
		fp.close()
		return True

	def set_dic_word_freq(self):
		if not self.read_freq_file():
			self.build_freq_dict()
			self.write_freq_file()

	def update(self, mail_type, word_list):		# 加入数据后更新模型
		if mail_type == 'normal':
			mt = 0
		else:
			mt = 1

		for word in word_list:
			if word not in self.dic_word_freq:
				self.dic_word_freq[word] = [self.PRE_DEFINED_WORD_FREQ, self.PRE_DEFINED_WORD_FREQ]
				self.dic_word_freq[word][mt] = 1.0 / (self.mail_count[mail_type] + 1)
			else:
				if self.dic_word_freq[word][mt] == self.PRE_DEFINED_WORD_FREQ:
					self.dic_word_freq[word][mt] = 1.0 / (self.mail_count[mail_type] + 1)
				else:
					self.dic_word_freq[word][mt] = \
				(1 + self.dic_word_freq[word][mt] * self.mail_count[mail_type]) / (self.mail_count[mail_type] + 1)

		self.mail_count[mail_type] += 1


def main():
	TrainModule().set_dic_word_freq()


if __name__ == '__main__':
	main()

