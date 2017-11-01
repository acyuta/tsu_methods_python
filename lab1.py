#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################
#
#  @author Akim Glushkov
#  @group 1453
#
# Необходимо написать скрипт, выполняющий рекурсивный обход сайта
# (для тестов используйте mosigra.ru и www.csd.tsu.ru)
# и вывести без дубликатов все адреса электронной почты
# содержащиеся на страницах.
#
# Для ускорения работы - добавьте ограничитель на переходы(напр. 10)
# по ссылкам - сайт может содержать очень много страниц.
#
# Для извлечения email и url следует использовать регулярные выражения.
#
# Базовый язык - Python 2.7 или Python 3.5.
# Требуется использовать библиотеки requests для http запросов и re для RegEx.
#
# Задание на языке python требуется сдать до 23:59 (UTC+7) 1 Ноября.
############################################################################

import requests
import re
import random


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


def parseEmails(page):
    return re.findall(r'[\w\.-]+@[\w\.-]+', page.text)


def parseUrls(page, parentUrl):
    text = page.text
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    hrefs = re.findall(r'(?<=<a href=")[^"]*', text)
    filtered = [parentUrl + a[1:len(a) - 1] for a in hrefs if a.startswith("/")]
    urls += filtered
    return urls


def findAvailableUrls(urls, visits):
    return diff(urls, visits)


def collectUrlsReq(url, depth, visits):
    print("Requesting page: ", url)
    visits.append(url)
    try:
        page = requests.get(url)
    except Exception:
        return [], False

    urls = parseUrls(page, url)
    emails = []
    emails += parseEmails(page)
    if (depth >= 0):
        availableUrls = findAvailableUrls(urls, visits)
        if (len(availableUrls) == 0):
            return emails, False
        else:
            status = False
            c = 0
            while status == False & c < len(availableUrls):
                ems, status = collectUrlsReq(random.choice(urls), depth - (c + 1), visits)
                c += 1
                emails += ems
            return emails, True
    else:
        return emails, True


if __name__ == '__main__':
    maxDepth = 10
    url = "http://www.csd.tsu.ru/"
    emails, status = collectUrlsReq(url, maxDepth, [])
    myemailset = set(emails)
    print(myemailset)
