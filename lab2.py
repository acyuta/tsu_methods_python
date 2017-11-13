#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################
#
#  @author Akim Glushkov
#  @group 1453
#
# Необходимо написать скрипт, обрабатывающий лог файл Nginx
# выводящий список IP адресов, с которых производились запросы.
# Адреса из общей подсети \24 необходимо группировать при выводе(напр. 10.40.0.4 и 10.40.0.231 относятся к одной подсети).
#
# Базовый язык - Python 2.7 или Python 3.5. Требуется использовать библиотеку re для RegEx.
#
#  Задание на языке python требуется сдать до 23:59 (UTC+7) 8 Ноября.
############################################################################

import re
import sys
import os.path
import os


def fch(str, ch, posl):
    pos = 0
    for c in str:
        if ch == c:
            if posl == 0:
                return pos
            else:
                posl = posl - 1
        pos = pos + 1

    raise RuntimeError("Не вернули позицию символа подстроки, т.к. дошли до конца строки")


def prepare(ips):
    result = list()
    prefix = None
    for ip in sorted(ips):
        try:
            if prefix is None:
                prefix = ip[0:fch(ip, '.', 2)]
                result.append(ip)
                continue
            elif prefix == ip[0:fch(ip, '.', 2)]:
                del result[-1]
                result.append(prefix + ".0/24")
            else:
                prefix = ip[0:fch(ip, '.', 2)]
                result.append(ip)

        except RuntimeError:
            pass

    return result


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Отсутствуют необходимые параметры (имя файла). Например, \"access.log\"")
        exit(-1)
    arg = sys.argv[1]
    if not os.path.isfile(arg):
        print("Входящий параметр '" + arg + "' не является файлом")
        exit(-1)

    try:
        file = open(arg)
        ips = set()
        c = 0
        for line in file:
            c = c + 1
            ip_str = re.match("([0-9.]*)", line).group(1)
            ips.add(ip_str)

        # print("Считано " + str(len(ips)) + " из " + str(c) + " различный адресов")
        print('\n'.join(prepare(ips)))


    except IOError:
        print("Ошибка чтения файла. '" + arg + "' не доступен для чтения или произошла ошибка при чтении")
        exit(-1)
