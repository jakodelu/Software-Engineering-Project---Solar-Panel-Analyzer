# Test strutturale SPA_BetaV1.2 - Branch Coverage 100%

## Getting Started

L'obiettivo è avere **Branch Coverage del 100%**.

Analizzando attentamente le funzionalità e il codice di SPA, oltre a considerare le possibilità di ***INPUT*** e seguendo la ***PROCEDURA SEQUENZIALE*** dell'algoritmo di elaborazione sviluppato, si nota che tutti i BRANCH dipendono unicamente da:
* IMMAGINI (se inserita, numero immagini, estensione dell'immagine - JPG o TIF - e dimensione - quest'ultima è implicita nella scelta dell'estensione)
* PARAMETRI (checkBox flaggate e valori inseriti - in totale ci sono 8 possibilità)

Per quanto evidenziato, il grafo di flusso di controllo (CFG) può essere ridotto come nella figura ***CFG.png*** allegata.
Tale grafo ricopre tutti i branch del software, essendo che le scelte (if) del codice dipendono tutte dagli input forniti dall'utente.

![img](https://github.com/mnarizzano/se-project-46/blob/master/test_struturali/cfg.png)<br />
***CFG.png***

Per supportare l'analisi del comportamento di SPA e delle linee di codice hittate, è stata utilizzata una libreria di Python che ha come scopo proprio il calcolo della copertura durante l'esecuzione del sotware: ***coverage.py***.

## Installing and run coverage.py in Ubuntu 16.04.5 LTS (Xenial Xerus)

Seguire le seguenti istruzioni nel Terminale.

1) Installing:

> sudo python3 -m pip install coverage

2) Running:

> coverage run main.py

3) Report:

Nel terminale

> coverage report -m files

Rappresentazione HTML

> coverage html files

## Test cases

Analizzando il CFG sono stati identificati i seguenti casi:

|id| case | parameters |
|--|--------------------|---------------------------------|
| 1	|	0 files selected	|	no parameters|
| 2	|	1 file JPG		  	| add Debug Mode|
| 3	|	2 files JPG		  	|	add Panels Size|
| 4	|	3 files JPG		  	|	add Blur|
| 5	|	1 file TIF		  	|	add Dilate|
| 6	|	2 files TIF		  	|	add Area Lim (min)|
| 7	|	1 file JPG		  	|	add Auto Threshold|
| 8	|	1 file JPG		  	|	add Low Threshold (remove Auto)|
| 9	|	1 file JPG		  	|	add High Threshold (remove Auto)|

## Results

### Simulazione dell'utente

Utilizzando il tool coverage di Python, è stato eseguito direttamente il software (simulando l'utente) nei 9 casi identificati e il risultato è una copertura del **94%**.

Non si può raggiungere il 100% per alcuni motivi:
* alcune funzioni set e get implementate di default non vengono utilizzate
* alcune parti di codice non vengono eseguite poichè riferite al caso di esecuzione da CLI, in tale situazione il software compie le stesse identiche attività, ma ha un modo diverso di raccogliere i parametri e di scegliere la cartella output.

Si possono osservare i risultati nelle figure ***coverage.png*** e ***coverage_table.png*** allegate.

![img](https://github.com/mnarizzano/se-project-46/blob/master/test_struturali/coverage.png)<br />
***coverage.png***

![img](https://github.com/mnarizzano/se-project-46/blob/master/test_struturali/coverage_table.png)<br />
***coverage_table.png***

### Testing by code

Utilizzando la libreria ***unittest.py*** di Python, sono stati eseguiti alcuni test del modulo Elaboration.py (Unit test), cuore di SPA, dove risiedono la maggior parte degli IF, quindi i vari branch.
I test sono stati eseguiti solo per alcuni casi, poichè il software esegue una nuova elaborazione (chiamando il modulo) per ogni immagine, quindi non sono testati input composti da più immagini.

I casi testati sono:<br />
a) 1 file JPG	|	Debug Mode<br />
b) 1 file JPG	|	add Panels Size<br />
c) 1 file JPG	|	add Blur<br />
d) 1 file TIF	|	add Dilate<br />
e) 1 file TIF	|	add Area Lim (min)<br />
f) 1 file JPG	|	add Auto Threshold<br />
g) 1 file JPG	|	add Low Threshold and High Threshold<br />

Il test ha successo se lo stato dell'elaborazione è 4.
Come si può notare nella figura ***unit_test.png*** allegata, i test hanno avuto successo.

![img](https://github.com/mnarizzano/se-project-46/blob/master/test_struturali/unit_test.PNG)<br />
***unit_test.png***

## Errors

Durante l'esecuzione dei casi è stato trovato un errore alla riga 559 di Elaboration.py (divisione tra due dati di tipo string).
L'imprecisione è stata corretta.

## Author

***Jacopo De Luca***<br />
***Corso di Software Engineering***<br />
***Corso di Laurea Magistrale in Ingegneria Informatica - DIBRIS***<br />
***Università degli Studi di Genova***<br />

jacopodeluca.private@gmail.com
