import requests
from bs4 import BeautifulSoup, Comment
import codecs
import time
import os


def html_parser():

    # Pull MDDELCC files in parser
    for number in range(1, 18):
        if number < 10:
            url = r'https://geoindex.xyz/files/mddelcc_ri_region0' + str(number) + '.html'
        else:
            url = r'https://geoindex.xyz/files/mddelcc_ri_region' + str(number) + '.html'

        # Build HTML file
        html = requests.get(url).content
        # Make our soup
        soup = BeautifulSoup(html, 'lxml')

        date_string = time.strftime("%Y%m%d")
        f = codecs.open('mddelcc_ri_in_' + date_string + '.txt', 'a+', encoding='utf-8')


        # Remove comments from file
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        [comment.extract() for comment in comments]

        # Start at 5 in order not to pull table headers. Stop at len -2 so we do not pick up the table footer
        for i in range(5, (len(soup('tr')) - 2)):
            td_list = soup('tr')[i]

            tds = td_list.findAll('td')

            for td in tds:
                tdstr = " ".join(str(td.text).replace('\r\n', ' ').split())
                # print(td.text)
                f.write(tdstr + '|')
            f.writelines("\n")


        f.close()
    clean_file()


def clean_file():

    date_string = time.strftime("%Y%m%d")
    f_in = codecs.open('mddelcc_ri_in_' + date_string + '.txt', 'rb', encoding='utf-8')
    f_out = codecs.open('MDDELCC_RI_' + date_string + '.csv', 'w', encoding='utf-8')

    # Remove white spaces and write to output file
    for line in f_in:
        f_out.write(" ".join(line.split()) + '\n')
    f_in.close()
    os.remove('mddelcc_ri_in_' + date_string + '.txt')

html_parser()
