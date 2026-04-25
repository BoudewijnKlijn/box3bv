Gisteren plaatste ik deze berekening/ vergelijking tussen beleggen in box 2 en box 3.

Met nog een paar extra aannames kan de hele berekening versimpeld worden tot onderstaande formule. Enkel de aangenomen groei van aandelen en de looptijd zullen noemenswaardig verschillen van persoon tot persoon. 


Formule (ratio) = `(    ((b - 1) * (v - 1) * (d + G) * ((d * (-v) + d + G + 1) ** T - 1))    / (d * (-v) + d + G)    + 1) / (1 + (d + G) * (1 - a)) ** T`

Deze figuur toont de ratio van vermogen opgebouwd via de BV maar terug in prive in vergelijking met altijd prive. Voorbeeld: 5% koersgroei per jaar en BV liquideren na 30 geeft 28% meer vermogen opgebouwd via de BV. 


* t = jaar in bv
* g = koersgroei per jaar
* d = 0.02 (dividend yield per jaar)
* a = 0.36 (box 3 tarief)
* v = 0.19 (vpb)
* b = 0.245 (box 2 tarief)

**Extra aannames: belangrijk!**

* Het is altijd verstandig om iets prive te beleggen om de 1.800 euro vrijstelling in box 3 te benutten. In de bovenstaande formule neem ik de vrijstelling niet mee. Daarmee kijk ik alleen naar het marginale belastingtarief, dus nadat de vrijstelling is gebruikt, ofwel altijd 36%.
* Geen kosten om te beleggen via BV (noch eenmalig, noch jaarlijks)

**Afleiding**

Beleggingen in box 3 maken elk jaar winst gelijk aan prijsstijging `g` plus dividend yield `d`. Over de winst moet belasting worden betaald. Ik neem aan dat de vrijstelling volledig is benut, dus de winst wordt volledig belast met `a = 36%`.

Na `t` jaar is het vermogen in prive gegroeid: `startkapitaal * (1 + (g + d) * (1 - a)) ** t`

(`**` betekent tot de macht)

In de BV wordt dividend `d` belast met vennootschapsbelasting vpb `v`. Dividend na belasting wordt belegd. De prijsstijging `g` wordt niet direct belast, pas als de beleggingen worden verkocht.

Na `t` jaar is het vermogen in de BV gegroeid tot: `startkapitaal * (1 + g + d * (1 - v)) ** t`

Er moet nog vpb worden betaald over ongerealiseerde prijsstijging. Over het herbelegde dividend na belasting is al vpb betaald dus dat is uitgezonderd.

Reeds belast:

* Na jaar 1 is dat: `startkapitaal * d`
* Na jaar 2 is dat: `startkapitaal * (d + d * (1 + g + d * (1 - v)))`
* Na jaar t is dat: `startkapitaal * [som van i = 0 tot t-1 (d * (1 + g + d * (1 - v)) ** i)]`
* Dit versimpeld tot: `startkapitaal * (d * (1 - v) * ((d * (1 - v) + g + 1) ** t - 1)) / (d * (1 - v) + g)`

Over ongerealiseerde winst moet uiteindelijk vpb worden betaald. Dat geeft `after_tax = (1 - v) * (vermogen - startkapitaal - reeds_belast)`. 

Over `after_tax + reeds_belast` moet dividend belasting `b` worden betaald. Vermogen in prive wordt dan: `startkapitaal + (after_tax + reeds_belast) * (1-b)`

Alles samenvoegen en wolfram alpha kan het enigszins versimpelen tot bovenstaande formule.