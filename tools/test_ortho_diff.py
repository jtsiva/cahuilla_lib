import pytest
import ortho_diff

def word_list_check():
    saubel_list = ["waxachill", "sasang", "’ivillu’at"]
    seiler_list = ["waxačil̃", "sasaŋ", "ʔivil̃uʔat"]
    ipa_list = ["wɑxɑt͡ʃiʎ", "sɑsɑŋ", "ʔiviʎuʔɑt"]

    #iterate over all the lists and make sure that each pair
    #and direction is correct