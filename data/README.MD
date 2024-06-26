
# Elder Scrolls Lore Data Readme

This is the master directory of data for the entire project:
**[Mediafire Master Folder](https://app.mediafire.com/x3nhxfhn1m3o1)**

There are these subdirectories:
- chat_gpt_assistant_data: refer to the `chat_gpt_assistant` section.
- llamaindex - refer to `storage` and `llama_index_bot` section.
- OLD - ignore
- **imperial library** - see below
- **UESP** - see below

This section will go over the data of `imperial library` and `UESP`


## Sources:


### UESP (Unofficial Elder Scrolls Pages)
- **Namespace**: Lore
- **URL**: [UESP Lore](https://en.uesp.net/wiki/Special:AllPages?from=&to=&namespace=130&hideredirects=1)

### Imperial Library
- **URL**: [Imperial Library](https://www.imperial-library.info)

## Datasets:

### UESP

- **cleaned_articles_tagged**: Contains 7,000 articles, 3/7 of which are books. JSON files for Books, People, and Places include extra fields.
- **UESP_LORE_DUMP**: HTML dump of the 7,000 articles.
- **intermediate cleaning**: Contains intermediate cleaning stages.

### Imperial Library

- **imperial_library_HTML_DUMP.7z**: Raw HTML dump of the website.
- **imperial_library_JSONS.7z**: JSON files containing titles and contents as HTML.
- **imperial_library_jsons_books.7z**: Cleaned JSON files of books from the website. This has about 5,000 JSON.
- if you want the consolidated books jsons (only for chatgpt_assistant) they are under chatgpt_assistant_data instead of Imperial Library. This has 18 JSONs, corresponding to each book category like "songs & poems"

### For more information about the cleaned files read the `cleaning` section.