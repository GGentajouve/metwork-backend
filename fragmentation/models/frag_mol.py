# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models, IntegrityError
from polymorphic.models import PolymorphicModel
from base.models import Molecule
from fragmentation.models import FragSimConf, FragSample
from base.modules.rdkit_functions import RDKit
import hashlib
from decimal import *
import time

class FragMol(PolymorphicModel):

	class JSONAPIMeta:
		resource_name = "fragmol"

	mass = \
		models.DecimalField(\
				max_digits=16, \
				decimal_places=10, 
				default = 0,
				db_index = True)

	MASS_DECIMALS = 10

	def gen_mgf(self, energy = 2, decimal = 6):
		getcontext().prec = decimal + 10
		DECIMALS = Decimal(10) ** (-1 * (decimal))
		res = 'BEGIN IONS\n' + \
				'PEPMASS={0}\n'.format( str(Decimal(self.mass).quantize(DECIMALS)) )
		res += '\n'.join([ '{0}={1}'.format(*at) for at in self.get_attributes()]) + '\n'
		res += 'SCANS={0}\n'.format(self.scan_id())
		res += '\n'.join([ \
			' '.join([ str( Decimal(v).quantize(DECIMALS) ) for v in (fp.mz, fp.intensity) ]) \
			for fp in self.fragmolpeak_set.all().filter(energy = energy).order_by('mz') ]) + '\n'
		res += 'END IONS\n'
		return res

class FragMolSim(FragMol):

	param_hash = models.CharField(\
					max_length=32, \
					default='')
	conf_hash = models.CharField(\
					max_length=32, \
					default='')
	frag_sim_conf = models.ForeignKey(
					'FragSimConf', 
					on_delete=models.CASCADE, 
					null = True,
					default=None)
	molecule = models.ForeignKey(
					Molecule, 
					on_delete=models.PROTECT, 
					null = True,
					default=None)
	status_code = models.SmallIntegerField(
					default = 0)

	class status:
		INIT = 0
		READY = 1
		RUNNING = 2
		DONE = 3
		ERROR = 99

	def __str__(self):
		return self.molecule.smiles()

	def wait_run_end(self, timeout = 3000):
		begin = time.time()
		while self.status_code != FragMolSim.status.DONE:
			time.sleep(0.5)
			if (time.time() - begin) > timeout:
				print ('\n#### fragmentation wait_run_end close due to timeout #####\n')
				return self
			else:
				self.refresh_from_db()
		return self

	def scan_id(self):
		return self.molecule.id

	def get_attributes(self):
		m = self.molecule
		return [
			( 'CHARGE', '1+' ), 
			( 'FILENAME', 'METWORK_' + str(m.id) ), 
			( 'SMILES', m.smiles() ), 
			( 'INCHI', RDKit.mol_to_inchi(m.mol_rdkit) ), 
			( 'INCHIAUX', m.inchi_key ), 
		]

	def update_hashes(self):
		for fn in FragSimConf.PARAM_FILES:
			with open(self.frag_sim_conf.file_path(fn), 'rb') as f:
				self.__setattr__(fn + '_hash', hashlib.md5(f.read()).hexdigest())
		self.save()
		return self

class FragMolSample(FragMol):

	frag_sample = models.ForeignKey(
					FragSample, 
					on_delete=models.CASCADE, 
					null = True,
					default=None)
	ion_id = models.IntegerField(
					default=0)

	def scan_id(self):
		return self.ion_id

	def get_attributes(self):
		return[ ( at.title, at.value ) for at in self.fragmolattribute_set.order_by('position') ]
