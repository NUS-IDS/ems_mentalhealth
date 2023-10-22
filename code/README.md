


The general flavor of running this code involves:
1. Setting the parameters in the config file (Such as model names, dictionary paths etc)
2. Run Predictor code with two parameters the "data.tsv" and output filepath (We write out the preds as a TSV file)
3. Compute the measures using computeMeasures (provide the gold directory path and the predictions TSV files as input)

For example:
After ensuring the correct paths and names in SVPConfig.py, run 

python SVPredictor.py ../gold/gold.tsv svp.preds.tsv 

python computeMeasures.py ../gold svp.preds.tsv

We provide code for the prompt-based FlanT5, Entailment-based (EPM) and Similarity/Voting-based (SVP) models discussed
in the paper.

NOTE: The EPM code takes a long time to run in comparison with the others because
of the entailment check for every sentence in the question with the 232 statements from Young's Schema Questionaire
whereas the SVP code is the fastest since it only involves quick embeddings similarity computations.





