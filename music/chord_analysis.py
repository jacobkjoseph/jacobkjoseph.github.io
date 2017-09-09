import csv
import glob
import re
import collections
import matplotlib.pyplot as plt
from nltk.corpus import stopwords


def split_base_suffix(chord):
    """ Splits chord into base and suffix (if applicable)
    >>> split_base_suffix('D#m7')
    ('D#', 'm7')
    """
    notes = "[CDEFGAB]"
    accidentals = "(?:#|##|b|bb)?"
    chord_base = re.findall(notes + accidentals, str(chord))[0]
    chord_suffix = chord.replace(chord_base, '')
    return chord_base, chord_suffix


def to_sharp(chord):
    """ Returns the corresponding sharp note for a given note
    >>> to_sharp('Bb')
    'A#'

    >>> to_sharp('B')
    'B'
    """
    flat_sharp_dict = {
        'Bb': 'A#',
        'Db': 'C#',
        'Eb': 'D#',
        'Gb': 'F#',
        'Ab': 'G#'
    }

    if chord in flat_sharp_dict:
        return (flat_sharp_dict.get(chord))
    else:
        return chord


def is_chord(text):
    """ Checks if the text is exactly a valid chord
    >>> is_chord('Ab')
    True

    >>> is_chord('Ab Ab')
    False

    >>> is_chord('Ab ')
    False

    >>> is_chord('H')
    False

    >>> is_chord('Amin#')
    False
    """
    notes = "[CDEFGAB]"
    accidentals = "(?:#|##|b|bb)?"
    modifiers = "(?:maj|min|m|sus|aug|dim)?"
    additions = "[0-9]?"
    return bool(re.match('^' + notes + accidentals + modifiers + additions + '$', text))


def is_chords_and_whitespace_only(text):
    """ Checks if the input consists of chords and whitespace only
    >>> is_chords_and_whitespace_only('C Dm Em F G Am Bdim C7 Dm7 Em7 F7 G7 \\n Am7 Bbm7')
    True

    >>> is_chords_and_whitespace_only('Happy Birthday to you')
    False

    >>> is_chords_and_whitespace_only('H F')
    False

    >>> is_chords_and_whitespace_only('A min')
    False
    """

    # Replace multiple whitespace with single whitespace
    text = ' '.join(text.split())
    # Split text into individual chords
    text = text.split(' ')
    for t in text:
        if not is_chord(t):
            return False
    return True


def find_key(text):
    # TODO: this should take chords instead of text
    keys = find_keys(text)
    if keys:
        # TODO improve logic. Currently the shortest chord that is common to
        # keys and available chords is returned as the key
        common = set(keys) & set(find_chords(text))
        return min(common, key=len)
    # chord_frequency = find_chord_frequency(find_chords(text))
    #
    #         for chord in copy.deepcopy(chord_frequency):
    #             if chord not in keys:
    #                 del chord_frequency[chord]
    #
    #         most_frequent_key = max(chord_frequency, key=chord_frequency.get)
    #         frequency = chord_frequency.get(most_frequent_key)
    #     return most_frequent_key
    else:
        return None


def find_keys_strict(unique_chords):
    """
    >>> find_keys_strict(['C', 'F', 'G'])
    ['C', 'Am']
    >>> find_keys_strict(['C2', 'F', 'G'])
    []
    """

    # TODO should take chords instead of unique_chords
    chords_in_c_major = find_chords(
        'C Dm Em F G Am Bdim C7 Dm7 Em7 F7 G7 Am7 Bbm7')
    chords_in_c_minor = find_chords(
        'Cm Ddim Eb Fm Gm Ab Bb Cm7 Dbm7 Eb7 Fm7 Gm7 Ab7 Bb7')
    keys = []
    # TODO should not have to check here that unique_chords is non-empty
    if unique_chords:
        for i in range(12):
            if set(unique_chords).issubset(transpose_chords(chords_in_c_major, i)):
                keys.append(transpose_chords(chords_in_c_major, i)[0])
            if set(unique_chords).issubset(transpose_chords(chords_in_c_minor, i)):
                keys.append(transpose_chords(chords_in_c_minor, i)[0])
    return keys


