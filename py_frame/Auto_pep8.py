# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/9/26 9:52
# file_name     Auto_pep8.py


import os


"""
PEP8格式化：

	1、pip install autopep8
		命令行使用方式 ： $ autopep8 --in-place --aggressive --aggressive <filename>

	2、选择菜单「File」–>「Settings」–>「Tools」–>「External Tools」–>点击加号添加工具

	3、填写如下配置项，点击「OK」保存
		Name：Autopep8 (可随意填写)

		Tools settings:

			Programs：autopep8

			Parameters：--in-place --aggressive --ignore=E123,E133,E50 $FilePath$

			Working directory：$ProjectFileDir$

	4、对想pep8格式化的代码直接点击右键，选择「Extern Tools」–>「Autopep8」即可

"""
