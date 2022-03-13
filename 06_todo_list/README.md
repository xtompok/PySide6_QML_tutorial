# TODO list

V tomto díle vytvoříme jednoduchý TODO list

## Změna počtu prvků modelu
Dosud jsme pracovali pouze s modely, které měly po celou dobu běhu programu
stejný počet prvků. QML část programu se tedy na začátku dotázala, kolik má
model prvků a pak o ně dle potřeby zobrazení žádala. Nyní budeme chtít mít
možnost, jak počet prvků za běhu programu měnit a to tak, aby se tyto změny
ihned projevovaly i v grafickém rozhraní. 

Z pohledu samotných dat v modelu je to jednoduché. Data držíme v seznamu, je
tedy snadné tento seznam metodou [.append(elem)](https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types) rozšířit, nebo pomocí
metody [.pop(idx)](https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types) některý prvek ze seznamu vyhodit. Pokud ale zkusíme udělat
jen tuto jednoduchou změnu, zjistíme, že sice se model změnil, ale uživatelské
rozhraní stále zobrazuje původní data z modelu. Je tomu tak proto, neboť
[`ListView`](https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types) (nebo jiné view) nedostane žádnou informaci o tom, že se data
modelu změnila a tudíž používá ta, která má již načtená. Pokud tedy chceme měnit
počet prvků modelu, musíme o tom informovat i QML a to si pak načte a správně
zobrazí změněné položky.

