# Grammo — Compilatore per un Linguaggio di Programmazione

## Descrizione

**Grammo** è un linguaggio di programmazione progettato ad hoc e dotato di un compilatore completo, sviluppato in Python. Il compilatore implementa una pipeline classica: parsing, costruzione dell’AST, analisi semantica e type checking, generazione di codice **LLVM IR**, ottimizzazione ed esecuzione **Just-In-Time (MCJIT)**.

L’obiettivo del progetto è realizzare un compilatore end-to-end, mantenendo una separazione netta tra front-end, semantica e backend LLVM.

## Architettura del progetto

La struttura del progetto riflette le principali fasi di compilazione:

```
lex_syntax/        # grammatica Lark e parsing
semantic/ast_builder.py    # costruzione dell’AST
semantic/*         # analisi semantica e type checking
codegen/          # generazione LLVM IR, ottimizzazione e JIT
main.py           # entry point CLI
test/             # programmi di esempio (.gm)
requirements.txt  # requisiti di dipendenza
```

## Linguaggio e semantica (sintesi)

* Tipi primitivi: `int`, `real`, `bool`, `string`, `void`
* Costrutti principali: dichiarazioni, assegnamenti, chiamate, `if / elif / else`, `while`, `for`, `return`, I/O
* La grammatica è volutamente permissiva: la correttezza è garantita dall’analisi semantica

### Regole semantiche essenziali

* identificatori devono essere dichiarati prima dell’uso;
* shadowing vietato;
* compatibilità dei tipi:

  * tipi identici sempre validi;
  * promozione implicita ammessa solo `int → real`;
* distinzione tra:

  * chiamate come statement (solo funzioni `void`);
  * chiamate come espressione (solo funzioni non-`void`);
* per funzioni non-`void` tutti i percorsi devono garantire un `return`;
* vincolo di entry point:

  * deve esistere `main`;
  * `main` deve essere `void` e senza parametri.

## Generazione del codice

Il backend genera **LLVM IR** utilizzando *llvmlite*, assumendo un AST già validato semanticamente.

### Mapping dei tipi

| Grammo | LLVM   |
| ------ | ------ |
| int    | i32    |
| real   | double |
| bool   | i1     |
| string | i8*    |
| void   | void   |

* variabili locali gestite con `alloca` + `load/store`;
* promozione `int → real` applicata in modo puntuale;
* concatenazione di stringhe tramite funzioni libc (`malloc`, `strlen`, `strcpy`, `strcat`).

## Ottimizzazione ed esecuzione

Dopo la generazione dell’IR:

* viene applicata una pipeline di ottimizzazione LLVM (livelli 0–3);
* il modulo è compilato ed eseguito interamente in memoria tramite **MCJIT**;
* la funzione `main` è invocata con firma `void main()`.

## Dipendenze

Il progetto richiede le seguenti librerie Python:

* **lark** — per analisi lessicale e sintattica;
* **llvmlite** — per generazione, ottimizzazione ed esecuzione di LLVM IR.

Installazione rapida:

```
pip install lark llvmlite
```

## Utilizzo del compilatore

Il compilatore è utilizzabile da riga di comando tramite `main.py`.

### Sintassi

```
python -m src.grammo.main FILE_SORGENTE [OPZIONI]
```

### Opzioni

* `FILE_SORGENTE`
  File Grammo (`.gm`) da compilare ed eseguire.

* `-o, --output`
  Salva il codice LLVM IR generato su file.

* `-O, --opt-level`
  Livello di ottimizzazione LLVM (0–3, default: 3).

* `-a, --ast`
  Stampa a video l’AST generato dopo il parsing.

### Esempio

```
python -m src.grammo.main src/grammo/test/input/factorial.gm -o out.ll -a
```

## Limitazioni note

* assenza di short-circuiting per `&&` e `||`;
* gestione delle stringhe con `malloc` senza `free` automatico;
* input string con buffer fisso (256 byte).

## Stato del progetto

Il compilatore realizza un flusso completo **parsing → semantica → LLVM IR → ottimizzazione → JIT**, ed è pensato come progetto didattico, chiaro e coerente con l’architettura classica dei compilatori.
