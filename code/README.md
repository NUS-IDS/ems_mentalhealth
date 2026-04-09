
code used for obtaining labels for mindline/7cups

The code is simple Python script which makes use of OpenAI api.

Our experiments used:
openai version 1.108.0

LLMs used in experiments include
"gpt-5-mini" and "gemini-3-flash-preview" 

The file [Common.py](Common.py) needs to be edited suitably to include your own API keys for OpenAI/Google.

The LLM prompts use the schema definitions from [../resources/schema_defs.tsv](../resources/schema_defs.tsv)

The predictions on the EMNLP dataset from various models are include in [../stlabels](../stlabels) directory.


The output labels can be obtained by using processEMNLP. For example:

```python processEMNLP.py ../gold/gold.tsv output.csv gpt```

whereas the metrics computed on these results by running

```python computeMeasures.py ../gold output.csv```
