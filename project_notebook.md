#### 2020-05-15 (written 05-18)

* Downloaded datasets
  
  * some of the other datasets from other papers are kinda hard to get to; some are even unavailable

* Tried to leverage pre-built tools to read in data, but all of them for some reason have to load everything into memory first and then do some conversion, which crashes my PC usually. Weird tho cuz if we using float32 datatype, whole dataset should only occupy approx 14-15gb of memory, and around 7-8 gb for float16

* parsed .txt/.tsv/.tsv.gz files directly, and used regex to split lines to populate numpy array
  
  * this takes like 20 min to populate the entire array

TODO: 

* write better data reader, probably using multiprocessing to read in data. 

#### 2020-05-18

* wrote a reader for the UCSC Organoid dataset that leverages multiprocessing. basically, uses mp to read lines into memory and then once there, can parse list to populate numpy array
  
  * NOTE: couldn't find way to have each process populate the numpy array directly, this seems like the next best option

* tried to perform PCA and IncrementalPCA - usually causes crashes in memory 

* IDEA: subset/sample data, perform PCA on subset, apply projection to full-dataset for tSNE/visualization/clustering
  
  * subset UCSC Organoid dataset to 20,000 cells; PCA with 10 or 100 resulting components takes a reasonable amount of time; performing the full SVD takes a while (let it run for like 1hr, and didn't finish)
  * maybe run PCA on the physio dataset and then apply that DR/embedding to organoid dataset

TODO:

* perform PCA on random subsets of data
  
  * asses quality of reconstruction and etc.

* perform tSNE on data that has been reduced
  
  * partial dataset (10%)
  
  * full dataset
