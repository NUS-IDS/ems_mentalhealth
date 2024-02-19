#Prompt for selecting the most applicable treatment suggestions


select_prompt_pfx="Consider the following list of suggestions: "

select_prompt_middle="From the above list select up to three most applicable for the following scenario: "

select_prompt_sfx="Only return the numbers of items from the list above as a comma-separated list."


#Prompt for generating ST-infused responses

counselor_prompt_pfx="As a mental health counselor, respond empathetically using the following suggestions "

counselor_prompt_sfx= " and respond to the following QA forum post. Post= "

#Default prompt for GPT 
 prompt="As a mental health counselor, respond empathetically to the following QA forum post. Post= "
