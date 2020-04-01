# Převod DMS na stupně a zpět

# Modely a View v Qt
V [minulém příkladu](../02_clicker/README.md) jsme se naučili používat
kontextové proměnné jakožto způsob, jak dopravovat data z Pythonu do QML. Ve
skutečnosti jsme použili jeden ze základních konceptů nejen Qt, sloužících k
oddělení aplikační logiky od grafického rozhraní, a to Model-View-Delegate. O
delegátech bude řeč příště, nyní si vysvětlíme Model a View.

Model je objekt, který drží nějaká data a ke kterému přistupuje aplikační
logika. Můžeme také říci, že model drží stav. Data, která drží, obvykle drží v
nějaké formě, se kterou se dobře pracuje aplikační logice. V minulém případě to
byla property 'counter', může to být seznam, slovník nebo i nějaká složitější
objektová struktura. Model se nestará o to, jak budou data zobrazena, i když
forma uložení může zvolena tak, aby následné zobrazení bylo jednoduché.

View je pak nějaká komponenta, která data z modelu zobrazuje. Pojem view je zde
nejednoznačný, protože jako view označujeme i celý soubor s grafickým rozhraním,
v této kapitole budeme brát za view komponentu, která slouží ke zobrazení dat z
modelu. Komponenty pro složitější modely se obvykle přímo jmenují `<něco>View`,
ale jako view může sloužit v podstatě libovolná komponenta, která je schopna
danou vlastnost modelu zobrazit. V minulém případě bylo view komponenta `Text`,
modelem byl objekt `click_model`. 

Modelů může být v aplikaci více, stejně tak každý model může mít více view.
Například model reprezentující nějaký bod na mapě může mít view vrstvu na mapě
zobrazující bod a vedle mapy dále textové pole se souřadnicemi tohoto bodu. V
mapě můžeme chtít zobrazovat i polygony, tyto polygony budou mít svůj vlastní
model a jako view jim bude sloužit jiná vrstva v mapě.

# Obousměrná vazba
View nemusí sloužit jen k zobrazení nějakého modelu, ale může umožňovat i změny
tohoto modelu. Vazby jsou vždy jednosměrné, pokud potřebujeme, aby view mohl
změnit data v modelu, musíme druhý směr vazby přidat explicitně. Pokud to
neuděláme, pak změna ve view zůstane ve view a když se změní model, view
provedenou změnu zahodí a zobrazí hodnotu z modelu. Pokud přidáme vazbu opačným
směrem explicitně, musíme být opratrní při implementaci modelu, hrozí totiž
zacyklení.

