# -*- coding: utf-8 -*-
from ..models import *
import unittest


class Teacher_test(unittest.TestCase):
	def setUp(self):
		self.teachaer_item = {
			"name" : "张三",
			"card_id" : 2
		}
	
	def tearDown(self):
		Teacher.objects.get(card_id=2).delete()
		
	def test_model(self):
		Teacher.objects.create(**self.teachaer_item)
		self.assertEqual(Teacher.objects.filter(card_id=2).exists(),  True)