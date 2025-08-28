# Calcolatore Gradazione Alcolica e Stima Alcolemia - Web App

<div align="center">

![Current Version](https://img.shields.io/badge/current-v2.0-blue?style=flat-square)
![Next Version](https://img.shields.io/badge/coming%20soon-v3.0-orange?style=flat-square)
![Platform](https://img.shields.io/badge/platform-web-green?style=flat-square)
![Language](https://img.shields.io/badge/javascript-vanilla-yellow?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-orange?style=flat-square)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)
![Mobile](https://img.shields.io/badge/mobile-optimized-purple?style=flat-square)

</div>

Una sera d'estate di un non meglio specificato giorno della settimana, mi trovavo con i miei amici in un bar nella mia città. La noia, quella tagliente compagna che si materializza nei momenti più inaspettati, mi stava divorando, così ho cominciato a guardare intensamente il bicchiere di gin tonic saldo nella mia mano sinistra (mai tenere il drink con la mano dominante...). Chissà qual è il grado alcolico effettivo di questa bevanda, pensai. Il mio sguardo si perse per un fugace attimo nella folla di giovani che consumavano allegramente bevande alcoliche, raccolti in gruppetti trainati da innocente spensieratezza. Quanti di loro lo vorrebbero sapere? Quanti di loro vorrebbero conoscere il proprio tasso alcolemico dopo una serata, con la stessa precisione con cui consultano il saldo del conto corrente e si promettono poi di smettere?</br>
Molti, secondo me. Tutti, probabilmente.</br>
Quante volte lanciamo i dadi e ci abbandoniamo alla dea fortuna in un insensato gioco probabilistico dal valore atteso certamente negativo? Più spesso di quello che immaginiamo, d'altronde anche gli esperti inciampano nella _gambler’s fallacy_, anche se per gradi di difficoltà diversi dal comune mortale che ordina "ancora uno, l'ultimo" convinto di essere perfettamente lucido.</br>
E quindi, sia mai vietarmi una metaforica passeggiata che si sarebbe presto trasformata in 40 ciclotimici giorni nel deserto. Sia mai che io mi perda una battaglia persa.

È così, foriero d'un lampo, che nasce questa applicazione web per il calcolo scientifico della gradazione alcolica dei cocktail, compresa di una stima dell'alcolemia basata sulla formula di Widmark avanzata. Il progetto è nato come strumento educativo per la consapevolezza del consumo di alcol e la prevenzione della guida in stato di ebbrezza.

### Versione Attuale (v2.0 - Open Source)
```
https://tmericj.github.io/cocktail-calculator/cocktail-app.html

```
### Prossima Release (v3.0 - Rolling out Soon)
La versione 3.0 sarà disponibile come applicazione web distribuita tramite link diretto.</br>
Nessuna installazione è richiesta, funziona su qualsiasi dispositivo moderno.</br>
Requisiti: Browser moderno (Chrome 80+, Firefox 75+, Safari 13+)

### Evoluzione del Progetto
Questo tool ha attraversato una significativa trasformazione architetturale, passando da una primitiva applicazione Python da terminale a una web app completa. La versione originale, basata su un database di 52 cocktail e un sistema di calcolo più semplice, è stata completamente riprogettata per offrire un'esperienza utente moderna e calcoli scientificamente più accurati.
Il database è stato espanso a oltre 120 bevande, includendo non solo cocktail famosi non presenti nel catalogo IBA, ma anche aperitivi regionali e una generica, per ora, lista di birre e vini. L'interfaccia è stata ripensata con un approccio mobile-first e organizzata in sezioni dedicate per ottimizzare il workflow dell'utente.


## Architettura Applicazione
### Interfaccia Utente
L'applicazione è strutturata in tre sezioni principali accessibili tramite navigazione a tab:
- **Sezione Ricerca**: Permette la ricerca rapida di cocktail per nome o categoria con visualizzazione immediata di gradazione alcolica, contenuto di alcol puro in grammi, ingredienti e proporzioni. Sono inoltre permesse ricerche con filtri applicati, suddivisi in "nome", "ingredienti", e "categoria", selezionabili singolarmente o in modo multiplo. Il sistema di ricerca è *case-insensitive* e supporta ricerche parziali (con almeno due lettere).
- **Sezione Calcolo Alcolemia**: Il cuore scientifico dell'applicazione, dove l'utente può costruire una sessione di bevute multiple inserendo cocktail, anche diversi tra loro, e quantità, per poi calcolare l'alcolemia basata sui propri parametri biometrici e sulle condizioni di consumo.
- **Sezione Database**: Visualizzazione completa del database. Questa sezione è organizzata per categorie: Classic (IBA), Contemporary (IBA), New Era (IBA), Aperitivo, Birra, Vino.

### Database delle Bevande
Il database contiene 120+ bevande categorizzate scientificamente:

87 cocktail IBA ufficiali (Classic, Contemporary, New Era) con l'aggiunta di alcune varianti famose</br>
17 aperitivi, inclusi cocktail regionali italiani (per ora solo Veneti)</br>
10 tipologie di birra con gradazioni medie</br>
7 categorie di vino con gradazioni e quantità medie</br>

Ogni voce contiene ingredienti con volumi precisi e gradazioni alcoliche, permettendo calcoli accurati della gradazione finale e del contenuto di alcol puro.


## Fondamenti Scientifici
### Calcolo della Gradazione Alcolica
La gradazione è calcolata usando la formula del volume pesato:
```
Gradazione = (Σ Volume_ingrediente × Gradazione_ingrediente) / Volume_totale × 100
```

Il contenuto di alcol puro in grammi utilizza la densità dell'etanolo (0.789 g/mL) e include un fattore di diluizione del 5% per tenere conto di ghiaccio sciolto, errori durante la preparazione o drink non completamente finiti.

### Sistema di Calcolo Alcolemia
#### Formula di Widmark Modificata
L'applicazione implementa la formula di Widmark con il calcolo personalizzato del Total Body Water (TBW) secondo Watson et al.:

```
TBW_uomo = 2.447 - (0.09516 × età) + (0.1074 × altezza_cm) + (0.3362 × peso_kg)
TBW_donna = -2.097 + (0.1069 × altezza_cm) + (0.2466 × peso_kg)

Fattore_Widmark = TBW / Peso_corporeo

BAC = (grammi_alcol × fattori_correzione) / (peso × fattore_Widmark) - (β × tempo_ore)
```

Fonte: P E Watson, I D Watson, R D Batt, (1980). Total body water volumes for adult males and females estimated from simple anthropometric measurements, *The American Journal of Clinical Nutrition*, *33*(1), 27-39. DOI: https://doi.org/10.1093/ajcn/33.1.27.

#### Fattori di Correzione Avanzati
**Livello di Fitness**: Il sistema considera tre livelli di forma fisica che influenzano il metabolismo dell'alcol:
- Sedentario: metabolismo base
- Attivo (2+ allenamenti/settimana): +5% efficienza metabolica
- Atleta (5+ allenamenti/settimana): +10% efficienza metabolica

**Idratazione**: Quattro livelli di idratazione durante il consumo influenzano la diluizione dell'alcol:
- Assente: -1.0% efficienza (disidratazione riduce metabolismo)
- Bassa (<100ml): baseline
- Media (300ml): +1.5% (TBW base più alto, dunque BAC iniziale inferiore)
- Alta (>1000ml): +2.5% (TBW base più alto, dunque BAC iniziale inferiore)

Da ciò si evince che le **persone allenate** metabolizzano l'alcol più efficacemente grazie a una migliore funzionalità epatica e una maggiore proporzione di massa magra, che processa l'alcol più velocemente rispetto al tessuto adiposo. Inoltre, poiché l'alcol si distribuisce nell'acqua corporea e i muscoli contengono circa il 75% di acqua contro il 10% del tessuto adiposo, gli atleti hanno un volume di distribuzione maggiore che comporta una diluizione iniziale superiore dell'alcol nel sangue. Anche per questo motivo viene considerato il livello di idratazione, che incide positivamente nel calcolo della TBW, aiutando a ridurre marginalmente l'effetto dell'alcol. Tuttavia, se l'utente si è allenato lo stesso giorno del consumo, il sistema applica una riduzione del 1% del tasso di eliminazione a causa della disidratazione muscolare.

In conclusione, una persona **allenata** e **idratata** presenta un **metabolismo più rapido** e una maggiore capacità di diluizione iniziale, motivi per cui registra un livello alcolemico più basso che smaltisce più velocemente.

### Simulazione Temporale
Per sessioni di bevute multiple, l'algoritmo simula l'assorbimento e l'eliminazione nel tempo:
- Calcola gli intervalli tra le ingestioni basandosi sulla durata totale
- Applica una curva di eliminazione lineare per ogni drink
- Considera l'effetto dello stomaco pieno (-30% assorbimento)
- Genera una timeline predittiva fino a 6 ore

### Limiti Legali Italiani

| Alcolemia (g/L) | Sanzioni |
|-----------------|----------|
| 0.0 - 0.5 | Guida consentita |
| 0.5 - 0.8 | Multa 527-2108€, sospensione 3-6 mesi |
| 0.8 - 1.5 | Arresto fino a 6 mesi, multa 800-3200€ |
| Oltre 1.5 | Arresto 6-12 mesi, confisca veicolo |


## Innovazioni Tecniche
### Responsive Design
L'interfaccia utilizza CSS Grid e Flexbox per un layout completamente responsivo. Il design è mobile-first per garantire una fruizione ottimale su smartphone, dove spesso avviene l'uso pratico dell'applicazione.

### Calcoli Real-time
Tutti i calcoli sono eseguiti client-side in JavaScript, garantendo privacy assoluta (nessun dato personale trasmesso) e performance immediate. L'architettura single-page elimina latenze di rete.

L'applicazione mantiene lo stato delle bevute aggiunte in memoria, permettendo modifiche dinamiche della composizione della sessione senza perdita di dati.

## Interface Preview

### Desktop Experience
<div align="center">
  <img src="assets/screenshots/desktop-v3-overview.png" alt="_Desktop Interface v3.0" width="800">
  <p><em>Soon to be Added – Interfaccia desktop v3.0: Sezione calcolo alcolemia</em></p>
</div>

### Mobile Experience  
<div align="center">
  <img src="assets/screenshots/mobile-v3-responsive.png" alt="_Mobile Interface v3.0" width="300">
  <p><em>Soon to be Added – Design mobile-first ottimizzato per uso pratico</em></p>
</div>

### Evolution Comparison (front page)
<div align="center">
  
**v1.0 - Python Terminal**  
<img src="Evolution_Comparison/Python_Version.png" alt="Version 1.0" width="600">

**v2.0 - First Web App**  
<img src="Evolution_Comparison/First_Web_App.png" alt="Version 2.0" width="600">

**v3.0 - Modern Web App**  
<img src="Evolution_Comparison/Second_Web_App.png" alt="Version 3.0" width="600">

</div>


## Sviluppi Futuri
Il tool verrà costantemente manutenuto.

### Prossimi Rilasci
Sezione "**Costruisci il Tuo Drink**": è in fase di studio e sviluppo una quarta sezione che permetterà agli utenti di creare cocktail personalizzati selezionando arbitrariamente ingredienti, volumi e gradazioni da un database esteso di liquori, mixer e guarnizioni. Questa funzionalità includerà sicuramente:
- Database ingredienti con oltre 200 bevande catalogate
- Calcolo automatico di gradazione e contenuto alcolico
- Suggerimenti di bilanciamento basati su proporzioni classiche

Inoltre, si vorrebbe offrire la possibilità di salvare **ricette personalizzate**.

A sviluppi futuri viene lasciato l'upgrade ad un sistema di **Profili Utente**, in cui memorizzare:
- Dati biometrici
- Preferenze di calcolo (fattori fitness, tolleranze)
- Storico delle sessioni per analisi longitudinale
- Cocktail e ricette preferite

Ancora in fase di studio di fattibilità ci sono ulteriori espansioni, come la traduzione in lingue diverse, geolocalizzazione per integrazione con le normative locali, integrazioni con dispositivi di terze parti.

## Considerazioni Tecniche e Limitazioni
Il sistema mantiene un margine di errore intrinseco di circa il 20%, tipico dei calcoli teorici di alcolemia. Fattori non modellabili includono variazioni genetiche del metabolismo (polimorfismi CYP2E1), condizioni mediche, farmaci, e tolleranza acquisita.
L'applicazione serve esclusivamente per scopi educativi e di awareness, non sostituendo mai misurazioni dirette tramite etilometro per decisioni legali o di sicurezza.

## Struttura Codebase
```
├── cocktail-app.html           # Applicazione principale (self-contained, version 2.0)
├── README.md                   # Documentazione
└── [legacy]/                   # Versione Python originale
    ├── gradazione_tool.py
    ├── database_ricette.csv
    └── test_tool.py
```

L'architettura (per ora) single-file facilita distribuzione e deployment, contenendo HTML, CSS, JavaScript e database in un unico documento.

## Changelog Versioni
### Changelog v1.0 - Foundation Release
Initial Python terminal-based implementation with core pharmacokinetic engine.
- Basic Widmark formula implementation with Watson TBW calculation
- CSV database with 52 IBA cocktails (Classic, Contemporary, New Era categories)
- Single and multiple drink BAC calculations with time progression
- Stomach condition modifier (-30% absorption when full)
- Terminal-based interactive menu system (7 options)
- Personalized cocktail modification with ingredient substitution
- Legal status classification with Italian driving limits

Core features:
- Weighted volume formula for alcohol graduation calculation
- Raw TBW-corrected Widmark factors for improved accuracy
- Timeline simulation with linear elimination modeling
- Category-based cocktail browsing and search functionality


### Changelog v2.0 - First Web Release
Major update: Advanced pharmacokinetic algorithm with fitness parameter
- Implemented distributed absorption model for multiple drinks
- Added fitness level parameter (sedentary/active/athlete) with +15-25% metabolism boost
- Temporal distribution of ingestions instead of single bolus
- Superposition principle for individual drink contributions
- Improved accuracy: reduced error from 71% to 27% in real-world testing
- Enhanced timeline predictions with continuous elimination modeling

Features added:
- Added 10 beer types (small/medium formats) with accurate ABV
- Added 6 wine categories with standard serving sizes
- Enhanced time formatting for better UX


### Changelog v3.0 (rolling out soon) - Full Web Application Architecture
Complete architectural transformation.
- Extended database: 120+ beverages including cocktails, aperitifs, beers, wines
- Mobile-First design: touch-optimized responsive layout with CSS Grid/Flexbox
- Advanced fitness modeling: Sedentary/Active/Athlete levels with metabolic corrections
- Acute exercise effects: same-day workout impact on elimination rates
- Hydration parameters: 4 level hydration system affecting BAC dilution

Technical architecture:
- Single-file self-contained HTML/CSS/JavaScript application
- No external dependencies or installation requirements
- Privacy-focused: all calculations performed locally
- Cross-browser compatibility (Chrome 80+, Firefox 75+, Safari 13+)

Regional specialties added:
- Te+ cocktail (Origin Bar Bassano) - 9.5% ABV tea-peach extract
- Leone aperitif - Traditional Veneto alternative to Americano
- Corrected Spritz variations (Classic vs Venetian preparations)

Scientific improvements:
- Enhanced TBW calculations with fitness-based corrections
- Hydration impact modeling (±2.5% BAC variation)
- Exercise-induced metabolism modifications
- Improved error margins through multi-factor calibration


---

**Bevi responsabilmente! Non guidare mai dopo aver bevuto alcol!**

*Tool sviluppato per educazione alla sicurezza stradale e consapevolezza del consumo di alcolici.*
