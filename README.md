
We used Python 3.11.4 for our experiments and
the libraries used by us are listed in code/requirements.txt 

("pip install -r requirements.txt" )

--

The data with expert annotations is available as a TSV file in the directory "gold" along with the list of labels 
as well as the definitions from schema therapy and prompts in the directory "resources".

The labels list (provided in the gold directory) is used in computing
overlap since some LLM models may not predict the label completely

--
Please check code/README for running the code
