# První program v Qt Quick

## Základní principy Qt Quick
Grafické aplikace v Qt Quick sestávají ze dvou částí - grafického rozhraní v QML
a výkonného (od slova vykonávat, nikoli výkon) kódu, který dodává grafickému
rozhraní data k zobrazení. Tento kód je v původním Qt v jazyce C++, ale my
budeme používat novější vazby do Pythonu pomocí PySide6, tudíž budeme psát v
Pythonu. Pro Qt verze 5 se knihovna jmenovala PySide2, pro aktuální Qt 6 se
přejmenovala na PySide6. Rozdily mezi PySide2 a PySide6 nejsou příliš významné,
pokud narazíte na návod pro PySide2, pravděpodobně bude fungovat i pro PySide6.
Poslední dobou se možnosti grafického rozhraní rozšiřují a je možné psát i
aplikace pouze v QML (uvnitř QML lze používat JavaScript). Data mezi Pythonem a
QML se předávají pomocí *context property*, o nich bude více v dalších dílech.

## Smyčka událostí (event loop)
Narozdíl od běžných programů v Pythonu, které pracují "shora dolů" jsou aplikace
s grafickým rozhraním (a často i serverové aplikace) založeny na principu smyčky
událostí. Program po spuštění provede inicializační část, kde vytvoří grafické
rozhraní a připraví objekty. Následně přejde do smyčky událostí, ve které čeká
na události od grafického rozhraní (kliknutí, psaní textu, změna velikosti okna)
a na tyto události reaguje. Některé události jsou obslouženy rovnou v grafickém
rozhraní, jiné propadnou do Pythonu a jsou odbaveny tam. Po odbavení události
program čeká ve smyčce na další událost.

## Popis programu
Na začátku vytvoříme [`QGuiApplication`](https://doc.qt.io/qtforpython/PySide6/QtGui/QGuiApplication.html), která zajišťuje, že se naše aplikace
bude chovat jako aplikace s grafickým rozhraním (bude mít okno apod.). 

Následně připravujeme grafické rozhraní - vytvoříme [`QQuickView`](https://doc.qt.io/qtforpython/PySide6/QtQuick/QQuickView.html) a řekneme mu,
ze kterého souboru má vzít popis grafického rozhraní. [`QUrl`](https://doc.qt.io/qtforpython/PySide6/QtCore/QUrl.html) slouží pro převod
cesty na `QUrl` objekt, definiční soubor rozhraní může být umístěn i někde
vzdáleně a aplikace si ho může odtud stáhnout, ale nebývá to příliš časté.
Nakonec nesmíme zapomenout view zobrazit, jinak se nám otevře prázdné okno. 

Když máme vše připraveno, spustíme pomocí `app.exec_()` smyčku událostí. Tato
metoda nevrátí, dokud aplikaci neukončíme nebo nezavřeme okno. Za volání této
funkce tedy nemá smysl psát další kód, protože by se vykonal až těsně před
ukončením aplikace.

## Popis grafického rozhraní
Jazyk [QML](https://doc.qt.io/qt-5/qmlfirststeps.html) je trochu podobný
JavaScriptu a CSS, ale má zjednodušenou syntaxi a jeho základem je hierarchická
struktura (nejen) grafických prvků. Každý prvek má jméno, začínající velkým
písmenem, a blok ohraničený složenými závorkami, ve kterém jsou specifikovány
vlastnosti prvku a deklarovány podřízené prvky. 

Prvky jsou definovány v knihovnách, ty je potřeba na začátku importovat pomocí
`import <Knihovna> <verze>`, kde `<Knihovna>` je název knihovny, lze zjistit
rozkliknutím prvku ze [seznamu QML typů](https://doc.qt.io/qt-5/qmltypes.html),
`<verze>` je specifikována tamtéž. Verze obvykle odpovídá verzi Qt, pokud
použijete, například zkopírováním ze starších ukázek, nižší verzi, nemělo by to
vadit, naopak novější verze vám se starším Qt fungovat nebude, protože prvku
mohly přibýt nové vlastnosti a metody.

V našem příkladu vyrobíme
[obdélník](https://doc.qt.io/qt-5/qml-qtquick-rectangle.html) s rozměry 200x200
px a v něm umístíme prvek [`Text`](https://doc.qt.io/qt-5/qml-qtquick-text.html) s textem *Hello world!*.

## Zdroje
 - [Your First QtQuick/QML Application](https://doc.qt.io/qtforpython/tutorials/basictutorial/qml.html)
 - [Jazyk QML a PySide2](https://www.root.cz/clanky/jazyk-qml-qt-modeling-language-a-pyside-2/)
 - [Jazyk QML a PySide](https://www.root.cz/clanky/jazyk-qml-qt-modeling-language-a-pyside/) - pozor, vztahuje se ke starší verzi PySide i QtQuick. Na QtQuick se skoro nic nezměnilo, PySide a PySide2 se ale liší výrazně
 - [Making a QML Application in Python (video)](https://www.youtube.com/watch?v=JxfiUx60Mbg)
