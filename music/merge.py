import glob
import os
import time
import re
import sys
from bs4 import BeautifulSoup
# This chord_analysis.py file is a local copy
from chord_analysis import find_first_chord
from chord_analysis import find_chords

# File
# ToDo move out all lyrics files from the GitHub folder
# ToDo move out the script from the GitHub folder
# ToDo lyric files should not be edited by the script
# ToDo remove meta info ('_A_', '_E_', '_H_', '_L_', '_M_' etc.) from file name and make it part of the file content
# ToDo add tags to files ('praise', 'worship', 'thanksgiving', 'prayer', 'holy spirit' etc.)
# ToDo logic to handle encoding issues UTF-8
# ToDo logic to detect characters in chord lines that leads to chords not getting detected
# ToDo leads (like chords) should also be transpose-able
# AI
# ToDo detect and annotate chorus, verses, hyperlinks (Youtube, Chordify) etc.
# ToDo search by lyrics
# ToDo cluster by similar chords, lyrics
# Todo classify by lyrics
# JavaScript
# ToDo write own JS for for table sort, transpose chords etc.
# ToDo show/hide chords
# ToDo auto adjust song to avoid scrolling when playing guitar
# ToDo improve the look and feel
# ToDo ability to choose font, color etc
# ToDo select/star a list of songs
# ToDo email a comment about a song

lang = {'a': 'Aramaic', 'e': 'English', 'h': 'Hindi', 'l': 'Latin', 'm': 'Malayalam'}


def get_title_from_filename(name, replace_char):
    name, extension = os.path.splitext(name)
    name = remove_lang_prefix(name)
    name = clean_filename(name, replace_char)
    name = name.title()
    return name


def remove_lang_prefix(name):
    for _ in lang:
        if name.startswith('_' + _ + '_'):
            name = name[3:]
    return name


def clean_filename(name, replace_char='_'):
    name = name.lower()
    filename, file_extension = os.path.splitext(name)
    filename = re.sub('[^a-zA-Z]+', replace_char, filename)
    return filename + file_extension


def create_song_html_from_template(txt_file_name):
    html_file_name = txt_file_name.replace('.txt', '.html')
    soup = BeautifulSoup(open('song.template'), 'html.parser')
    soup.head.title.string = remove_lang_prefix(html_file_name[:-5]).replace('_', ' ')
    soup.body.pre.string = open(txt_file_name, 'r', encoding='utf8', errors='ignore').read()
    soup.body.pre['data-key'] = find_first_chord(open(txt_file_name, 'r', encoding='utf-8').read())
    soup = soup.prettify()
    with open(html_file_name, 'w') as file:
        file.write(str(soup))


def main():
    # Delete all .html files
    for file in glob.glob('*.html'):
        os.remove(file)

    # Rename all .txt file names
    for file in glob.glob('*.txt'):
        os.rename(file, clean_filename(file))

    # Generate a .html file for each .txt file
    for text_file_name in glob.glob('*.txt'):
        create_song_html_from_template(text_file_name)

    # Generate the index.html file
    soup = BeautifulSoup(open('index.template'), 'html.parser')
    for file in glob.glob('*.html'):
        # ToDo improve the way the <tr> tags are appended to the table
        temp_soup = BeautifulSoup('<b></b>', 'html.parser')

        a_tag = temp_soup.new_tag('a', href=file, target='_blank')
        a_tag.string = get_title_from_filename(file, ' ')
        td1_tag = temp_soup.new_tag('td')
        td1_tag.append(a_tag)

        td2_tag = temp_soup.new_tag('td')
        td2_tag.string = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(file.replace('.html', '.txt'))))

        td3_tag = temp_soup.new_tag('td')
        td3_tag.string = time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(file.replace('.html', '.txt'))))

        td4_tag = temp_soup.new_tag('td')
        td4_tag.string = lang[file[1]]

        td5_tag = temp_soup.new_tag('td')
        key = find_first_chord(open(file.replace('.html', '.txt'), 'r', encoding='utf-8').read())
        if key:
            td5_tag.string = key
        else:
            td5_tag.string = ''

        td6_tag = temp_soup.new_tag('td')
        chords = find_chords(open(file.replace('.html', '.txt'), 'r', encoding='utf-8').read())
        if key:
            td6_tag.string = ', '.join(sorted(list(set(chords))))
        else:
            td6_tag.string = ''

        tr_tag = temp_soup.new_tag('tr')
        tr_tag.append(td1_tag)
        tr_tag.append(td2_tag)
        tr_tag.append(td3_tag)
        tr_tag.append(td4_tag)
        tr_tag.append(td5_tag)
        tr_tag.append(td6_tag)

        soup.body.table.append(tr_tag)

    with open('index.html', 'w') as file:
        soup = soup.prettify()
        file.write(str(soup))


if __name__ == '__main__':
    main()
