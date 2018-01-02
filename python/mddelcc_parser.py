import requests
from bs4 import BeautifulSoup, Comment
import codecs
import time
import os

def log(program, entry):
    program = program
    entry = entry
    command = "python3 logger.py -p %s -e %s" % (program,entry)
    return command

def html_parser():

    
    # Pull MDDELCC files in parser
    for number in range(1, 18):
        if number < 10:
            url = r'https://geoindex.xyz/files/mddelcc_region0' + str(number) + '.html'
        else:
            url = r'https://geoindex.xyz/files/mddelcc_region' + str(number) + '.html'

        # Build HTML file
        os.system(log("\"MDDELCC_PARSER.PY:HTML_PARSER\"", "\"Pulling from " + url + "\""))
        html = requests.get(url).content
        # Make our soup
        os.system(log("\"MDDELCC_PARSER.PY:HTML_PARSER\"", "\"Parsing big html\""))
        soup = BeautifulSoup(html, 'lxml')

        date_string = time.strftime("%Y%m%d")
        os.system(log("\"MDDELCC_PARSER.PY:HTML_PARSER\"", "\"Creating file " + 'mddelcc_in_' + date_string + '.txt' + "\""))
        f = codecs.open('mddelcc_in_' + date_string + '.txt', 'a+', encoding='utf-8')

        # Remove comments from file
        os.system(log("\"MDDELCC_PARSER.PY:HTML_PARSER\"", "\"Removing comments from html file\""))
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        [comment.extract() for comment in comments]

        os.system(log("\"MDDELCC_PARSER.PY:HTML_PARSER\"", "\"Iterating on tr tags - extracting td tags\""))
        # Start at 2 in order not to pull table headers. Stop at len -1 so we do not pick up the table footer
        for i in range(2, (len(soup('tr')) - 1)):
            td_list = soup('tr')[i]
            tds = td_list.findAll('td')
            for td in tds:
                try:
                    if td.text == '':
                        f.write('Aucun' + '|')
                    else:
                        # Remove wacky table data formatting for proper data insertion
                        # Converted td.text to a string as it's easier to manipulate than a BS4 ResultSet
                        tdstr = " ".join(str(td.text).replace('\r\n', ' ').split())
                        tdstr = tdstr.replace('&', 'et')
                        f.write(tdstr + '|')
                except ValueError:
                    f.write('fail' + '|')
            f.writelines("\n")
        f.close()
        os.system(log("\"MDDELCC_PARSER.PY:HTML_PARSER\"", "\"Cleaning file " + 'mddelcc_in_' + date_string + '.txt' + "\""))
    clean_file()


def clean_file():

    date_string = time.strftime("%Y%m%d")
    f_in = codecs.open('mddelcc_in_' + date_string + '.txt', 'rb', encoding='utf-8')
    os.system(log("\"MDDELCC_PARSER.PY:HTML_PARSER:CLEAN_FILE\"", "\"Writing file " + 'mddelcc_in_' + date_string + '.csv' + "\""))
    f_out = codecs.open('MDDELCC_' + date_string + '.csv', 'w', encoding='utf-8')

    # Remove white spaces and write to output file
    for line in f_in:
        f_out.write(" ".join(line.split()) + '\n')
    f_in.close()


# Launch it
html_parser()