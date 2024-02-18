

This branch holds the submission materials for the demo paper under review for IJCAI-24
titled "Generating Theory-Grounded Responses for Mental Health Forum Questions"
<ol>
<li>We provide compiled guidelines from multiple resources for treating sample EMSs in "Schema Interventions" (Compiled by Beng Heng Ang)
</li>
<li>The treatment suggestions lists used in response generation can be found in the "treatments" and "rewritten_treatments" directories. 
Top-3 matching suggestions for a given question text
are used to prompt the LLM during response generation.
</li>
<li>
The complete code will be released after review with the outline released in the mydemo*.py for an idea.
</li>
<li>
Outputs contains sample runs of our demo on the dataset released in the previous paper (with counselor-annotated EMS labels).
These files also contain the "default" response obtained by prompting the GPT 3.5 LLM as well as an actual counselor response
from <a href="https://github.com/nbertagnolli/counsel-chat">CounselChat dataset</a> released by Nicolas Bertagnolli.
</li>
</ol>

<br>
<br>

Please check under the <a href="https://github.com/NUS-IDS/ems_mentalhealth/tree/emnlpfindings"> emnlpfindings branch </a> for the repository 
of our EMNLP Findings 2023 paper 

<a href="https://aclanthology.org/2023.findings-emnlp.792/">Identifying Early Maladaptive Schemas from Mental Health Question Texts" </a>
Sujatha Das Gollapalli, Beng Heng Ang, See-Kiong Ng
