# coding: utf8
from __future__ import unicode_literals

from django.db import models

import os.path
import hashlib
import subprocess

from rdkit.Chem import rdChemReactions
from django.conf import settings
from base.modules import FileManagement

class Reaction(FileManagement, models.Model):

	class JSONAPIMeta:
		resource_name = "reactions"

	REACTANTS_MAX = 2

	METHODS_CHOICES = (
		('reactor', 'Reactor'),
		('rdkit', 'RDKit'),)

	name = models.CharField(
			max_length=128, 
			default='new_reaction', 
			unique=True)
	description = models.CharField(
					max_length=255, 
					default='',
					null= True,
					blank=True)
	user = models.ForeignKey(
					settings.AUTH_USER_MODEL, 
					on_delete=models.CASCADE, 
					db_index = True)
	file_hash = models.CharField(
			max_length=32, 
			default='')
	reactants_number = models.SmallIntegerField(
			default=0)
	method_priority = models.CharField(
			max_length=32,
			choices = METHODS_CHOICES, 
			default='reactor') # cls. methods_allowed
	smarts = models.CharField(
			max_length=1024, 
			default='') # smarts used by rdkit method

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if self.smarts == '': 
			self.smarts = self.get_smarts_from_mrv()
		if self.reactants_number == 0:
			self.reactants_number = self.get_reactants_number_from_mrv()
		super(Reaction, self).save(*args, **kwargs)
		return self
	
	def gen_image(self):
		svg = subprocess.check_output(["molconvert", "svg:w400h200", self.mrv_path()]).decode('utf-8')
		with open( self.image_path(), 'w') as fw:
			fw.write(svg)

	def get_image(self):
		if not os.path.isfile(self.image_path()):
			self.gen_image()
		return open( self.image_path(), 'r').read()

	@classmethod
	def import_file(cls, file_object, name, user, description=None):
		r = cls(name = name, user=user, description=description)
		r.save()
		with open(r.mrv_path(), 'w') as f:
			f.write(file_object.read().decode('utf-8'))
		r.save()
		r.gen_image()
		return r
	
	def has_no_project(self):
		from metabolization.models import ReactionsConf
		return ReactionsConf.objects.filter(reactions__in = [self]).count() == 0

	def mrv_path(self):
		return '/'.join([
			self.item_path(), 
			'reaction.mrv'])

	def image_path(self):
		return '/'.join([
			self.item_path(), 
			'image.svg'])

	def mrv_exist(self):
		return os.path.isfile(self.mrv_path()) 

	def method_to_apply(self):
		prio = self.method_priority
		default = 'reactor'
		available = self.methods_available()
		if prio in available:
			return prio
		elif default in available:
			return default

	def methods_available(self):
		res = []
		if self.mrv_exist():
			res.append('reactor')
		if self.rdkit_ready():
			res.append('rdkit')
		return res

	def rdkit_ready(self):
		try:
			rx = self.react_rdkit()
			return rx.Validate() == (0,0)
		except:
			return False

	def get_smarts_from_mrv(self):
		if self.mrv_exist():
			return subprocess.check_output(['molconvert', 'smarts', self.mrv_path()]).decode('utf-8')
		else:
			return ''

	def react_rdkit(self):
		return self.react_rdkit_(self.smarts)

	def react_rdkit_(self, smarts):
		if smarts != '':
			return rdChemReactions.ReactionFromSmarts(smarts)

	def get_reactants_number_from_mrv(self):
		smarts = self.get_smarts_from_mrv()
		if smarts:
			rx = self.react_rdkit_(smarts)
			return rx.GetNumReactantTemplates()
		else:
			return 0

## Hash management ##
# file_hash aims to check if reaction file has not be changed since last DB update
	def file_hash_compute(self):
		if self.mrv_exist():
			with open(self.mrv_path(), 'rb') as f:
				return hashlib.md5(f.read()).hexdigest()
		else:
			return ''

	def file_hash_update(self):
		self.file_hash = self.file_hash_compute()
		return self

	def file_hash_check(self):
		return self.file_hash == self.file_hash_compute()

	def __unicode__(self):
		return self.name

####
