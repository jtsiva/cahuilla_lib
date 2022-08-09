import pytest
from orthography import Orthography

def test_word_list_check():
    ortho = Orthography ('../sounds/orthography.json')
    test_words = {"saubel_chemivillu" : ["wáxachill", "sásang", "'ívillu'at"],
    "seiler_dictionary" : ["wáxačil̃", "sásaŋ", "ʔívil̃uʔat"],
    "IPA" : ["wɑxɑt͡ʃiʎ", "sɑsɑŋ", "ʔíviʎuʔɑt"]}

    #iterate over all the lists and make sure that each pair
    #and direction is correct
    for ortho_name in test_words:
        for word1 in test_words[ortho_name]:
            convert_output = ortho.convert_orthography(word1)
            for key, word2 in convert_output["converted"].items():
                assert (word2 in test_words[key])