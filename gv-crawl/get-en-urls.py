import sys
import os
import re
import sqlite3
import argparse
from collections import namedtuple
from articles import Article, url_pattern

def find_translation_url(article, lang):
    for url in article.translations.split():
        m = url_pattern.match(url)
        if not m: continue
        l = m.group(1)
        l = 'en' if not l else l[:-1]
        l = 'en' if l in ('rising', 'advocacy') else l
        if l == lang:
            return url

def main():
    parser = argparse.ArgumentParser(description='Write articles to disk for alignment')
    parser.add_argument('src_lang', help='source language - original [en]')
    parser.add_argument('trg_lang', help='target language - translated [sw]')
    parser.add_argument('database', help='database path to read articles from')
    args = parser.parse_args()

    conn = sqlite3.connect(args.database)
    trg_cur = conn.cursor()
    src_cur = conn.cursor()

    def article_pairs(trg_lang, src_lang):
        trg_cur.execute('select * from articles where lang = ?', (trg_lang,))
        for article in trg_cur.fetchall():
            trg_article = Article(*article)
            src_url = find_translation_url(trg_article, src_lang)
            yield trg_article, src_url

    found, not_found = 0, 0
    for (trg, src_url) in article_pairs(args.trg_lang, args.src_lang):
      if src_url is not None:
        print src_url
      else:
        not_found += 1

if __name__ == '__main__':
    main()
