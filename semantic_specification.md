# Specifica di Analisi Semantica - Progetto Grammo

## 1. Introduzione
Questo documento descrive le specifiche e le scelte implementative per la fase di analisi semantica del compilatore Grammo. L'obiettivo dell'analisi semantica è verificare la correttezza del programma oltre la sintassi, garantendo la coerenza dei tipi, la corretta gestione degli scope e la validità del flusso di controllo.

Il codice sorgente relativo a questa fase si trova nel package `src.grammo.semantic`.

## 2. Abstract Syntax Tree (AST)
L'AST rappresenta la struttura gerarchica del programma depurata dai dettagli sintattici non necessari.
**File di riferimento**: [`src/grammo/semantic/ast_nodes.py`](../src/grammo/semantic/ast_nodes.py)

### Scelte Implementative
*   **Dataclasses**: Utilizzo di Python `dataclasses` per definire i nodi, garantendo un codice conciso e immutabile di default.
*   **Gerarchia dei Nodi**: Tutti i nodi ereditano da una classe base `Node` che traccia le informazioni di debug (linea, colonna).
    *   `Stmt`: Istruzioni che non producono valore (es. `IfStmt`, `WhileStmt`, `AssignStmt`).
    *   `Expr`: Espressioni che valutano a un tipo (es. `BinaryExpr`, `Literal`, `FuncCallExpr`).
    *   `Declaration`: Definizioni di variabili o funzioni.

## 3. Tabella dei Simboli
La tabella dei simboli gestisce la visibilità degli identificatori (variabili e funzioni) e i loro tipi associati.
**File di riferimento**: [`src/grammo/semantic/symbol_table.py`](../src/grammo/semantic/symbol_table.py)

### Gestione dello Scope
L'implementazione utilizza una **pila di scope** (`List[Dict[str, Symbol]]`).
1.  **Scope Globale**: Risiede alla base della pila (`scopes[0]`).
2.  **Scope Locale**: Viene creato (`enter_scope`) all'ingresso di una funzione e distrutto (`exit_scope`) all'uscita.
3.  **Lookup**: La ricerca di un simbolo avviene dall'ultimo scope inserito (più interno) risalendo fino a quello globale.

Si è scelto di implementare uno scoping statico (lexical scoping) standard.

## 4. Analizzatore Semantico
L'analizzatore semantico è il cuore del processo di validazione. Utilizza il pattern *Visitor* per attraversare l'AST.
**File di riferimento**: [`src/grammo/semantic/semantic_analyzer.py`](../src/grammo/semantic/semantic_analyzer.py)

### Processo di Analisi
L'analisi avviene in più passaggi per supportare riferimenti in avanti (forward references) e validazioni complesse.

#### Fase 1: Registrazione Globale
Scansione delle dichiarazioni di alto livello (`analyze` method).
*   Le firme delle funzioni vengono registrate nella tabella dei simboli prima di analizzarne i corpi. Questo permette alle funzioni di chiamarsi reciprocamente indipendentemente dall'ordine di definizione nel file.
*   Le variabili globali vengono registrate e verificate.
*   **Verifica Entry Point**: Si controlla la presenza e la firma corretta della funzione `main` (deve essere `void` e senza parametri).

#### Fase 2: Analisi dei Corpi e Type Checking
Visita approfondita dei corpi delle funzioni.
*   Vengono visitati gli statement e le espressioni.
*   Ogni espressione visitata restituisce il proprio **tipo** (stringa `int`, `real`, `bool`, `string`, `void`).

### Regole di Validazione Implementate

#### Gestione dei Tipi (Type Checking)
Il sistema è fortemente tipizzato con alcune coercizioni implicite:
*   **Compatibilità**: `int` è compatibile con `real` (promozione implicita), ma non viceversa.
*   **Operazioni Binarie**:
    *   Aritmetica (`+`, `-`, `*`, `/`): Supporta `int` e `real`. Somma tra stringhe supportata (concatenazione).
    *   Logica (`&&`, `||`, `!`): Richiede operandi `bool`.
    *   Confronto (`<`, `>`, `==`, ecc.): Richiede tipi compatibili.
*   **Assegnamenti**: Il tipo dell'espressione a destra deve essere compatibile con il tipo della variabile a sinistra.

#### Gestione dello Shadowing
**Scelta di progetto**: Lo shadowing è **proibito**.
*   Se un parametro o una variabile locale ha lo stesso nome di una variabile globale o di una funzione già definita, viene sollevato un errore semantico. Questo riduce l'ambiguità e i bug accidentali.
*   Codice: `if self.symbol_table.lookup(param.name): self.error(...)`.

#### Control Flow Analysis
Per le funzioni con tipo di ritorno diverso da `void`, il compilatore deve garantire che **tutti i percorsi di esecuzione** restituiscano un valore.
*   Implementato nel metodo `_check_all_paths_return`.
*   Analizza ricorsivamente blocchi `If/Else`. Un `If` garantisce il ritorno solo se ramo `then`, ramo `else` ed eventuali `elif` restituiscono tutti un valore.
*   I cicli (`While`, `For`) non sono considerati percorsi garantiti poiché la condizione potrebbe essere falsa inizialmente.

#### I/O Semantics
*   **Input**: Si verifica che l'argomento di interpolazione `#(var)` sia effettivamente un riferimento a variabile (`VarRef`) e non un'espressione generica, poiché deve ricevere un valore.
*   **Output**: Supporta espressioni generiche.

## 5. Gestione degli Errori
Gli errori semantici sollevano l'eccezione `SemanticError`, fornendo un messaggio descrittivo e, dove possibile, il riferimento alla riga del sorgente in cui si è verificato l'errore.

---
*Documento generato automaticamente dall'assistente AI Antigravity.*
