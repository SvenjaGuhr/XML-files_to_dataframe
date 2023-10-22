# XML-files_to_dataframe

Two different scripts

1) BPO Corpus from XML to CSV [https://github.com/SvenjaGuhr/XML-files_to_dataframe/blob/main/Tidy_BPO_suspense_files-to-data-frame.ipynb]
Generates a corpus by loading all xml files from a chosen directory, prepares the text data, extracts xml-tagged content, filters, creates and stores subsets of xml-tagged data.

2) Sound annotated XML-file to CSV [https://github.com/SvenjaGuhr/XML-files_to_dataframe/blob/main/xml_sound_annotated_to_csv.ipynb]
Opens an XML-file, reads the text as a string, removes the xml-frame, does some cleaning, tokenizes the text using spacy en_core_web_sm while excluding the xml-tag-annotated unit "<sound>word</sound>" saving all in a dataframe with the column "tokens". Unfortunately, the "<" and ">" get splitted from the unit anyway. I haven't found a direct way yet, but the following heuristic:  if the pattern r"<sound>(.*?)</sound>" is found in the "tokens"-column, add a "sound_annotation"-column with the word in between the XML-tags. In a further step, I add another column with default annotation "O" for "no sound annotation". Afterwards, I iterate again over the "tokens"-column, if the pattern r"<sound>(.*?)</sound>" is found in the "tokens"-column, overwrite the entry with the related cell entry from the "sound_annotation"-column which is the sound word extracted earlier. In a last step, I clean the data frame column "tokens" from empty entries, and "<|>", reset the index, and then delete the "sound_annotation"-column that is not needed anymore to get a pretty data frame with the sound annotations.
This script can be modified indicating another xml-tag and regex pattern of choice.
