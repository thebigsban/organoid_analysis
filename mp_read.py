import multiprocessing as mp

def process_wrapper(linebyte):
	with open('Organoid_UCSC_primarymatrix_nonorm.txt','r') as f:
		f.seek(linebyte)
		line = f.readline()
		print(line[0:100])


pool = mp.Pool()
jobs = []

with open('Organoid_UCSC/primarymatrix_nonorm.txt','r') as f:
	nextLineByte = f.tell()
	for line in f:
		jobs.append(pool.apply_async(process_wrapper, (nextLineByte)))
		nextLineByte = f.tell()

for job in jobs:
	job.get()

pool.close()
