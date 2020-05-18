import gzip
import numpy as np
from multiprocessing import Process, Manager
import time
import itertools
import multiprocessing


def do_work(in_queue, out_list):
    while True:
        item = in_queue.get()
        line_no, line = item
        #print(type(line))
        # exit signal 
        if line == None:
            return
        
        # fake work
        #time.sleep(.5)
        #result = (line_no, line)
        #print(result[0])
        #out_list.append(result)
        out_list.append([line_no, np.array(line.split(b"\t")[1:]).astype(np.float16)])
        if line_no % 1000 == 0:
            print(line_no)



def read_organoid_ucsc():
    num_workers = multiprocessing.cpu_count()//2

    manager = Manager()
    results = manager.list()
    work = manager.Queue(num_workers)

    pool = []

    for i in range(num_workers):
        p = Process(target = do_work, args = (work, results))
        p.start()
        pool.append(p)

    with gzip.open('Organoid_UCSC/exprMatrix.tsv.gz') as f:
        iters = itertools.chain(f, (None,)*num_workers)
        #counter = 0
        for num_and_line in enumerate(iters):
            work.put(num_and_line)
            #counter += 1
            #if counter == 1000:
            #    break
    for p in pool:
        p.join()

    expr_mat = np.zeros((16774, 235121), dtype = np.float16)
    for i in range(len(results)):
        if i == 0:
            pass
        else:
            expr_mat[results[i][0]-1] = results[i][1]

    return expr_mat

'''
with gzip.open('Organoid_UCSC/exprMatrix.tsv.gz') as f:
    counter = 0
    for line in f:
        #print(line[0:100])
        #print(line[0:100].split("\t"))
        #a = line#[0:100]
        if counter == 0:
            counter += 1
        elif counter == 16773:
            break
        else:
            a = np.array(line.split(b"\t")[1:]).astype(np.float16)
            expr_mat[counter-1] = a
            counter += 1
            if counter % 100 == 0:
                print(counter)
'''

# transpose it so observations (cells) correspond to rows, and features (genes) correspond to columsn
#expr_mat = expr_mat.T


# normalize along genes
#from sklearn.preprocessing import StandardScaler
#expr_mat = StandardScaler().fit_transform(expr_mat)



'''
# COVARIANCE MATRIX CALCULATION - TAKES 88HRS TO COMPUTE
cov_mat = np.zeros((expr_mat.shape[0], expr_mat.shape[0]))


for i in range(len(cov_mat)):
    for j in range(i, len(cov_mat)):
        cov_mat[i,j] = np.dot(expr_mat[i], expr_mat[j])
    print(i)
'''

#PCA - Memory requirements are ass

# incremental PCA
'''
from sklearn.decomposition import IncrementalPCA
from scipy import sparse

transformer = IncrementalPCA(n_components=10, batch_size=200)
X_sparse = sparse.csr_matrix(expr_mat)
X_transformed = transformer.fit_transform(expr_mat)
'''