import glob
import os
import time


def clean_name(name):
    clean_name = name
    clean_name = clean_name.replace('_E_', '')
    clean_name = clean_name.replace('_H_', '')
    clean_name = clean_name.replace('_M_', '')
    clean_name = clean_name.replace('.Html', '')
    clean_name = clean_name.replace('_', ' ')
    clean_name = clean_name.replace('-', ' ')
    return clean_name


def main():
    # Rename all .txt files
    for file in glob.glob("*.txt"):
        os.rename(file,file.replace(' ','_'))
	
	
	# Delete all .html files
    for file in glob.glob("*.html"):
        os.remove(file)

    head1 = '''
<!doctype html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>'''

    head2 = '''
        </title>
        <link rel="stylesheet" type="text/css" href="jquery.transposer.css" />
    </head>
    <body>
        <pre id="content" data-key="C"  onclick="myFunction()">'''
    tail = '''
        </pre>
        <script type="text/javascript" src="jquery.min.js"></script>
        <script type="text/javascript" src="jquery.transposer.js"></script>
        <script type="text/javascript">$(function() {$("pre").transpose();});</script>
    </body>
</html>'''

    # Generate a .html for each .txt
    htmlFiles = []
    for fileName in glob.glob("*.txt"):
        newFile = fileName.replace('.txt', '.html')
        # Populate the list of html files
        htmlFiles.append(newFile)
        with open(newFile, 'w') as outfile:
            # -4 is to skip the file extension (.txt)
            outfile.write(
                head1 + clean_name(fileName[:-4]) + head2 + open(fileName, 'r', encoding='utf8').read() + tail)

    # Generate the index.html file
    f = open("index.html", 'w')
    # index header
    temp = '''
<!doctype html>
<html>
	<head>
		<title>Music</title>
		<link rel="stylesheet" type="text/css" href="style.css" />
		<link rel="icon" type="image/x-icon" href="../img/favicon.ico">
	</head>
	<body>
		<table class="sortable">
		<tr>
			<th>Name</th><th>Modified</th><th>Created</th><th>Language</th>
		</tr>
		'''
    f.write(temp)
    for file in htmlFiles:
        f.write("<tr><td><a href =\"" + file.replace(" ", "%20") + "\" target=\"_blank\">" + clean_name(file.title()) + "</td><td>" + time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(
            file.replace('.html', '.txt')))) + "</td><td>" + time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(file.replace('.html', '.txt')))) + "</td><td>" + file[1] + "</td></tr>\n")
    # index footer
    temp = '''
		</table>
		<script type="text/javascript" src="sorttable.js"></script>
	</body>
</html>
		'''

    f.write(temp)
    f.close()

if __name__ == '__main__':
    main()
