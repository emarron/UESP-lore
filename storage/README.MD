# Storage Section Readme

## Overview

This section contains storage for LlamaIndex vector stores to be used with llama_index_bots. These vector stores are essential for enabling efficient and effective querying of The Elder Scrolls lore data using Llama models.

## Download Link

To download the vector stores, use the following link:
[MediaFire Storage](https://app.mediafire.com/83516vc48hz8v)

## Index Creation

If you create a new index from the `data` directory, it will be stored in this section. Ensure that the new indexes follow the prescribed naming convention for consistency.

## Naming Convention

The naming convention for the vector stores is as follows:

```
storage_%embedding_model%_%llm_model%
```

For example, if you are using an embedding model named "embed_model_v1" and an LLM model named "llama_model_v1", the storage name would be:

```
storage_embed_model_v1_llama_model_v1
```

## Dataset Information

All the vector stores in this section are trained on the UESP 7,000 cleaned and tagged dataset. The dataset was last updated on (YY/MM/DD) 24/06/26.

## Important Notes

- Ensure you use the appropriate embedding and LLM models when creating or using vector stores to maintain compatibility.
- Regularly check for updates to the dataset and vector stores to ensure you have the most recent and accurate information.

