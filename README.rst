==============================================
PrincipiVaje -- Pomoč za razumevanje PPRI
==============================================

PPRI je spletni vmesnik knjižnice za snov PPRI(Principi porazdeljene in računalniške inteligence)

`Online različica <http://ppri-feri.herokuapp.com/>`_


Features
---------

* Nevronska mreža z vzvratnim prenosom napake (Backpropagation) z paketnim učenjem
* Hopfieldova nevronska mreža
* Učenje Hopfieldove nevronske mreže
* Učenje nevrona z vzratnim prenosom napake s CEE in MSE napako z logistično in TLU funkcijo

Installation
------------

Paket potrebuje Pyramid in ostale knjižnice. Najboljše je uporabiti virtualenv.

    python setup.py develop

    pserve development.ini

Za samo mrežo je potrebna samo datoteka neuralnetwork in numpy knjižnica.


Testiran je pod Pythonom 2.7

TODO
-------------

* Rekurzivna Elmanova nevronska mreža...
