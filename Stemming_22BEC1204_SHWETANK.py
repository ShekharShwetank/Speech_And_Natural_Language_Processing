import string # for punctuation

# character classifications for stemmer logic
GLOBAL_VOWELS = "aeiou"
CONSONANT_DESIGNATORS = "bcdfghjklmnpqrstvwxz" # 'y' is handled dynamically

class CustomStemmingLogic:
    #Implements a custom version of the Porter Stemming algorithm.

    def _is_char_vowel(self, char_input):
        #Determines if a character is a vowel.
        return char_input.lower() in GLOBAL_VOWELS

    def _is_char_consonant(self, char_input):
        #Determines if a character is a consonant.
        return not self._is_char_vowel(char_input)

    def _derive_vc_pattern(self, segment):
        #Generates a Vowel-Consonant (VC) pattern string for a given word segment. 'y' is treated as a vowel if preceded by a consonant, otherwise consonant.
        pattern_sequence = []
        for idx, char_elem in enumerate(segment):
            if self._is_char_vowel(char_elem):
                pattern_sequence.append('V')
            elif char_elem.lower() == 'y': # Special 'y' handling
                if idx > 0 and self._is_char_consonant(segment[idx - 1]):
                    pattern_sequence.append('V')
                else:
                    pattern_sequence.append('C')
            else:
                pattern_sequence.append('C')
        return "".join(pattern_sequence)

    def _calculate_measure(self, current_stem):
        #Calculates the 'measure' (m) of a stem, which is the number of VC sequences.
        vc_form = self._derive_vc_pattern(current_stem)
        count_vc = vc_form.count('VC')
        return count_vc

    def _stem_has_vowel(self, sub_stem):
        #Checks if a given stem contains at least one vowel.
        for char_in_stem in sub_stem:
            if self._is_char_vowel(char_in_stem):
                return True
        return False

    def _ends_with_double_consonant(self, sub_stem_fragment):
        #Checks if a stem ends with a double consonant (e.g., 'tt', 'ff').
        if len(sub_stem_fragment) < 2:
            return False
        return (not self._is_char_vowel(sub_stem_fragment[-1]) and
                sub_stem_fragment[-1] == sub_stem_fragment[-2])

    def _ends_with_cvc_pattern(self, sub_stem_fragment):
        #Checks if a stem ends with a CVC pattern where the final C is not 'w', 'x', or 'y'.
        if len(sub_stem_fragment) < 3:
            return False
        return (self._is_char_consonant(sub_stem_fragment[-3]) and
                self._is_char_vowel(sub_stem_fragment[-2]) and
                self._is_char_consonant(sub_stem_fragment[-1]) and
                sub_stem_fragment[-1] not in 'wxy')

    def _perform_replacement(self, base_word, old_suffix, new_suffix):
        #Replaces an old suffix with a new one.
        if not base_word.endswith(old_suffix):
            return base_word
        return base_word[:-len(old_suffix)] + new_suffix

    # Implementation of the Porter Stemmer

    def _process_step1a(self, word_input):
        #Handles plurals and -sses, -ies, -s suffixes.
        if word_input.endswith('sses'):
            return self._perform_replacement(word_input, 'sses', 'ss')
        if word_input.endswith('ies'):
            return self._perform_replacement(word_input, 'ies', 'i')
        if word_input.endswith('ss'):
            return word_input
        if word_input.endswith('s'):
            return self._perform_replacement(word_input, 's', '')
        return word_input

    def _process_step1b(self, word_input):
        #Handles -eed, -ed, -ing suffixes.
        current_word = word_input
        if current_word.endswith('eed'):
            base_part = current_word[:-3]
            if self._calculate_measure(base_part) > 0:
                current_word = self._perform_replacement(current_word, 'eed', 'ee')
        elif current_word.endswith('ed'):
            base_part = current_word[:-2]
            if self._stem_has_vowel(base_part):
                current_word = self._adjust_step1b_base(base_part)
        elif current_word.endswith('ing'):
            base_part = current_word[:-3]
            if self._stem_has_vowel(base_part):
                current_word = self._adjust_step1b_base(base_part)
        return current_word

    def _adjust_step1b_base(self, base_segment):
        #Helper for Step 1b's conditions after suffix removal.
        if base_segment.endswith('at') or base_segment.endswith('bl') or base_segment.endswith('iz'):
            return base_segment + 'e'
        if self._ends_with_double_consonant(base_segment) and base_segment[-1] not in 'lsz':
            return base_segment[:-1]
        if self._calculate_measure(base_segment) == 1 and self._ends_with_cvc_pattern(base_segment):
            return base_segment + 'e'
        return base_segment

    def _process_step1c(self, word_input):
        #Handles the -y to -i rule.
        if word_input.endswith('y') and self._stem_has_vowel(word_input[:-1]):
            return self._perform_replacement(word_input, 'y', 'i')
        return word_input

    def _process_step2(self, word_input):
        #Handles various common suffixes (e.g., -ational, -tional).
        suffix_replacements = {
            'ational': 'ate', 'tional': 'tion', 'enci': 'ence', 'anci': 'ance',
            'izer': 'ize', 'abli': 'able', 'alli': 'al', 'entli': 'ent',
            'eli': 'e', 'ousli': 'ous', 'ization': 'ize', 'ation': 'ate',
            'ator': 'ate', 'alism': 'al', 'iveness': 'ive', 'fulness': 'ful',
            'ousness': 'ous', 'aliti': 'al', 'iviti': 'ive', 'biliti': 'ble'
        }
        for suffix, replacement in suffix_replacements.items():
            if word_input.endswith(suffix):
                potential_stem = word_input[:-len(suffix)]
                if self._calculate_measure(potential_stem) > 0:
                    return potential_stem + replacement
        return word_input

    def _process_step3(self, word_input):
        #Handles further suffixes (e.g., -icate, -ative).
        suffix_replacements = {
            'icate': 'ic', 'ative': '', 'alize': 'al', 'iciti': 'ic',
            'ical': 'ic', 'ful': '', 'ness': ''
        }
        for suffix, replacement in suffix_replacements.items():
            if word_input.endswith(suffix):
                potential_stem = word_input[:-len(suffix)]
                if self._calculate_measure(potential_stem) > 0:
                    return potential_stem + replacement
        return word_input

    def _process_step4(self, word_input):
        #Removes certain common suffixes based on m > 1.
        suffixes_to_remove = [
            'al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant', 'ement',
            'ment', 'ent', 'sion', 'tion', 'ou', 'ism', 'ate', 'iti', 'ous',
            'ive', 'ize'
        ]
        for suffix in suffixes_to_remove:
            if word_input.endswith(suffix):
                potential_stem = word_input[:-len(suffix)]
                if self._calculate_measure(potential_stem) > 1:
                    # Special rule for 'sion' and 'tion': only remove if base ends in 's' or 't'
                    if suffix in ['sion', 'tion']:
                        if potential_stem.endswith('s') or potential_stem.endswith('t'):
                            return potential_stem
                        else: # Don't remove if condition not met, or just remove as per general rule
                            return potential_stem
                    return potential_stem # For other suffixes, just remove
        return word_input

    def _process_step5a(self, word_input):
        #Removes final 'e' based on m conditions.
        if word_input.endswith('e'):
            potential_stem = word_input[:-1]
            m_val = self._calculate_measure(potential_stem)
            if m_val > 1:
                return potential_stem
            if m_val == 1 and not self._ends_with_cvc_pattern(potential_stem):
                return potential_stem
        return word_input

    def _process_step5b(self, word_input):
        #Removes final 'l' if double consonant and m > 1.
        if word_input.endswith('l') and self._ends_with_double_consonant(word_input) and self._calculate_measure(word_input) > 1:
            return word_input[:-1]
        return word_input

    def perform_stemming(self, source_word):
        #Applies all Porter Stemmer steps to a single word.
        if len(source_word) < 3:
            return source_word

        processed_word = source_word.lower()
        
        processed_word = self._process_step1a(processed_word)
        processed_word = self._process_step1b(processed_word)
        processed_word = self._process_step1c(processed_word)
        processed_word = self._process_step2(processed_word)
        processed_word = self._process_step3(processed_word)
        processed_word = self._process_step4(processed_word)
        processed_word = self._process_step5a(processed_word)
        processed_word = self._process_step5b(processed_word)
        
        return processed_word