def find_keys(text):
    """
    >>> find_keys('C Dm Em F G Am Bdim C7 Dm7 Em7 F7 G7 Am7 Bbm7')
    ['C', 'Am']
    >>> find_keys('C Dm Em F G Am Bdim C7 Dm7 Em7 F7 G7 Am7 Bbm7 C2')
    ['C', 'Am']
    """
    # TODO: this should take chords instead of text

    keys = []
    chords = find_chords(text)
    if len(chords) == 0:
        return keys
    unique_chords = list(set(chords))
    chord_frequency = find_chord_frequency(chords)
    # Successively remove the least frequent chord while trying to find a key
    # match
    while True:
        keys = find_keys_strict(unique_chords)

        if len(keys) > 0 or len(unique_chords) == 0:
            return keys

        else:
            least_frequent_chord = min(
                chord_frequency, key=chord_frequency.get)
            del chord_frequency[least_frequent_chord]
            unique_chords.remove(least_frequent_chord)
            # chords[:] = [x for x in chords if x != least_frequent_chord]

    return keys


def find_steps(old_key, new_key):
    """
    >>> find_steps('A','B')
    2

    >>> find_steps('A','Bm')
    False
    """

    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    old_key_base, old_key_suffix = split_base_suffix(old_key)
    new_key_base, new_key_suffix = split_base_suffix(new_key)

    if old_key_suffix != new_key_suffix:
        return False

    return notes.index(new_key_base) - notes.index(old_key_base)


def transpose_chord(chord, steps):
    """ 
    >>> transpose_chord('A', 4)
    'C#'

    >>> transpose_chord('C#', -4)
    'A'

    >>> transpose_chord('Em', -2)
    'Dm'
    """

    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    chord_base, chord_suffix = split_base_suffix(chord)
    base_index = notes.index(chord_base)
    transposed_index = (base_index + steps) % 12
    transposed_chord_base = notes[transposed_index]
    return transposed_chord_base + chord_suffix


def transpose_chords(chords, steps):
    """ 
    >>> transpose_chords(['C', 'G', 'A', 'D', 'Em'], -2)
    ['A#', 'F', 'G', 'C', 'Dm']
    """
    return [transpose_chord(chord, steps) for chord in chords]


def multi_replace(string, replacements):
    # This code is from http://stackoverflow.com/
    substrs = sorted(replacements, key=len, reverse=True)
    regexp = re.compile('|'.join(map(re.escape, substrs)))
    return regexp.sub(lambda match: replacements[match.group(0)], string)


def transpose_line(line, steps):
    """
    >>> transpose_line('D    Em   D   G   A    D           G A D', -1)
    'C#   D#m  C#  F#  G#   C#          F#G#C#'
    """
    # Add extra space to accommodate potential 'expansion' during transpose.
    # Trailing space is removed after transpose is done.
    line += ' ' * 10
    chords = find_chords(line)

    unique_chords = list(set(chords))
    transposed_unique_chords = transpose_chords(unique_chords, steps)

    for i in range(len(unique_chords)):
        if len(unique_chords[i]) > len(transposed_unique_chords[i]):
            transposed_unique_chords[i] = transposed_unique_chords[
                i].ljust(len(unique_chords[i]), ' ')
        else:
            unique_chords[i] = unique_chords[i].ljust(
                len(transposed_unique_chords[i]), ' ')

    replacements = dict(zip(unique_chords, transposed_unique_chords))
    line = multi_replace(line, replacements)
    return line.rstrip()


def transpose_file_by_step(text, steps):
    lines = text.split('\n')
    output = ''
    for line in lines:
        if is_chords_and_whitespace_only(line):
            output += transpose_line(line, steps) + '\n'
        else:
            output += line + '\n'
    return output


def transpose_file_to_key(text, new_key):
    old_key = find_key(text)
    if old_key and find_steps(old_key, new_key):
        return transpose_file_by_step(text, find_steps(old_key, new_key))
    return False


def find_chords(text):
    """
    Will find chords only from valid chord lines
    >>> find_chords('C Dm Em F G Am Bdim C7 Dm7 Em7 F7 G7 Am7 Bbm7')
    ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'Bdim', 'C7', 'Dm7', 'Em7', 'F7', 'G7', 'Am7', 'A#m7']
    """
    notes = "[CDEFGAB]"
    accidentals = "(?:#|##|b|bb)?"
    modifiers = "(?:maj|min|m|sus|aug|dim)?"
    additions = "[0-9]?"

    chords = []

    lines = text.split('\n')
    for line in lines:
        if is_chords_and_whitespace_only(line):
            for chord in re.findall(r'\b' + notes + accidentals + modifiers + additions + r'(?!\w)', line):
                base, suffix = split_base_suffix(chord)
                base = to_sharp(base)
                chords.append(base + suffix)
    return chords


