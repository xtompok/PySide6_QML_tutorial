# Klikni na tlačítko 

## Context property
Abychom mohli propojit grafické rozhraní a výkonný kód v Pythonu, musíme si
pořídit objekt, ke kterému bude rozumět jak Python, tak QML. Pokud takovýto
objekt už máme, můžeme ho do QML zpřístupnit pomocí *context property*.
`QQuickView` si drží kontext - stav - ke kterému lze přistupovat jak z Pythonu,
tak z QML. My můžeme pomocí
[`setContextProperty`](https://doc.qt.io/qtforpython/PySide6/QtQml/QQmlContext.html#PySide6.QtQml.PySide6.QtQml.QQmlContext.setContextProperty)
do tohoto kontextu přidat náš objekt a určit mu, pod jakým jménem se bude
objevovat v QML. 

Kontext získáme z `QQuickView` pomocí metody `view.rootContext()`. Pokud pak
zavoláme `ctxt.setContextProperty('myObj', my_object)`, pak objekt `my_object`
z Pythonu bude dostupný v QML jako `myObj`. Kde takový objekt vzít?
Nejjednodušší je vytvořit si vlastní třídu, která bude dědit od [`QObject`](https://doc.qt.io/qtforpython/PySide6/QtCore/QObject.html) 
a v ní deklarovat potřebné signály, sloty a property (viz níže). Díky tomu, že
naše třída dědí od QObject, je možné ji použít jako context property a Qt zařídí
potřebné vazby.


## Signály a sloty
Uživatel může vyvolat mnoho různých akcí a na některé akce potřebuje reagovat více
komponent. Přímé volání funkcí by v tomto případě bylo otížně realizovatelné,
proto je ve Qt zaveden mechanismus signálů a slotů.

Pokud dojde k nějaké akci, například je stisknuto tlačítko, je při tom emitován
signál. Pokud chceme na nějaký signál reagovat, musíme si vytvořit slot a
následně připojit signál stisku tlačítka do našeho slotu. Jeden signál může být
připojen do libovolného množství slotů (i do žádného), jeden slot může být
připojen k libovolnému množství signálů. 

Každý signál a slot má definovanou signaturu (seznam argumentů a jejich typů),
kterou je při propojování signálů a slotů potřeba dodržovat. Respektive slot
může brát méně argumentů, než má signál, zbylé argumenty signálu se pak zahodí.
Společné argumenty ale musí mít stejné typy. Toto je důsledek použití C++ jako
výchozího jazyka pro Qt, proto to může v Pythonu působit zvláštně.

Jak vytvořit slot nebo signál? Obojí je potřeba vytvořit v Pythonu jako metodu
objektu, který, alespoň nepřímo, dědí z `QObject`. Signál vytvoříme pomocí
funkce `Signal(<typ1>,<typ2>,...)` a takto vytvořený signál pak můžeme emitovat
pomocí `signal.emit(<arg1>,<arg2>,...)`, kde `<arg1>` a další jsou skutečné
hodnoty dříve deklarovaných typů, které chceme v signálu poslat.

Slot vytvoříme pomocí dekorátoru `@Slot(<typ1>,<typ2>,...)` k metodě objektu.
Tato metoda pak kromě `self` bere daný počet argumentů typů deklarovaných v
dekorátoru. 

Pokud potřebujeme propojit signál a slot přímo v Pythonu, můžeme použít metodu
`connect` v podobě `signal.connect(slot)`.

## Property
Často potřebujeme, aby nám GUI reflektovalo hodnotu nějaké proměnné v Pythonu,
například aby byla zobrazena hodnota počítadla, nebo aby byl nápis *Vyhráli
jste* zobrazen pouze, když je sudoku správně vyplněné. Toto by samozřejmě bylo
realizovatelné i s použitím pouze signálů a slotů, ale bylo by to zbytečně
pracné a náročné na údržbu. Proto byl zaveden koncept *property*, které
takovouto činnost zjendodušují. 

Property je ve zjednodušeném pohledu lepší atribut objektu, který je kromě
Pythonu viditelný i v QML. Opět se zde ukazuje původ v C++, abychom mohli
vytvořit property, musíme deklarovat *getter*, *setter* a notifikační signál.
Budeme tedy postupovat zcela v duchu OOP. Pro další text předpokládejme, že
chceme vytvořit property `counter`. Vytvoříme si privátní atribut
`self._counter`, ve kterém budeme uchovávat skutečnou hodnotu počitadla, ale
nebudeme k ní přistupovat odjinud než z inicializátoru, getteru a setteru.

*Getter* je metoda, která nám vrátí hodnotu interního atributu.
Budeme dodržovat konvenci a gettery pojmenovávat `get_<atribut>`, tedy v našem
případě `get_counter`. Tato funkce pouze vrátí hodnotu `self._counter`.

*Notifikační signál* může, ale nemusí, emitovat změněnou hodnotu.
Jméno je `<atribut>_changed`, tedy dle předchozí kapitoly `counter_changed =
Signal()`. Jedná se také o metodu, i když je deklarovaná jinak, než jsme zvyklí.

*Setter* je o něco složitější, protože v případě, že se hodnota změnila, musíme
emitovat notifikační signál, aby se případně překreslilo GUI. Metoda bude
vypadat například takto:

```
def set_counter(self,val):
    if val != self._counter:
        self._counter = val
	self.counter_changed.emit()

```

Když máme všechny tři metody připravené, můžeme vytvořit
[`Property`](https://doc.qt.io/qtforpython/PySide6/QtCore/Property.html).
`Property` bere 4 argumenty - typ, getter, setter a pojmenovaný argument
`notify` s notifikační metodou. Naší property bychom vytvořili takto:
`counter = Property(int,get_counter,set_counter,notify=counter_changed)`. Nyní
se můžeme k propetry v Pythonu chovat jako k normálnímu atributu, tedy můžeme ho
číst i nastavovat pomocí `self.counter = 42` a gettery a settery se zavolají
automaticky. Také tuto property můžeme svázat (bind) v QML s libovolným počtem
vlastností libovolného počtu komponent. Pokud se hodnota této property změní,
automaticky se změní i na všech místech v GUI, kde je použita. Rovněž pokud ji
změníme z GUI (viz další díl), pak se změní i v Pythonu.


## Popis programu
Program reprezentuje jeden z nejjednoduššich interaktivních programů - obsahuje
textové pole a tlačítko, při každém stisku tlačítka se číslo v textovém poli
zvýší o jedna. Abychom toho dosáhli, potřebujeme mít v programu třídu, která
bude jako context property přidaná do QML a která bude umět GUI předat hodnotu
počitadla a bude schopna zpracovat událost stisku tlačítka. Tuto třídu jsme
nazvali `ClickModel` a obsahuje jeden slot `increase` a jednu property `count`.

V rámci inicializace ClickModelu je potřeba nezapomenout zavolat inicialízátor
`QObject`, protože jinak nebudou vazby s GUI fungovat. Dále je v programu
vytvořena instance ClickModelu, získán z view kontext a do něj přidána tato
instance pod jménem `clickModel`.

## Popis grafického rozhraní
V grafickém rozhraní je potřeba oproti minulému příkladu importovat
`QtQuick.Controls`, abychom mohli použít `Button`. Prvky jsou uspořádány do
sloupce pod sebou, k tomu slouží komponenta `Column`, pokud bychom chtěli mít
komponenty v řádku, existuje ekvivalentní komponenta `Row`. V komponentě `Text`
je provedena vazba property `count` našeho z našeho modelu v Pythonu k
vlastnosti `text`, neboli tomu, co komponenta vypíše. V komponentě Button je pak
následně provedeno připojení signálu `onClicked` do slotu `increase` našeho
modulu. Po spuštění pak můžeme ověřit funkčnost klikáním na tlačítko, počitadlo
by se mělo automaticky aktualizovat. Do konzole je vypisována původní a nová
hodnota při zavolání setteru.

## Zdroje
 - [Signals and Slots](https://doc.qt.io/qt-5/signalsandslots.html)
 - [Embedding C++ Objects into QML with Context Properties](https://doc.qt.io/qt-5/qtqml-cppintegration-contextproperties.html) - sice pojednává o C++, ale principy jsou platné stejně i pro Python
 - [The Property System](https://doc.qt.io/qt-5/properties.html) - opět více zaměřené na C++, ale ukazuje to možnosti property
