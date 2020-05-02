# Mapa měst

V tomto díle přidáme k seznamu měst z minulého dílu jejich mapu a zobrazení dalších informací o aktuálně zvoleném městu. Navíc při zvolení města v seznamu se mapa automaticky posune tak, aby zvolené město bylo uprostřed.

## Enum
Pokud potřebujeme vyjádřit nějaký výčet, obvykle číselných, hodnot, kde každá hodnota má nějaký význam, je vhodné si hodnoty pojmenovat. Pro pojmenovávání výčtů je v Pythonu k dispozici třída [`Enum`](https://docs.python.org/3/library/enum.html), která umožňuje snadno jednotlivé hodnoty výčtu pojmenovat a použít.

Enum vytvoříme snadno tak, že vytvoříme třídu, která dědí od [`Enum`](https://docs.python.org/3/library/enum.html). Jako atributy třídy (tedy přímo ve třídě, nikoli v inicializátoru) pak popíšeme jednotlivé prvky výčtu a přiřadíme k nim číselné hodnoty. Jednotlivé prvky výčtu je vhodné pojmenovávat velkými písmeny.

Příklad:

	from enum import Enum

	class Roles(Enum):
		LOCATION = QtCore.Qt.UserRole+0
		AREA = QtCore.Qt.UserRole+1
		POPULATION = QtCore.Qt.UserRole+2

K prvkům takto vytvořeného enumu můžeme přistupovat pomocí jména, například `Roles.LOCATION`, pokud chceme získat číselnou hodnotu, použijeme atribut `.value`, například `Roles.AREA.value`.  

Pokud nám na přesných číselných hodnotách nezáleží, můžeme použít místo číselné hodnoty funkci [`auto()`](https://docs.python.org/3/library/enum.html#enum.auto) z modulu `Enum` a ta čísla přiřadí automaticky.

Příklad:

	from enum import Enum, auto

	class Fruit(Enum):
		APPLE = auto()
		PEAR = auto()
		GRAPEFRUIT = auto()


## Role
Jak jsme si již [v minulém díle](../04_city_list/README.md) ukázali, k jednotlivým vlastnostem prvků v seznamu přistupujeme pomocí rolí. Zatím jsme si ukazovali pouze výchozí [`Qt.DisplayRole`](https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html#PySide2.QtCore.PySide2.QtCore.Qt.ItemDataRole), ale nyní budeme chtít kromě jména města umět získat i počet obyvatel, rozlohu a pro umístění v mapě i souřadnice. Pro každou tuto informaci si tedy vytvoříme vlastní roli.

Qt podporuje uživatelsky vytvářené role. Aby nedocházelo ke kolizi rolí definovaných v Qt a uživatelských rolí, je existuje konstanta `Qt.UserRole`, která nám říká, od kterého čísla máme začít vytvářené role číslovat. Protože budeme vytvářet rolí více, vytvoříme si pro naše role enum. Tento enum můžeme vytvořit přímo uvnitř třídy `CityListModel`, protože jen uvnitř této třídy pro nás mají hodnoty význam.

Abychom mohli přistupovat k nově vytvořeným rolím, musíme dát všem, kteří naši třídu používají, najevo, že naše třída tyto role podporuje. Ke zjištění, jaké role jsou pro danou třídu dostupné slouží metoda [`roleNames`](https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractItemModel.html#PySide2.QtCore.PySide2.QtCore.QAbstractItemModel.roleNames). Tato metoda vrací slovník, jehož klíči jsou čísla rolí a hodnotami pojmenování rolí, tedy to, jak budeme k rolím přistupovat z QML. Pokud metodu nepředefinujeme, pak se předávají [výchozí role](https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractItemModel.html#PySide2.QtCore.PySide2.QtCore.QAbstractItemModel.roleNames). My k nim chceme přidat i role vlastní, proto nejprve získáme slovík rolí od předka a následně k němu přidáme nové klíče pro námi vytvořené role.

Hodnotami nemohou být obyčejné řetězce, ale kvůli vazbám do Qt musí jít o [`QByteArray`](https://doc.qt.io/qtforpython/PySide2/QtCore/QByteArray.html?highlight=qbytearray#PySide2.QtCore.QByteArray). Ten můžeme snadno vytvořit předáním [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) objektu pri vytváření [`QByteArray`](https://doc.qt.io/qtforpython/PySide2/QtCore/QByteArray.html?highlight=qbytearray#PySide2.QtCore.QByteArray). [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) objekt vytvoříme jako normální řetězec, akorát před první uvozovky předřadíme `b`, tedy například `b'location'`. Takovýto objekt pak není řetězcem, ale dokud v něm používáme jen základní znaky (pro nás převážně písmena anglické abecedy a čísla), chovají se tyto objekty obdobně. V našem případě s ním nepotřebujeme nijak pracovat, stačí nám ho jen vytvořit a předat ho do `QByteArray`, tedy například `QByteArray(b'location')`.

Pokud máme metodu `roleNames()` takto předefinovanou, můžeme kdekoli, kde pracujeme s rolemi našeho modelu, používat i nově přidané role.

## Souřadnice
Pro práci se zeměpisnými souřadnicemi se v Qt používá třída [`QGeoCoordinate`](https://doc.qt.io/qtforpython/PySide2/QtPositioning/QGeoCoordinate.html). Tato třída umožňuje uchovávat jak 2D, tak 3D souřadnice, souřadnice musí být v systému WGS84. Třída má i metody na výpočet vzdálenosti nebo azimutu mezi dvěma body. Při vytváření [`QGeoCoordinate`](https://doc.qt.io/qtforpython/PySide2/QtPositioning/QGeoCoordinate.html) se jako první parametr zadává zeměpisná šířka, jako druhý zeměpisná délka a jako třetí volitelný nadmořská výška.

## Popis programu
Program zobrazuje seznam všech měst v ČR a při zvolení nějakého města ze seznamu program ukáže v prostředním sloupci jeho index (pořadí v seznamu), rozlohu a počet obyvatel a zároveň vystředí mapu v pravé části tak, aby bylo zvolené město uprostřed.

Třída `CityListModel` slouží jako model pro seznam i mapu a jsou z ní získávány i rozšiřující informace o městech.

## Popis grafického rozhraní
Rozhraní je rozděleno do tří sloupců. V prvním je seznam měst, ve druhém rozšiřující informace o zvoleném městě a ve třetím sloupci je zobrazená mapa s městy (reprezentovány svými popisky).

Protože na mnoha místech potřebujeme pracovat s aktuálně zvolenou položkou ze seznamu, bylo by nepraktické ve všech místech, kde s ní potřebujeme pracovat, ji získávat ze seznamu. Také by to nebylo vhodné z pohledu rozšiřitelnosti, například pokud bychom umožnili výběr města i kliknutím do mapy, tak bychom museli celý systém navázání složitě upravovat. Proto si [vytvoříme novou property](https://doc.qt.io/qt-5/qtqml-syntax-objectattributes.html#property-attributes) `currentModelItem`, ve které budeme uchovávat aktuálně zvolené město ze seznamu. Přesněji model aktuálně zvoleného města, kterého se můžeme ptát na všechny role, které jsme si předtím v Pythonu deklarovali. Tato property je viditelná z celého QML a použijeme ji všude tam, kde chceme zobrazovat informace o aktuálně vybraném prvku. Pokud bychom v budoucnu umožnili vybrat město jiným způsobem, bude stačit jen nastavit tuto proměnnou a vše ostatní bude fungovat stejně bez potřeby zásahu.

Pro zobrazení seznamu používáme [`ListView`](https://doc.qt.io/qtforpython/PySide2/QtPositioning/QGeoCoordinate.html) jako minule, [*delegát*](https://doc.qt.io/qtforpython/PySide2/QtPositioning/QGeoCoordinate.html) a [`highlight`](https://doc.qt.io/qtforpython/PySide2/QtPositioning/QGeoCoordinate.html) zůstaly nezměněny. Místo přímého použití property `cityListModel` jako modelu je nyní použit [`DelegateModel`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodel.html), který nám umožní relativně snadno získat zvolenou položku. [`DelegateModel`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodel.html) má vlastnost [`model`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodel.html), která udává, z jakého modelu bude brát data, v našem případě to bude `cityListModel` a vlastnost [`delegate`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodel.html), kam přiřadíme (nezměněného) delegáta z minule. Když je delegát nastavený u `DelegateModel`, již se u `ListView` nenastavuje. Dále je potřeba při změně vybraného města v seznamu nastavit property `currentModelItem`.

Získání modelu aktuálně zvoleného prvku není úplně přímočaré, protože narážíme na univerzálnost jednotlivých komponent. Nejprve musíme získat [`DelegateModelGroup`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodelgroup.html) se všemi prvky z [`DelegateModel`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodel.html)u, což uděláme pomocí vlastnosti [`items`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodel.html). Následně můžeme získat pomocí [`.get(<index>)`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodelgroup.html#get-method) objekt reprezentující prvek modelu na daném indexu. Index zjistíme stejně jako v minulém případě pomocí vlastnosti [`currentIndex`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodelgroup.html#get-method). Ze získaného objektu ale ještě potřebujeme vlastnost [`model`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodelgroup.html#get-method), abychom získali model zvoleného prvku a mohli se ptát na jeho jednotlivé role. Výše zmíněné kroky můžeme zapsat za sebe do řádku a získáme výsledný tvar `cityListDelegateModel.items.get(cityList.currentIndex).model`.

Sloupec s rozšířenými informacemi o vybraném městě tvoří sloupec s několika komponentami [`Text`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodelgroup.html#get-method), ve kterých se z `currentModelItem` pomocí rolí získává rozloha a počet obyvatel. Abychom mohli uvádět km<sup>2</sup> s horním indexem, musíme u komponenty, která je zobrazuje, nastavit vlastnost [`textFormat`](https://doc.qt.io/qt-5/qml-qtqml-models-delegatemodelgroup.html#get-method) na `Text.RichText` a následně můžeme použít HTML značku [`<sup>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/sup) a [`</sup>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/sup) k ohraničení horního indexu.

Poslední sloupec obsahuje mapu. Pro práci s mapou a se souřadnicemi, musíme nejprve importovat [`QtLocation`](https://doc.qt.io/qt-5/qtlocation-index.html) a [`QtPositioning`](https://doc.qt.io/qt-5/qtpositioning-index.html). Mapu v QML reprezentujeme pomocí komponenty [`Map`](https://doc.qt.io/qt-5/qtpositioning-index.html), která ale tvoří jen skořápku zajišťující interakci mezi zobrazovanou mapou, dalšími mapovými prvky a uživatelem.

K zobrazení podkladní mapy v komponentě [`Map`](https://doc.qt.io/qt-5/qtpositioning-index.html) je třeba vytvořit komponentu [`Plugin`](https://doc.qt.io/qt-5/qtpositioning-index.html), ve které nastavíme, jakého typu mapa je a případné další parametry. V našem případě chceme zobrazit mapové dlaždice z projektu [OpenStreetMap](https://osm.org) a to ve variantě bez popisků, aby se naše popisky měst nepletly s popisky na mapě. Takové dlaždice poskytuje například [Wikimedia cloud services](wmflab.org). Plugin nám pomocí vlastnosti [`name`](https://doc.qt.io/qt-5/qml-qtlocation-plugin.html#name-prop) umožňuje vybrat z několika poskytovatelů dlaždic, my zvolíme `osm`, protože chceme zobrazovat data projektu OpenStreetMap. Tím vybereme [Qt Location Open Street Map Plugin](https://doc.qt.io/qt-5/location-plugin-osm.html), ve kterém můžeme pomocí komponent [`PluginParameter`](https://doc.qt.io/qt-5/qml-qtlocation-pluginparameter.html) upravovat jednotlivá nastavení. My si pomocí parametru [`osm.mapping.custom.host`](https://doc.qt.io/qt-5/qml-qtlocation-plugin.html#name-prop) zvolíme vlastního poskytovatele dlaždic.

V komponentě [`Map`](https://doc.qt.io/qt-5/qml-qtlocation-map.html) nastavíme plugin pomocí vlastnosti [`plugin`](https://doc.qt.io/qt-5/qml-qtlocation-map.html) a aby byla zobrazena mapa od poskytovatele, kterého jsme nastavili v pluginu, musíme nastavit vlastnost [`activeMapType`](https://doc.qt.io/qt-5/qml-qtlocation-map.html#activeMapType-prop) [dle dokumentace](https://doc.qt.io/qt-5/qml-qtlocation-map.html#activeMapType-prop) na `supportedMapTypes[supportedMapTypes.length - 1]`. Tímto máme nastavenou podkladní mapu.

Abychom na mapě mohli zobrazovat názvy měst z našeho modelu, musíme do mapy přidat komponentu [`MapItemView`](https://doc.qt.io/qt-5/qml-qtlocation-map.html#activeMapType-prop). Obdobně jako [`ListView`](https://doc.qt.io/qt-5/qml-qtquick-listview.html) nastavíme [`MapItemView`](https://doc.qt.io/qt-5/qml-qtlocation-mapitemview.html) dvě vlastnosti - [`model`](https://doc.qt.io/qt-5/qml-qtlocation-mapitemview.html#model-prop), ze kterého máme brát data a [`delegate`](https://doc.qt.io/qt-5/qml-qtlocation-mapitemview.html#delegate-prop), ve kterém určíme, jak mají data vypadat. Komponenta delegáta musí obsahovat právě jednu komponentu dědící od `MapItem`, což v našem případě je [`MapQuickItem`](https://doc.qt.io/qt-5/qml-qtlocation-mapquickitem.html).

[`MapQuickItem`](https://doc.qt.io/qt-5/qml-qtlocation-mapquickitem.html) má několik vlastností, které je vhodné nastavit:
 - [`coordinate`](https://doc.qt.io/qt-5/qml-qtlocation-mapquickitem.html#coordinate-prop) - souřadnice, na kterých se má zobrazovaná komponenta zobrazit
 - [`sourceItem`](https://doc.qt.io/qt-5/qml-qtlocation-mapquickitem.html#sourceItem-prop) - zobrazovaná komponenta - QML komponenta, která se má zobrazit
 - [`anchorPoint`](https://doc.qt.io/qt-5/qml-qtlocation-mapquickitem.html#anchorPoint-prop) - který bod ze zobrazované komponenty má být ten, který se zobrazí na zadaných souřadnicích. Udává se v pixelech, ve výchozím stavu se na zadaných souřadnicích zobrazí levý horní roh zobrazované komponenty

V našem případě je zobrazovaná komponenta jednoduchá komponenta [`Text`](https://doc.qt.io/qt-5/qml-qtquick-text.html), která obsahuje jméno daného města a je umístěna na souřadnice daného města.

Nyní máme podkladní mapu, popisky s názvy měst a zbývá jen nastavit, jak má být mapa přiblížená a jak má být vystředěná. Přiblížení zvolíme pomocí atributu [`zoomLevel`](https://doc.qt.io/qt-5/qml-qtlocation-map.html#zoomLevel-prop) a střed mapy určený vlastnotí [`center`](https://doc.qt.io/qt-5/qml-qtlocation-map.html#center-prop) svážeme se souřadnicemi vybraného města ze seznamu, čímž zajistíme, aby se mapa při změně vybraného města automaticky vystředila na toto město. Samozřejmě dále můžeme mapou přibližovat, oddalovat a posouvat, ale když dojde ke změně vybraného města, mapa se automaticky vystředí na toto město.


## Zdroje
- [Item roles](https://doc.qt.io/qt-5/model-view-programming.html#item-roles) - vybraná kapitola z Model/View programming, více viz minulý díl
- [QML Object Attributes - Property Attributes](https://doc.qt.io/qt-5/qtqml-syntax-objectattributes.html#property-attributes) - popisuje možnosti vytváření a používání property v QML
- [How to access ListView's current item from qml](https://stackoverflow.com/questions/16389831/how-to-access-listviews-current-item-from-qml) - trik s využitím `DelegateModel`
- [Qt Location](https://doc.qt.io/qt-5/qtlocation-index.html) - souhrn možností knihovny Qt Location
- [Map QML Type](https://doc.qt.io/qt-5/qml-qtlocation-map.html)