def find_first_chord(text):
    # TODO: this one line function is not required
    return find_chords(text)[0] if find_chords(text) else False


def find_last_chord(text):
    # TODO: this one line function is not required
    return find_chords(text)[-1] if find_chords(text) else False


def find_chord_frequency(chords):
    chord_frequency = {}
    for chord in chords:
        if chord in chord_frequency:
            chord_frequency[chord] += 1
        else:
            chord_frequency[chord] = 1
    return chord_frequency
    #         print(filename)
    #         for chord in sorted(chord_frequency, key=chord_frequency.get, reverse=True):
    #             print(chord, chord_frequency[chord])
    #         print('*' * 10)


def transpose_all_files_to_key(path, target_key):
    f_out = csv.writer(open('output.csv', 'w'), lineterminator='\n')
    f_out.writerow(['filename', 'transposed', 'key', 'keys', 'first_chord',
                    'last_chord', 'sorted chord_frequency', 'chord_frequency'])
    for filename in glob.glob(path + '\*.txt'):
        text = open(filename, 'r', encoding='utf-8').read()
        key = find_key(text)
        transposed = False
        if key and key != target_key and transpose_file_to_key(text, target_key):
            transposed = True
            # overwrite existing file with transposed file
            print(filename, '*** transposed ***')
            with open(filename, 'r+') as f:
                f.seek(0)
                f.write(transpose_file_to_key(text, target_key))
                f.truncate()
        chord_frequency = find_chord_frequency(find_chords(text))

        f_out.writerow([filename, transposed, key, find_keys(text), find_first_chord(
            text), find_last_chord(text), sorted(chord_frequency, key=chord_frequency.get, reverse=True),
                        chord_frequency])


def is_ascii(path):
    # TODO: logic is not correct
    for filename in glob.glob(path + '\*.txt'):
        text = open(filename, 'r').read()
        print(re.sub('[\x00-\x7f]', '', text))


def remove_chord_lines(text):
    # TODO: use this function
    lines = text.split('\n')
    output = ''
    for line in lines:
        if not is_chords_and_whitespace_only(line):
            output += line + '\n'
    return output


def remove_chord_lines_from_file(filename):
    text = open(filename, 'r', encoding='utf-8').read()

    with open(filename, 'r+') as f:
        f.seek(0)
        f.write(remove_chord_lines(text))
        f.truncate()


def remove_chord_lines_from_all_files(path):
    for filename in glob.glob(path + '\*.txt'):
        remove_chord_lines_from_file(filename)


def bag_of_words_from_file(filename):
    text = open(filename, 'r', encoding='utf-8').read()
    words = text.split()

    # Remove chords
    for word in words:
        if is_chord(word):
            words.remove(word)

    words = [word.lower() for word in words]

    # Convert list of words to frequency dictionary
    word_frequency = {}
    for word in words:
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1

    # Remove English stopwords
    for k in stopwords.words('english'):
        if k.lower() in word_frequency:
            del word_frequency[k]

    return word_frequency


def bag_of_words_from_all_files(path):
    a = {}
    for filename in glob.glob(path + '\*.txt'):
        b = bag_of_words_from_file(filename)
        for word, frequency in b.items():
            if word in a:
                a[word] += frequency
            else:
                a[word] = frequency
    return a


def plot_frequency_graph(word_frequency):
    plt.bar(range(len(word_frequency)), word_frequency.values(), align='center')
    plt.xticks(range(len(word_frequency)), word_frequency.keys())
    plt.show()


def main():
    # transpose_all_files_to_key(r'.\music', 'E')

    # remove_chord_lines_from_all_files(r'.\music')

    word_frequency = bag_of_words_from_all_files(r'.\music')
    top = dict()
    for word in (sorted(word_frequency, key=word_frequency.get, reverse=True)):
        # print(word, word_frequency[word])
        top[word] = word_frequency[word]
        if len(top) > 30:
            break
    print(top)
    plot_frequency_graph(top)


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    # Shift + Alt + F10 Choose configuration and run



    main()