### Přidávání prvků
Pokud chceme prvky přidávat, musíme před samotnou změnou modelu zavolat metodu
[`beginInsertRows(index,first,last`)](https://doc.qt.io/qtforpython/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.PySide6.QtCore.QAbstractItemModel.beginInsertRows), která vyšle signál o tom, že se budou
přidávat do modelu řádky a po jejich přidání budou mít první přidaný řádek index
`first` a poslední přidaný řádek index `last`. Tento signál zachytí QML a od
této chvíle ví, že se data v modelu budou měnit. Poté je možné řádky do modelu
přidat a ihned poté je třeba zavolat metodu [`endInsertRows()`](https://doc.qt.io/qtforpython/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.PySide6.QtCore.QAbstractItemModel.endInsertRows), která vyšle
signál o tom, že řádky byly vloženy a modifikace modelu ukončena. Tento signál
také zachytí QML, dotáže se modelu na aktuální počet prvků a načte a zobrazí
přidané prvky. 

Pokud přidáváme jeden prvek, bude `first` a `last` nastavené na stejnou hodnotu,
protože první přidaný prvek je zároveň posledním přidaným prvkem. Pokud chceme
vložit prvky na konec, tak bude mít `first` hodnotu rovnou aktuálnímu počtu
řádků, protože první vložený prvek bude právě na indexu odpovídajícímu
aktuálnímu počtu řádků.

Metody `beginInsertRows` a `endInsertRows` je vhodné volat vždy co nejtěsněji
kolem úprav samotného modelu. Mezi začátkem a koncem vkládání je model
považovaný za měněný a to může mít důsledky na výkon aplikace.

### Odebírání prvků
Odebírání prvků funguje obdobně jako přidávání. Než začneme měnit model, musíme
zavolat metodu [`beginRemoveRows(index, first,last)`](https://doc.qt.io/qtforpython/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.PySide6.QtCore.QAbstractItemModel.beginRemoveRows), která vyšle signál o
tom, že budou z modelu odebrány řádky a to tak, že první odebraný řádek bude
ten, který má aktuálně index `first` a poslední odebraný řádek bude ten, který
má aktuálně index `last`. Následně je možné řádky odebrat v modelu a
bezprostředně po jejich odebrání je potřeba zavolat metodu `endRemoveRows(https://doc.qt.io/qtforpython/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.PySide6.QtCore.QAbstractItemModel.endRemoveRows)`,
která vyšle signál, že modifikace modelu byla ukončena. Oba tyto signály zachytí
QML a zajistí, aby zobrazené prvky po ukončení odebírání odpovídaly modelu. 

Obdobně jako `beginInsertRows` a `endInsertRows` by metody `beginRemoveRows` a
`endRemoveRows` měly být volány co nejtěsněji kolem samotné modifikace modelu.

### Složitější změny modelu
Pokud potřebujeme významnějším způsobem změnit model, lze při snaze o zachování
jednoduchosti použít postup, kdy nejprve všechny prvky z modelu odebereme,
provedeme modifikace a následně všechny prvky po modifikacích přidáme. Tento
postup není vhodný pro větší datové sady a časově náročnější modifikace, protože
prvky nakrátko zmizí z rozhraní a je výpočetně náročné je všechny z rozhraní
odstranit a následně je tam opět přidat. Pro složitější třídění a filtrování je
vhodné použít modely k tomu určené (např.
[`QSortFilterProxyModel`](https://doc.qt.io/qt-6/qsortfilterproxymodel.html),
ale to je již nad rámec tohoto tutoriálu.

## Popis programu
Program zobrazuje seznam úkolů. Tyto úkoly při startu načte ze souboru a
umožňuje pomocí textového pole nové úkoly přidávat a hotové úkoly odstraňovat. 

Modelem aplikace je třída `TaskListModel`, která je velmi podobná třídě
`CityListModel` z [předminulého dílu](04_city_list). Kromě základních metod potřebných pro
správné fungování spolu s QML dále obsahuje tři sloty, které slouží pro
modifikaci seznamu. Všiměte si, že tyto sloty berou argumenty, které pak při
modifikaci využívají. Slot `addTask` dostane jako argument řetězec, který přidá
do seznamu úkolů jako další úkol, slot `deleteTask` dostane jako argument index
úkolu, který má smazat. Tím pádem nepotřebují tyto sloty žádné další vazby na
uživatelské rozhraní, protože rovnou dostanou všechny informace, které ke své
funkci potřebují.

## Popis grafického rozhraní
Program má dvě grafická rozhraní - jednoduché v souboru
[`simple_view.qml`](todo_list/simple_view.qml) a pokročilé ve
[`view.qml`](todo_list/view.qml), které ukazuje uživatelsky přívětivější
variantu práce se seznamem úkolů. 

### Jednodušší rozhraní
Toto rozhraní umožňuje přidávat úkoly zapsáním do textového pole a kliknutím na
"Přidej úkol" a odebrat úkol jeho zvolením v seznamu úkolů a následným kliknutím
na "Odeber zvolený úkol".

Implementace rozhraní je velmi podobná [seznamu měst](/04_city_list). Za
povšimnutí stojí řešení přidávání úkolů, kdy text nově přidávaného úkolu
nezískává Python z [`TextInputu`]() sám, ale řetězec je předán přímo v signálu.
Umožňuje to tak větší flexibilitu v grafickém rozhraní, kdy je možné zadávat
text různými způsoby a stačí pak jen vyslat správný signál k přidání úkolu.
Obdobně rozhraní pro mazání úkolu je pomocí signálu, který obsahuje index úkolu,
který má smazat.

### Pokročilé rozhraní
Toto rozhraní umožňuje přidávat úkoly zapsáním do textového pole a následným
stisknutím Enteru nebo kliknutím na "Přidej úkol". Po přidání úkolu se textové
pole smaže. Odebrání úkolů je možné po jednom kliknutím na úkol nebo na zaškrtávací
políčko vedle něj, dále lze odebrat všechny úkoly naráz pomocí kliknutí na
tlačítko "Odeber všechny úkoly". Seznam úkolů se automaticky zvětšuje tak, aby
vyplnil veškeré dostupné volné místo v okně, textové pole na zadávání nových
úkolů spolu s tlačítky je zarovnáno na dolní stranu okna.

Aby bylo možné snadno adaptovat uživatelské rozhraní při změně velikosti okna,
budeme používat [`ColumnLayout`](https://doc.qt.io/qt-5/qml-qtquick-layouts-columnlayout.html) a [`RowLayout`](https://doc.qt.io/qt-5/qml-qtquick-layouts-rowlayout.html) z modulu
[`QtQuick.Layouts`](https://doc.qt.io/qt-5/qtquicklayouts-index.html). Oproti
jednoduchým komponentám [`Row`](https://doc.qt.io/qt-5/qml-qtquick-row.html) a [`Column`](https://doc.qt.io/qt-5/qml-qtquick-column.html) umí tyto komponenty roztahovat
vložené prvky tak, aby vyplnily okno, zarovnávat je a dělat s nimi i další
pokročilé pozicování. Tyto možnosti se nastavují ve vnořených komponentách
pomocí atributu [`Layout.<atribut>`](https://doc.qt.io/qt-5/qml-qtquick-layouts-layout.html) a vždy se vztahují k nejbližší nadřazené
komponentě typu `Layout`. Speciálně pozor u `RowLayout`u, kde atributy
[`Layout.fillWidth`](https://doc.qt.io/qt-5/qml-qtquick-layouts-layout.html#fillWidth-attached-prop) a [`Layout.alignment`](https://doc.qt.io/qt-5/qml-qtquick-layouts-layout.html#alignment-attached-prop) rovnou v `RowLayout`u se vztahují k
umístění komponenty `RowLayout` v komponentě `ColumnLayout`, nikoli k prvkům
komponenty `RowLayout`. Lidsky řečeno říkají, že se řádková komponenta má
zarovnat dolů a roztáhnout přes celou šířku komponenty `ColumnLayout`. Atribut
[`fillWidth`](https://doc.qt.io/qt-5/qml-qtquick-layouts-layout.html#fillWidth-attached-prop) / [`fillHeight`](https://doc.qt.io/qt-5/qml-qtquick-layouts-layout.html#fillHeight-attached-prop) říká, že má daná komponenta vyplnit celý
zbývající prostor, pomocí atributu `alignment` lze určit, ke které straně /
stranám se má zarovnávat. 

K zobrazení jednotlivých úkolů slouží komponenta [`CheckBox`](https://doc.qt.io/qt-5/qml-qtquick-controls2-checkbox.html), která dělá
zatrhávací políčko s popiskem. Aby bylo možné políčko zaškrtnout, je potřeba
povolit atribut [`checkable`](https://doc.qt.io/qt-5/qml-qtquick-controls2-abstractbutton.html#checkable-prop), ke stavu zaškrtnutí je pak možné přistupovat
pomocí atributu [`checkState`](https://doc.qt.io/qt-5/qml-qtquick-controls2-checkbox.html#checkState-prop), v tomto programu toho ale nevyužíváme. Místo toho
hlídáme signál [`clicked`](https://doc.qt.io/qt-5/qml-qtquick-controls2-abstractbutton.html#clicked-signal) a při jeho vyslání necháme daný úkol smazat.

Aby byl [`TextInput`](https://doc.qt.io/qt-5/qml-qtquick-textinput.html) sloužící k zadávání textu nového úkolu výraznější, je
obalen komponentou [`Rectangle`](https://doc.qt.io/qt-5/qml-qtquick-rectangle.html), která mu zařizuje orámování. Tato komponenta
získá svou šířku z `Layout`u, ale výšku nemá danou, takže je potřeba nějakou
zvolit. Protože hned vedle jsou umístěna tlačítka, byla zvolena výška
orámovávacího obdélníka jako výška jednoho z tlačítek, aby to vizuálně
navazovalo. U samotné vložené komponenty TextInput je potřeba nastavit výšku
podle obklopujícího obdélníka a zmenšit ji o rozměry rámečku. Také se hodí
samotný text vertikálně vystředit, aby navazoval na text na tlačítkách vedle.

[`TextInput`](https://doc.qt.io/qt-5/qml-qtquick-textinput.html) má nastaven atribut [`focus`](https://doc.qt.io/qt-5/qml-qtquick-item.html#focus-prop), aby bylo možné rovnou začít
psát nové úkoly. Dále je využit signál [`accepted`](https://doc.qt.io/qt-5/qml-qtquick-textinput.html#accepted-signal), který je vyvolán při
potvrzení enterem. Při jeho zpracování je využit blok, který umožňuje zadat více
příkazů jako reakci na signál. V tomto případě je přidán nový úkol se zadaným
textem a následně je textové pole smazáno, aby bylo možné psát další úkol.

## Zdroje
  - [QAbstractItemModel](https://doc.qt.io/qtforpython/PySide6/QtCore/QAbstractItemModel.html)
  - [QSortFilterProxyModel](https://doc.qt.io/qt-6/qsortfilterproxymodel.html)
  - [Qt Quick Layouts Overview](https://doc.qt.io/qt-5/qtquicklayouts-overview.html)
