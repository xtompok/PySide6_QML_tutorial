# PySide2 QML tutorial
Tutorial for using Python with Qt, specially with QtQuick and PySide2 libraries. 

## About (EN)
The text is in czech due to primarily targeting Czech students.
Source code and comments is in english. Feel free to ask me if you can't
understand any part. Translations, comments and contributions are welcomed.

## O tomto návodu
Tutoriál pro používání Qt Quick v Pythonu pomocí PySide2, primárně zaměřen na
studenty a zájemce o geografii. Pomocné texty jsou v češtině, zdrojové kódy a
komentáře v nich jsou anglicky. Pokud by něco nebylo jasné, dejte mi vědět.
Pokud byste chtěli pomocné texty přeložit do angličtiny nebo měli jiné náměty či
připomínky, jsou vítány. Tento tutoriál vzniká převážně proto, že jsem nenašel
jiný (anglický / český), který pokrývá používání Qt Quick a Pythonu více než
povrchně. Pokud o nějakém takovém víte, dejte mi prosím vědět.

Aby kód zbytečně nebobtnal, jsou nové věci komentovány vždy v tom díle, kde jsou
představeny. V dalších dílech jsou již komentovány jen stručně, pokud vám není
něco jasné, zkuste se podívat do předchozích dílů.

Uživatelské rozhraní (QML soubor) se obvykle vyskytuje ve dvou variantách -
`view.qml` obsahující jen nezbytně nutné prvky a `view_rich.qml` graficky
propracovanější, ukazující možnosti přizpůsobení grafického rozhraní. Mezi
rozhraními se přepíná ve zdrojovém kódu přepsáním `VIEW_PATH`.

Pokud nějaký pojem nemá český ustálený ekvivalent, budu používat původní
anglické názvy, text tedy může někdy vypadat poněkud krkolomně.

## Doporučený SW
Pro Python doporučuji PyCharm nebo jiný editor s doplňováním syntaxe, pro
editaci QML pak Qt Creator (součástí balíku Qt). QML lze psát i v PyCharmu
(nastavit syntaxi na JavaScript), ale pro pokročilejší úpravy nabízí Qt Creator
i vizuální editor, kde se změny ihned projeví. Pro základní rozhraní není Qt
Creator nutný.

Příklady jsou testovány na Python 3.7 a Python 3.8.2 (pozor, na Windows Python
3.8.0 nefunguje s PySide2, aktualizujte Python). Qt je používáno ve verzi 5.14,
ale pravděpodobně budou, alespoň úvodní příklady fungovat i se staršími verzemi.

## Spouštění příkladů
Nejlépe ve složce příkladu vytvořit virtualenv s PySide2. Příklady budou mít v
budoucnu `requirements.txt`.

## Díly (budou postupně přibývat)
 1. [První program](01_first_program)
 2. [Klikni na tlačítko](02_clicker)
	- binding proměnných
	- reakce na stisk tlačítka
 3. [Převod DMS na stupně a zpět](03_dms_converter)
	- koncept model a view
	- obousměrná synchronizace mezi modelem a GUI
 4. [Seznam měst](04_city_list)
 	- model, view, delegate
	- abstraktní třídy
	- fokus - úvod
 5. [Mapa měst](05_city_map)
 	- Map View
	- property v QML


## Zdroje
 - [Dokumentace ke Qt](https://doc.qt.io/)
 - [Qt for Python](https://doc.qt.io/qtforpython/index.html#)
 - Seriál [Grafické uživatelské rozhraní v Pythonu](https://www.root.cz/serialy/graficke-uzivatelske-rozhrani-v-pythonu/), poslední 3 díly
 - [Seznam QML typů](https://doc.qt.io/qt-5/qmltypes.html)
 - [Seznam modulů v PySide2](https://doc.qt.io/qtforpython/modules.html)

