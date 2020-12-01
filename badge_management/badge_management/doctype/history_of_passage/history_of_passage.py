# -*- coding: utf-8 -*-
# Copyright (c) 2020, Guerbadot Alexandre and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import date, timedelta
from frappe.model.document import Document

class HistoryOfPassage(Document):
	

	def get_default_unit(self):
		return frappe.db.get_single_value('Badge Management Settings', 'default_unit')

	def get_default_item(self):
		return frappe.db.get_single_value('Badge Management Settings', 'default_item')

	def get_unpaired_document(self):
		"""
			Look for the unpaired document of the day
		"""
		return frappe.db.get_list('History Of Passage',
			filters={
				'customer' : self.customer,
				'is_paired' : 0,
				'date' : ['>', date.today()]
			},
			fields= ['name', 'date']
		)

	def insert_document(self, doc):
		"""
			Insert a document in the doctype History Of Presence

			doc : The document to be inserted
		"""

		doc = frappe.get_doc({
			'doctype' : 'History Of Presence',
			'user' : self.user,
			'customer' : self.customer,
			'start_date' : doc.date,
			'start_date_document' : doc.name,
			'end_date' : self.date,
			'end_date_document' : self.name,
			'item' : self.get_default_item(),
			'unit' : self.get_default_unit()
		})
		doc.insert(ignore_permissions=True)

	
	def after_insert(self):

		# Get the unpaired passage for a the user
		unpaired = self.get_unpaired_document()

		# If there is 2 unpaired document, they're paired and then create a History Of Presence
		if len(unpaired) == 2:
			if self.name == unpaired[0].name:
				self.insert_document(doc=unpaired[1])
			else:
				self.insert_document(doc=unpaired[0])
			
			# Set the value of is_paired to 1 for each History Of Passage
			frappe.db.set_value('History Of Passage', unpaired[0].name,'is_paired', 1)
			frappe.db.set_value('History Of Passage', unpaired[1].name,'is_paired', 1)

