# localsearch_eval

2 python scripts you can use locally to evaluate localsearch's performance.

```bash
# Insert documents from the data folder into the localsearch server, thens runs a single "Index" command
# 
# For this initial evaluation, data was downloaded from: https://huggingface.co/datasets/wikitext
# 
# TODO: try this on a different dataset, full-text wikipedia articles, not just samples designed for text-generation models
task insert 


# Prompts user for a text query, and sends it to the server. Then displays the resulting documents with their scores and content.
# 
task query
```