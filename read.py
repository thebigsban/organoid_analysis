import gzip
import numpy as np
from multiprocessing import Process, Manager
import time
import itertools
import multiprocessing
import anndata
import pandas as pd


def do_work(in_queue, out_list, dtype = np.float16):
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
        line_list = line.split(b"\t")
        out_list.append([line_no, line_list[0], np.array(line_list[1:]).astype(dtype)])
        #gene_list.append([line_no, line_list[0]])
        if line_no % 1000 == 0:
            print(line_no)


def read_dataset(file, dtype = np.float16):
    """
    A function leveraging multiprocessing to read in scRNAseq datasets line-by-line in order to populate a numpy array.

    Arguments:
        file : str
            absolute or relative path to file, either formatted as .txt or .gz
        dtype : data type (optional)
            data type of numpy array to store expression data. default is 16-bit floating point

    Returns:
        expr_mat : numpy.array
            numpy array of given data type containing the expression matrix. note that the array will be formatted such that rows are cells, and columns are genes (though the file format may be the other way around)
        gene_list : list
            list of genes sequenced 
    """
    num_workers = multiprocessing.cpu_count()//2

    manager = Manager()
    results = manager.list()
    #gene_list = manager.list()
    work = manager.Queue(num_workers)

    pool = []

    for i in range(num_workers):
        p = Process(target = do_work, args = (work, results, dtype))
        p.start()
        pool.append(p)

    if file[-2:] == 'gz':
        with gzip.open(file) as f:
            iters = itertools.chain(f, (None,)*num_workers)
            #counter = 0
            for num_and_line in enumerate(iters):
                work.put(num_and_line)
                #counter += 1
                #if counter == 1000:
                #    break
    elif file[-3:] == 'txt':
        with open(file) as f:
            iters = itertools.chain(f, (None,)*num_workers)
            #counter = 0
            for num_and_line in enumerate(iters):
                work.put(num_and_line)
                #counter += 1
                #if counter == 1000:
                #    break
    else:
        print('please call function with path to either a .txt or .gz file')
        return 0
    for p in pool:
        p.join()


    expr_mat = np.zeros((len(results), len(results[20][2])), dtype = np.float16)
    #print(expr_mat.shape)
    gene_list = []
    for i in range(len(results)):
        if results[i][0] == 0:
            pass
        else:
            expr_mat[results[i][0]-1] = results[i][2]
            gene_list.append([results[i][0], results[i][1]])

    # sort gene list by row index
    gene_list.sort(key = lambda x : x[0])

    # remove index - return gene list only
    for i in range(len(gene_list)):
        # note genes are stored as bytes in form b"GENE_NAME|GENE_NAME", so we keep only GENE_NAME
        gene_list[i] = gene_list[i][1].decode('utf-8').split('|')[0]

    # transpose matrix if genes correspond to rows instead of columns TODO MAKE THIS WORK
    #if expr_mat.shape[0] == len(gene_list)-1:
    #    expr_mat = expr_mat.T

    return expr_mat.T, gene_list



def read_organoid_ucsc():
    """
    A function leveraging multiprocessing to read in scRNAseq datasets line-by-line in order to populate a numpy array. 
    """
    expr_mat, gene_list = read_dataset('/home/sban/Documents/organoid_analysis/Organoid_UCSC/exprMatrix.tsv.gz')
    return expr_mat, gene_list
def read_primary_ucsc():
    expr_mat, gene_list = read_dataset('/home/sban/Documents/organoid_analysis/PrimaryCell_UCSC/exprMatrix.tsv.gz')
    return expr_mat, gene_list


def read_organoid_ucsc_scanpy(*args, **kwargs):
    expr_mat, gene_list = read_organoid_ucsc()
    meta = pd.read_csv('/home/sban/Documents/organoid_analysis/Organoid_UCSC/meta.tsv', sep='\t')
    gene_dict = {}
    gene_dict['gene_name'] = gene_list
    ad = anndata.AnnData(X = expr_mat, var = gene_dict, obs = meta, dtype = 'float16', **kwargs)
    ad.var_names=ad.var['gene_name']
    return ad

def read_primary_ucsc_scanpy(*args, **kwargs):
    expr_mat, gene_list = read_organoid_ucsc()
    meta = pd.read_csv('/home/sban/Documents/organoid_analysis/PrimaryCell_UCSC/meta.tsv', sep='\t')
    gene_dict = {}
    gene_dict['gene_name'] = gene_list
    ad = anndata.AnnData(X = expr_mat, var = gene_dict, obs = meta, dtype = 'float16', **kwargs)
    ad.var_names=ad.var['gene_name']
    return ad







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