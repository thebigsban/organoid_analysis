import numpy as np
import pandas as pd
import anndata
import pickle
import read

class ADIntermediate:
	"""
	Basically a class intermediate that helps me save and load intermediate results from scanpy processing. For some reason the default scanpy shit doesn't let me save so this is wat I gotta do.
	"""
	def __init__(self, ad):
		self.X = ad.X
		self.var = ad.var
		self.obs = ad.obs



def save_adi(ADI, path):
	with open(path, 'wb') as f:
		pickle.dump(ADI, f)


def load_adi(path):
	with open(path,'rb') as f:
		a =  pickle.load(f)
	return a

def adi2ad(adi):
	return anndata.AnnData(X = adi.X, var = adi.var, obs = adi.obs)