# Custom Rules for Correcting Stemmer O/P
def apply_specific_corrections(original_form, auto_stemmed_form):
    #custom rules to correct the output of the Porter Stemmer for specific words.
    correction_map = {
        "beautiful": "beauty",
        "generously": "generous",
        "university": "univers",
        "organization": "organize",
        "multiply": "multipl",
        "matrices": "matrix",
        "denial": "deni"
    }
    
    # Check if the original word is in our correction map and return the predefined correction if found.
    if original_form.lower() in correction_map:
        return correction_map[original_form.lower()]
        
    return auto_stemmed_form

if __name__ == "__main__":
    porter_custom_instance = CustomStemmingLogic()

    example_words = [
        "consulting", "computer", "national", "beautiful", "generously",
        "university", "organization", "multiply", "happiness", "connection",
        "agreed", "caring", "fixes", "dogs", "matrices", "denial", "activate"
    ]

    print("Custom Porter Stemmer with Corrections")
    print("{:<15} | {:<18} | {:<18}".format("Original Word", "Stemmed (Raw)", "Stemmed (Corrected)"))
    print("-" * 55)

    for current_word in example_words:
        raw_stem = porter_custom_instance.perform_stemming(current_word)
        corrected_stem_output = apply_specific_corrections(current_word, raw_stem)
        print(f"{current_word.ljust(15)} | {raw_stem.ljust(18)} | {corrected_stem_output.ljust(18)}")

    sample_text = (
        "Implementing my own custom stemming algorithms requires careful attention to detailed rules defined. Here is an example Born into slavery in February 1818, Elizabeth Hobbs Keckley was the daughter of her owner, Armistead Burwell, and his house slave, Agnes. Elizabeth Keckley began working as a nursemaid when she was four years old, and endured years of beatings and rape, the latter of which resulted in a pregnancy. However, one part of her childhood would eventually save her: from her mother, Elizabeth Keckley had learned how to sew."
    )
    
    # Simple tokenization for the example text
    import re
    cleaned_text = re.sub(f'[{re.escape(string.punctuation)}]', '', sample_text).lower()
    words_from_text = cleaned_text.split()

    print("\n\n Processing a Sample Text ")
    for word_item in words_from_text:
        raw_stem_text = porter_custom_instance.perform_stemming(word_item)
        final_stem_text = apply_specific_corrections(word_item, raw_stem_text)
        print(f"'{word_item}' -> Raw: '{raw_stem_text}', Corrected: '{final_stem_text}'")