# Organoid Analysis

**This repo contains the instructions and code for the re-analysis of data found in the paper ["Cell stress in cortical organoids impairs molecular subtype specification"](https://www.nature.com/articles/s41586-020-1962-0), published in Nature on January 29, 2020**

The motivation behind these analyses is to explore computational methods of reconstructing the range of cell subtypes in cortical organoids. The hypothesis is that organoid stress induces local and/or global transformations in the gene expression profile of cell subtypes such that direct comparison of gene expression profiles of cell subtypes collected directly from human cortical areas are not suitable to classify cell subtypes. We believe that cell classes and subtypes are still present in organoids, and that their classes and subtypes are computationally recoverable, possible after some deformation/registration/regression in gene expression space.

## 1. The data

In the paper, they mention using the following datasets:

* Dissociated cells from five cortical samples collected at 6-22 gestational weeks from seven regions (prefrontal, motor, parietal, somatosensory, primary visual, hippocampus), total 189,409 cells
  
  * Data was found [here](https://cells.ucsc.edu/?ds=organoidreportcard), at the UCSC Organoid Report Card website, totaling approx 263mb extracted to 3.5gb.

* Forebrain organoids (37) following three previously published protocols, totalling 235,121 cells, with scRNAseq data collected at 3,5,8,10,15, 24 weeks. 
  
  * One set was found [here](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE132672), on the NCBI website, totaling approx. 1.9gb extracted to 4gb, saved in folder "Organoid_NCBI"
  
  * Another set was found [here]([UCSC Cell Browser](https://cells.ucsc.edu/?ds=organoidreportcard)), on the UCSC Organoid report card website, totaling approx. 251mb extracted to 3.5gb, saved in folder "Organoid_UCSC"

* Previously-published organoid single-cell data from 276,054 cells across 8 protocols. 
  
  * citation 3-5, 8,9,13,15
    
    * "Camp JG. Human cerebral organoids recapitulate gene expresion programs in fetal neocortex development"
    
    * "Pollen, AA. Establishing cerebral organoids of human-specific brain evolution"
      
      * Found [here](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE124299), NCBI GEO, not yet downloaded
    
    * "Velasco, S. Individual brain organoids reproducibly form cell diversity of the human cerebral cortex"
      
      * Found [here](https://www-ncbi-nlm-nih-gov.ucsf.idm.oclc.org/geo/query/acc.cgi?acc=GSE129519), NCBI GEO (not yet downloaded) 
    
    * Sloan, S.A. Human astrocyte maturation captured in 3D cerebral cortical spheroids derived from pluripotent stem cells"
      
      * Found [here](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE99951), NCBI GEO (not yet downloaded)
    
    * Amiri, A. Transcriptome and epigenome landscape of human cortical development modeled in organoids
    
    * Quadrato, G. Cell diversity and network dynamics in photosensitive human brain organoids
      
      * Found [here](https://www-ncbi-nlm-nih-gov.ucsf.idm.oclc.org/geo/query/acc.cgi?acc=GSE86153), not yet downloaded
    
    * Marton, R.M. Differentiation and maturation of oligodendrocytes in human three-dimensional neural cultures. 
      
      * Found [here](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE115011), not yet downloaded

## 2. Pre-processing

Batch correction (citation 39)

* each cell within a batch was normalized to highest expressing gene, making range of expression [0,1]

* values were multiplied by average number of counts within a batch

* normalized datasets piped into Seurat v.2 (citation 40)
  
  * discard outliers
    
    * cells with < 500 genes per cell
    
    * more than 10% of reads aligning to mitochondrial genes
  
  * log_2 transformed, variable genes were calculated using default Seurat parameters

Louvain-Jaccard clustering