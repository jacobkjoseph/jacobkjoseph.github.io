import glob
import os
import time


def clean_name(name):
    clean_name = name
    clean_name = clean_name.replace('_A_', '')
    clean_name = clean_name.replace('_E_', '')
    clean_name = clean_name.replace('_H_', '')
    clean_name = clean_name.replace('_L_', '')
    clean_name = clean_name.replace('_M_', '')
    clean_name = clean_name.replace('.Html', '')
    clean_name = clean_name.replace('_', ' ')
    clean_name = clean_name.replace('-', ' ')
    return clean_name


def main():
    # Initialize static html
    with open('helper.py1', 'r') as f:
        static_html = f.readlines()
    header_1 = ''.join(static_html[0:6])
    header_2 = ''.join(static_html[8:13])
    footer_1 = ''.join(static_html[15:21])
    index_header = ''.join(static_html[23:35])
    index_footer = ''.join(static_html[37:41])
    
    # Rename all .txt files
    for file in glob.glob("*.txt"):
        os.rename(file, file.replace(' ', '_'))

    # Delete all .html files
    for file in glob.glob("*.html"):
        os.remove(file)

    # Generate an .html for each .txt
    htmlFiles = []
    for fileName in glob.glob("*.txt"):
        newFile = fileName.replace('.txt', '.html')
        # Populate the list of html files
        htmlFiles.append(newFile)
        with open(newFile, 'w') as outfile:
            print(fileName)
            # -4 is to skip the file extension (.txt)
            outfile.write(header_1 + clean_name(fileName[:-4]) + header_2 + open(fileName, 'r', encoding='utf8', errors='ignore').read() + footer_1)

    # Generate the index.html file
    f = open("index.html", 'w')

    f.write(index_header)

    lang = {'A': 'Aramaic','E': 'English', 'H': 'Hindi', 'L': 'Latin', 'M': 'Malayalam'}

    for file in htmlFiles:
        f.write("<tr><td><a href =\"" + file.replace(" ", "%20") + "\" target=\"_blank\">" + clean_name(
            file.title()) + "</td><td>" + time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(
            file.replace('.html', '.txt')))) + "</td><td>" + time.strftime('%m/%d/%Y', time.gmtime(
            os.path.getctime(file.replace('.html', '.txt')))) + "</td><td>" + lang[file[1]] + "</td></tr>\n")

    f.write(index_footer)
    f.close()


if __name__ == '__main__':
    main()