Vazba view a modelu není totiž dána přímo property, která je svázána,
ale notifikacemi, že se property změnila. Pokud dojde v modelu ke změně hodnoty
nějaké property, je vyslán notifikační signál (viz setter v minulém příkladu).
View je na tento signál připojeno a když dostane notifikační signál, zeptá se na
aktuální hodnotu dané property v modelu a tu zobrazí. Naopak to funguje stejně,
když máme svázán view a model směrem z view do modelu a dojde ke změně view
(například uživatel začne psát do
[`TextInput`u](https://doc.qt.io/qt-5/qml-qtquick-textinput.html), po každém
napsaném / smazaném znaku vyšle `TextInput` signál, který zachytí property a
zavolá *setter* s aktuální hodnotou z view. Tím ale dojde ke změně modelu, tedy
model vyšle notifikační signál, ten zachytí view a načte si z modelu aktuální
hodnotu. Tím ale došlo ke změně ve view a tak je vyslán notifikační signál,
který zachytí model ... a byli bychom v kruhu, kdybychom si na to nedali pozor. 

Z tohoto důvodu je potřeba být v setterech opatrný a vysílat notifikační signál
jen tehdy, když skutečně dojde ke změně hodnoty v modelu. Jednak se tím ušetří
trochu výkonu, kdy view nebude muset překreslovat jednu hodnotu za tu samou, ale
hlavně tím rozbijeme zacyklení, protože když model dostane zprávu, že se změnila
hodnota property a zavolá setter, tak setter již žádný signál nevyšle a cyklus
je přerušen. 

Pokud vytvoříme obousměrnou vazbu, může si někdy QML stěžovat na `QML QQuickTextInput: Binding loop detected`.
Je vhodné ověřit, že nedochází k zacyklení a následně je možné toto upozornění
ignorovat. 

## Popis programu
Program slouží k převodu úhlových jednotek mezi desetinnými stupni a stupni,
minutami a vteřinami. Program obsahuje 4 textová pole, kde každé je obousměrně
svázáno s jednou property a 2 tlačítka, která jsou připojena k metodám objektu
třídy `DMSModel`. 

Třída `DMSModel` slouží jako model pro celou aplikaci, v jednotlivých property
je ukázka, jak lze zápis property postupně zkrátit při zachování stejné
funkčnosti. Celý getter lze jako lambda funkci integrovat přímo do vytváření
property. Setter je složitější a pokud bychom se pokusili o totéž, nebyl by
výsledek o mnoho kratší a byl by výrazně méně čitelný. Notifikační signál nelze
integrovat stejně jako getter, protože z důvodů vazeb musí být pojmenovanou
metodou dané třídy. Zbytek kódu je obdobný jako u minulého příkladu.

## Popis grafického rozhraní
Grafické rozhraní je tvořeno dvěma řádky (komponenta
[`Row`](https://doc.qt.io/qt-5/qml-qtquick-row.html)), které jsou uspořádny do
sloupce (komponenta [`Column`](https://doc.qt.io/qt-5/qml-qtquick-column.html)).
Aby jednotlivé nápisy v řádku nesplývaly, má řádek nastavenu vlastnost `spacing`
na 2 px. Jednotlivá pole, do kterých uživatel zadává stupně, minuty a vteřiny
jsou tvořeny komponentami [`TextInput`](https://doc.qt.io/qt-5/qml-qtquick-textinput.html).

Komponenta [`TextInput`](https://doc.qt.io/qt-5/qml-qtquick-textinput.html)
se chová obdobně jako komponenta `Label`, ale navíc umožňuje editaci textu.
Vazba směrem z Pythonu je vytvořena ve vlastnosti `text`. Abychom mohli vytvořit
opačnou vazbu, musíme se umět odkázat na konkrétní komponentu `TextInput`.

Každé komponentě QML můžeme nastavit vlastnost `id` - identifkátor, který by měl
být v rámci celého QML unikátní. Pak na takovou komponentu můžeme odkudkoli z
QML odkazovat právě pomocí jejího identifikátoru. Pojmenování identifikátoru je
vhodné volit tak, aby z něj bylo jasné, co je daná komponenta zač a co v sobě
uchovává. Pojmenovává se obvykle camelCase ve formátu `<obsah><Typ>`, tedy
například `secInput`. 

Vazbu z QML do modelu (a tedy i do Pythonu) vyrobíme pomocí komponenty
[`Binding`](https://doc.qt.io/qt-5/qml-qtqml-binding.html). Tato komponenta má
široké možnosti použití, my ji zatím použijeme jen velmi jednoduše. Abychom
mohli vytvořit vazbu, musíme vědět, property kterého objektu svazujeme s jakou
hodnotou / property. Objekt určíme pomocí vlastnosti `target`, jeho property
(cíl vazby) pomocí vlastnosti `property` a zdroj vazby pomocí vlastnosti
`value`(zde využijeme identifikátor `TextInput`u). Od této chvíle kdykoli se
změní zdroj, změní se i cíl a díky tomu, že opačnou vazbu máme definovanou v
TextInputu samotném, máme vytvořenou obousměrnou vazbu a kdykoli se změní model,
změní se i text v `TextInput`u a naopak.


Když program spustíme a zkusíme převést jednu vteřinu na desetiny stupně,
program nám vypíše `QML QQuickTextInput: Binding loop detected for property
"text"`. Je tomu tak proto, že `TextInput` má pomocí vlastnosti `maximumLength`
omezenou maximální délku vloženého textu. Pokud převedeme jednu vteřinu na
desetiny stupně, získáme periodické číslo. Po klikutí na *To float!* tedy
vznikne dlouhé číslo které se přes *setter* zapíše do property `deg_float`. Přes
notifikační signál se propíše do `TextInput`u, kam se ale celé nevejde, tedy
zbylé číslice jsou zahozeny. Protože se `TextInput` změnil, je znovu vyvolán
*setter* property `deg_float`, ale tentokrát se zkráceným číslem (protože se
propisuje skutečný obsah `TextInput`u). Zkrácené číslo neodpovídá původnímu,
tedy je znovu přiřazeno a znovu je vyslán notifikační signál. Proběhne nové
kolečko až do *setter*u, kde už ale nedochází ke změně a tedy se celý cyklus
zastaví. Qt ale toto chování vyhodnotí jako smyčku ve vazbách a proto vyvolá
chybovou hlášku. 

## Zdroje
 - [How to do Bi-directional Data Binding in Qt](http://imaginativethinking.ca/bi-directional-data-binding-qt-quick/)
