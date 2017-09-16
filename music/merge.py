import glob
import os
import time
import re
import sys
from bs4 import BeautifulSoup
# This chord_analysis.py file is a local copy
from chord_analysis import find_first_chord


# File
# ToDo move out all lyric files from the Github folder
# ToDo move out the script from the Github folder
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


def clean_name(name, replace_char='_'):
    name = name.title()
    for a in ['_A_', '_E_', '_H_', '_L_', '_M_']:
        if name.startswith(a):
            name = name[3:]
    name = re.sub('[^a-zA-Z]+', replace_char, name)
    return name


def create_song_html_from_template(txt_file_name):
    html_file_name = txt_file_name.replace('.txt', '.html')
    soup = BeautifulSoup(open('song.template'), "html.parser")
    soup.head.title.string = clean_name(txt_file_name[:-4], ' ')
    soup.body.pre.string = open(txt_file_name, 'r', encoding='utf8', errors='ignore').read()
    soup.body.pre['data-key'] = find_first_chord(open(txt_file_name, 'r', encoding='utf-8').read())
    soup = soup.prettify()
    with open(html_file_name, "w") as file:
        file.write(str(soup))


def main():
    lang = {'A': 'Aramaic', 'E': 'English', 'H': 'Hindi', 'L': 'Latin', 'M': 'Malayalam'}

    # Delete all .html files
    for file in glob.glob("*.html"):
        os.remove(file)

    # Standardize all .txt file names
    for file in glob.glob("*.txt"):
        os.rename(file, re.sub('[^a-zA-Z]+', '_', file[:-4]).title() + '.txt')

    # Generate an .html for each .txt
    for fileName in glob.glob("*.txt"):
        create_song_html_from_template(fileName)

    # Generate the index.html file
    soup = BeautifulSoup(open('index.template'), "html.parser")
    for file in glob.glob('*.html'):
        filename = file.replace(" ", "%20")
        title = clean_name(file[:-5], ' ')
        t1 = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(file.replace('.html', '.txt'))))
        t2 = time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(file.replace('.html', '.txt'))))
        lang_ = lang[file[1]]

        # ToDo improve the way the <tr> tags are appended to the table
        temp_soup = BeautifulSoup("<b></b>", "html.parser")

        a_tag = temp_soup.new_tag('a', href=filename, target="_blank")
        a_tag.string = title
        td1_tag = temp_soup.new_tag('td')
        td1_tag.append(a_tag)

        td2_tag = temp_soup.new_tag('td')
        td2_tag.string = t1

        td3_tag = temp_soup.new_tag('td')
        td3_tag.string = t2

        td4_tag = temp_soup.new_tag('td')
        td4_tag.string = lang_

        tr_tag = temp_soup.new_tag('tr')
        tr_tag.append(td1_tag)
        tr_tag.append(td2_tag)
        tr_tag.append(td3_tag)
        tr_tag.append(td4_tag)

        soup.body.table.append(tr_tag)

    with open('index.html', "w") as file:
        soup = soup.prettify()
        file.write(str(soup))


if __name__ == '__main__':
    main()
