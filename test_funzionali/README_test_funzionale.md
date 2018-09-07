# Test funzionale SPA_BetaV1.2

## Getting Started

Il test funzionale è un metodo Black Box per testare un software.
In questo tipo di testing, il tester si è immedesimato nell'utente che utilizzerà SPA. Questi è a conoscenza solo delle funzionalità del tool, decise a priori e contenute nei documenti di progettazione, in particolare nell'URD è nota la tabella dei requisiti e nel DRS l'use cases.

Quindi il test funzionale di SPA si è basato solo sulla conoscenza delle azioni permesse all'utente.

## Test cases

Come spiegato nel *README_test_strutturale.md*, i casi si limitano all'inserimento di input, ovvero le immagini e i parametri.
Il tester ha eseguito SPA provando varie combinazioni di input e ha esaminato il comportamento del tool e l'output, paragonandoli ai risultati aspettati, secondo quanto indicato nei documenti.

## Testing

Di seguito la tabella raffigurante il testing.

| id | scenario | immagine | parametri | risultato atteso | risultato effettivo |
|----|----------|----------|-----------|------------------|---------------------|
| 1 | Nessun file in input | Nessuna | Default | Errore | Ok |
| 2 | File di formato errato | .PNG | Default | Errore elaborazione | Ok - Nessun errore, ma reset degli input (immagine non considerata) |
| 3 | Parametri di tipo errato | .JPG/.TIF | Inserimento lettere | Errore | Ok - Le lettere vengono scartate, sono permessi solo caratteri numerici da 0 a 9 |
| 4 | Input valido | .JPG/.TIFF | Caratteri numerici | Avvio elaborazione | Ok - Lancio dell'elaborazione (mancanza feedback in Ubuntu) |
| 5 | Apri immagine | Nessuna | Default | Scelta input | Ok - Scelta di una o più immagini, il cui percorso viene mostrato nella GUI |
| 6 | Apri 50 immagini | Nessuna | Default | Scelta input | Fail - Le immagini vengono lette e successivamente elaborate, ma non tutte vengono mostrate nella GUI |
| 7 | Avvio elaborazione e analisi output | .JPG/.TIF | Default | Salvataggio nella cartella output (da creare se non esiste) dei pannelli riconosciuti e dei dati | Ok |
| 9 | Debug Mode | .JPG/.TIF | DebugMode flaggata | Salvataggio di informazioni supplementari | Ok - Nell'output si trovano anche le immagini dei vari step |
| 10 | Lancio procedura su più immagini | n .JPG/.TIF | Default | Sequenza di n elaborazioni | Ok - n elaborazioni completate, visibili nell'output
| 10 | File nella barra in alto | .JPG/.TIF | Default | Scegli immagine | Ok |
| 11 | Help nella barra in alto | Nessuna | Default | Informazioni e guida del tool | Ok |
| 12 | Chiudi | Nessuna | Default | Chiusura tool | Ok |
| 13 | Chiudi nella barra in alto | Nessuna | Default | Chiusura tool | Ok - Viene mostrata un finestra di controllo |

## Author

***Jacopo De Luca***<br />
***Corso di Software Engineering***<br />
***Corso di Laurea Magistrale in Ingegneria Informatica - DIBRIS***<br />
***Università degli Studi di Genova***<br />

jacopodeluca.private@gmail.com
