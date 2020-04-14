# Seznam měst

## Model-View-Delegate
V tomto díle si na jednoduchém seznamu měst v ČR ukážeme použití celého konceptu Model-View-Delegate. Nejprve si tento princip obecně popíšeme, pak se pustíme do detailů jednotlivých částí a předávání dat mezi nimi. Našim cílem je zobrazit seznam všech měst ve sloupci pod sebou.

*Model* v Pythonu bude poskytovat seznam měst. V QML pak bude [ListView](https://doc.qt.io/qt-5/qml-qtquick-listview.html), který tento seznam zobrazí. ListView umí prvky zobrazit pod sebou (nebo vedle sebe, nastavíme-li to), ale to, jakou grafickou reprezentaci mají mít jednotlivé prvky, to musí určit *delegát*. Delegát je zavolán pro každý prvek zvlášť a pro každý prvek vytvoří komponentu, která se pak zobrazí v seznamu. Toto rozdělení nám umožní využívat `ListView` různými kreativními způsoby. Jednotlivé prvky mohou být například obrázky, tlačítka nebo třeba jen barevné obdélníky s parametry závislými na modelu.

## Rozhraní a abstraktní třídy
Aby bylo zobrazování seznamů dostatečně univerzální, musí podporovat mnoho různých operací - přidat prvky do seznamu, změnit hodnotu prvku, odebrat prvky, a mnoho dalších. Všechny tyto operace musí být synchronizované mezi grafickým rozhraním a modelem. V obecnějším případě často máme nějakou sadu operací, kterou musí náš kód splňovat, aby se dal použít k nějaké činnosti. Této sadě říkáme *[rozhraní](https://cs.wikipedia.org/wiki/Interface_(programov%C3%A1_konstrukce)) (interface)*. V našem případě nám `ListView` dá seznam funkcí (slotů), které musíme v našem modelu implementovat, abychom mohli náš model použít jako model pro `ListView`.

Poznámka autora: Všimněme si, že tentokrát bude QML s modelem interagovat výhradně pomocí *slotů* a *signálů* a nikoli pomocí *property*. V našem modelu totiž nemusíme mít data, která chceme zobrazovat, ve formě seznamu, dokonce je nemusíme mít vůbec (například když je požadován nějaký prvek seznamu, tak ho jen vytáhneme z databáze a předáme do rozhraní a v Pythonu ho vůbec nedržíme).

Abychom tyto operace nemuseli implementovat od nuly, máme na to připravené *abstraktní třídy*. Abstraktní třídu si můžeme představit jako nedokončenou třídu určenou k tomu, abychom si ji dokončili podle naší potřeby a ona nám pomohla implementovat nějaké rozhraní. Takováto třída má obvykle implmentovány takové metody, k jejichž implementaci jí stačí výsledky jiných jejích metod (včetně těch, co musíme implementovat my). Nemusíme se proto při implementaci těmito metodami zabývat, ale pokud bychom chtěli, můžeme je samozřejmě přetížit.

Ukažme si příklad jednoduchého rozhraní a abstraktní třídy. Mějme rozhraní sloužící k přístupu k seznamu. Toto rozhraní vyžaduje následující metody:
  - `count(self)` - vrátí počet prvků v seznamu
  - `get(self,i)` - vrátí `i`-tý prvek
  - `first(self)` - vrátí první prvek
  - `last(self)` - vrátí poslední prvek

Když se nad těmito metodami zamyslíme, tak pokud máme implementované metody `count` a `get`, tak umíme přímočaře implementovat metody `first` a `last`. Aby se nemusel každý, kdo chce implemetovat toto rozhraní, obtěžovat se psaním triviálních metod `first` a `last`, připravíme uživatelům abstraktní třídu `AbstractList`:

	from abc import ABC, abstractmethod
	import typing

	class AbstractList(ABC):

		@abstractmethod
		def count(self) -> int:
			"""returns nomber of items in the list"""
			pass

		@abstractmethod
		def get(self,i:int) -> typing.Any:
			"""returns i-th element of the list"""
			pass

		def first(self) -> typing.Any:
			"""returns first element of the list"""
			return self.get(0)

		def last(self) -> typing.Any:
			"""returns last element of the list"""
			return self.get(self.count()-1)

Pokud nyní někdo chce implementovat výše uvedené rozhraní, stačí mu podědit naši třídu `AbstractList` a implementovat její abstraktní metody, tedy `count` a `get`, tedy například takto:

	class ListClass(AbstractList):

		def __init__(self,list):
			self.list = list

		def count(self):
			return len(self.list)

		def get(self,i):
			return self.list[i]

Nyní se vrátíme zpět k našemu původnímu příkladu. Z [dokumentace](https://doc.qt.io/qt-5/qml-qtquick-listview.html#model-prop) zjistíme, že náš model musí dědit (být podtřídou) třídy [`QAbstractItemModel`](https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractItemModel.html). Nebudeme se ale hned hnát do implementací abstraktních metod této třídy, ale přečteme si [podrobný popis](https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractItemModel.html#detailed-description), kde se dočteme, že pro `ListView` máme zvážit použití [`QAbstractListModel`](https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractItemModel.html#detailed-description), který pro našim potřebám vyhovuje více, proto jej použijeme. Zde nyní náš model opustíme a vrátíme se k němu v kapitole Model, až si vysvětlíme další věci potřebné k jeho implementaci.

## Delegát
Delegát je další důležitou součástí skládačky. Delegát "dostane" položku a "vrátí" komponentu, která se následně vloží do `ListView`. Pojem "dostane" a "vrátí" je v uvozovkách, protože nejde o funkci, ale o nějakou komponentu v QML. Tato komponenta může uvnitř využívat property `model`, která drží aktuální prvek a tak, jak bude komponenta vypadat po "dosazení" aktuální položky za všechna použití property `model`, bude vložena do `ListView`. Nejlepší způsob, jak si popsat chování delegáta se všemi souvislostmi je představit si, že v místě, kde je uvedeno `delegate:` vložíme komponentu, která je delegátem tolikrát, kolikrát je v modelu a za property `model` v každé vložené komponentě dosadíme odpovídající prvek modelu.

## Role
Od property `model` v delegátovi bychom mohli očekávat, že se bude chovat jako objekt ze seznamu a budeme tedy moci odkazovat na jeho property. Bohužel tomu tak není, protože by to vyžadovalo, aby jednotlivé prvky seznamu dědily od `QObject`, aby mohly být vůbec z QML dostupné. Tento požadavek by ale byl příliš silný a řadu věcí by znesnadňoval, proto se k vlastnostem prvků seznamu přistupuje pomocí rolí. Pomocí [rolí](https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html#PySide2.QtCore.PySide2.QtCore.Qt.ItemDataRole) říkáme, o jakou vlastnost objektu máme zájem. Model se následně dozví, o jakou roli kterého prvku máme zájem a podle toho nám vrátí patřičná data.

Máme k dispozici několik [předdefinovaných rolí](https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html#PySide2.QtCore.PySide2.QtCore.Qt.ItemDataRole), můžeme si ale snadno vytvořit role vlastní. Vlastními rolemi se budeme zabývat v příštím díle, v tomto si vystačíme s předdefinovanými a to konkrétně s tou nejčastěji používanou, `Qt.DisplayRole`. Tuto roli můžeme v QML použít pomocí `model.display`. Pokud nám v našem případě model vrací jako `Qt.DisplayRole` jméno města, delegát zobrazující jednoduchý text může vypadat například takto:

	delegate: Text {
		text: model.display
	}

## Model
Nyní již víme, co jsou to role a můžeme implementovat naši třídu `CityListModel` dědící od `QAbstractListModel`. Z [dokumentace k dědění](https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractListModel.html#subclassing) z `QAbstractListModel` zjistíme, že potřebujeme implementovat alespoň metody [`rowCount`](https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractItemModel.html#PySide2.QtCore.PySide2.QtCore.QAbstractItemModel.rowCount) a [`data`](https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractItemModel.html#PySide2.QtCore.PySide2.QtCore.QAbstractItemModel.data).

Metoda [`rowCount(self,parent=QModelIndex()) -> int`](https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractItemModel.html#PySide2.QtCore.PySide2.QtCore.QAbstractItemModel.rowCount) vrací počet řádek našeho modelu, její implementace je tedy přímočará.

Metoda [`data(self, index: QModelIndex, role=Qt.DisplayRole) -> typing.Any`](https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractItemModel.html#PySide2.QtCore.PySide2.QtCore.QAbstractItemModel.data) je složitější. Bere dva argumenty - `index`, ze kterého zjistíme, který prvek je požadován a `role`, která nám určuje, jakou roli daného prvku máme vrátit. `index` je typu [`QModelIndex`](https://doc.qt.io/qtforpython/PySide2/QtCore/QModelIndex.html), který umožňuje mít složitější strukturu dat než obyčejný seznam, nám ale z něj budou stačit jen dvě metody - [`isValid()`](https://doc.qt.io/qtforpython/PySide2/QtCore/QModelIndex.html#PySide2.QtCore.PySide2.QtCore.QModelIndex.isValid), která nám vrátí `True`, pokud jde o platný index a [`row()`](https://doc.qt.io/qtforpython/PySide2/QtCore/QModelIndex.html#PySide2.QtCore.PySide2.QtCore.QModelIndex.row), která nám řekne, kolikátý prvek máme vrátit. `role` je pak jednou z [rolí](https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html#PySide2.QtCore.PySide2.QtCore.Qt.ItemDataRole), v našem případě si vystačíme s `Qt.DisplayRole` a ostatní budeme zatím ignorovat.

Implementujeme-li tyto dvě metody, můžeme naši třídu `CityListModel` použít jako model pro libovolné `ListView` v QML.

## Popis programu
Program zobrazuje seznam všech měst v ČR. Program obsahuje jedno `ListView`, ve kterém jsou města zobrazena a pokud zvolíme pomocí proměnné `VIEW_URL` bohatši rozhraní `view.qml`, můžeme jednotlivá města označovat pomocí klávesnice nebo myši program do konzole vypíše, kolikáté město jsme zvolili. Třída `CityListModel` dědící od `QAbstractListModel` zajišťuje model pro `ListView`.

Samotný seznam měst pochází z projektu [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page), dotaz ve [SPARQL](https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/Wikidata_Query_Help) si můžete [prohlédnout](city_list/wikidata_cities.sparql). Dotazovací jazyk není příliš přívětivý, pokud byste chtěli něco získat z Wikidat, doporučuji si v příkladech najít podobný dotaz a upravit ho, než se snažit psát dotaz od začátku.


## Popis grafického rozhraní


## Zdroje
- [Model/View Programming](https://doc.qt.io/qtforpython/overviews/model-view-programming.html) - popis principu, přibližně odpovídá tomuto a příštímu dílu
  - doporučuji od začátku po sekci [Models](https://doc.qt.io/qtforpython/overviews/model-view-programming.html#models) včetně
  - od sekce [Model Classes](https://doc.qt.io/qtforpython/overviews/model-view-programming.html#model-classes), po [Using model indexes](https://doc.qt.io/qtforpython/overviews/model-view-programming.html#using-model-indexes) včetně
  - od sekce [Creating ne models](https://doc.qt.io/qtforpython/overviews/model-view-programming.html#creating-new-models) po [Inserting and removing rows](https://doc.qt.io/qtforpython/overviews/model-view-programming.html#inserting-and-removing-rows) včetně
  - od sekce [Item data handling](https://doc.qt.io/qtforpython/overviews/model-view-programming.html#item-data-handling) po [Parents and children](https://doc.qt.io/qtforpython/overviews/model-view-programming.html#parents-and-children) včetně
  - mezi těmito částmi jsou sekce věnované jinému druhu grafickému rozhraní, než je QML, tudíž pro nás nejsou důležité
- [ListView QML Type](https://doc.qt.io/qt-5/qml-qtquick-listview.html)
- [QML Listview selected item highlight on click](https://stackoverflow.com/questions/9400002/qml-listview-selected-item-highlight-on-click)
- [QAbstractListModel Class](https://doc.qt.io/qt-5/qabstractlistmodel.html) - dokumentace k C++ variantě
- [Using C++ Models with Qt Quick Views](https://doc.qt.io/qt-5/qtquick-modelviewsdata-cppmodels.html) - sice pojednává o C++, ale principy jsou platné stejně i pro Python
