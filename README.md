# Calcolatore Gradazione Alcolica e Alcolemia

Un tool Python completo per calcolare la gradazione alcolica dei cocktail e stimare l'alcolemia per la sicurezza stradale, basato su un database di oltre 50 ricette ufficiali IBA e cocktail regionali.

## Caratteristiche

### Calcolo Gradazione Cocktail
- **Database Completo**: 52 cocktail con ricette ufficiali IBA e specialità regionali
- **Calcolo Preciso**: Formula del volume pesato per la gradazione alcolica
- **Personalizzazione Avanzata**: Modifica ingredienti, volumi e gradazioni
- **Cocktail Regionali**: Include specialità venete come Leone e Te+

### Calcolo Alcolemia (NOVITÀ!)
- **Formula di Widmark Avanzata**: Con calcolo TBW (Total Body Water) personalizzato
- **Parametri Completi**: Genere, peso, altezza, età, stomaco pieno/vuoto
- **Tempi di Smaltimento**: Calcola quando tornerai sobrio e quando potrai guidare
- **Limiti Legali**: Mostra le sanzioni previste dal Codice della Strada italiano

## Requisiti

- Python 3.7+
- pandas

## Installazione

```bash
cd "/Users/tommaso/Desktop/Progetti esterni/Gradiente alcolico"
pip install pandas
```

## Uso Rapido

```bash
python gradazione_tool.py
```

## Menu Principale

1. **Cerca un cocktail per nome** - Calcola gradazione e grammi di alcol puro
2. **Mostra tutti i cocktail disponibili** - Lista completa 52 cocktail
3. **Cerca per categoria** - Filtra per IBA, regionali, etc.
4. **Calcola cocktail personalizzato** - Modifica ricette esistenti
5. **Calcola alcolemia per cocktail specifico** - Stima scientifica dell'alcolemia
6. **Esci**

## Cocktail Disponibili

### Novità Regionali
- **Te+**: Estratto alcolico al tè pesca (9.5% vol) - Origin Bar, Bassano del Grappa
- **Leone**: Aperitivo veneto tradizionale
- **Spritz Variations**: Campari, Aperol, Select (classici e veneziani)

### Cocktail IBA 2024
- **The Unforgettables**: Negroni, Manhattan, Martini, Daiquiri, etc.
- **Contemporary Classics**: Cosmopolitan, Mojito, Caipirinha, etc.
- **New Era Drinks**: Espresso Martini, Paper Plane, etc.

## Sistema Alcolemia Avanzato

### Parametri Richiesti
- **Genere** (uomo/donna) - Influenza il fattore Widmark
- **Peso** (kg) - Base del calcolo
- **Altezza** (cm) - Per calcolo TBW preciso
- **Età** (anni) - Correzione metabolismo
- **Stomaco** (pieno/vuoto) - Riduce assorbimento del 30%
- **Tempo trascorso** - Calcola smaltimento

### Formula Scientifica
Utilizza la **Formula di Widmark modificata** con **TBW di Watson**:

```
TBW (uomo) = 2.447 - (0.09145 × età) + (0.1074 × altezza) + (0.3362 × peso)
TBW (donna) = -2.097 + (0.1069 × altezza) + (0.2466 × peso)

Fattore Widmark = TBW / Peso corporeo

Alcolemia = (Grammi alcol / (Peso × Fattore Widmark)) - (Beta × Ore)
```

### Output Dettagliato
- **Alcolemia al picco** e **attuale**
- **Stato legale** secondo il Codice della Strada
- **Tempo per azzeramento** completo
- **Tempo per guidare** legalmente (sotto 0.5 g/L)
- **TBW personalizzato** e **Fattore Widmark**

## Limiti Legali Italiani

| Alcolemia (g/L) | Sanzioni |
|-----------------|----------|
| 0.0 - 0.5 | ✅ Guida consentita |
| 0.5 - 0.8 | ⚠️ Multa 527-2108€, sospensione 3-6 mesi |
| 0.8 - 1.5 | ❌ Arresto fino a 6 mesi, multa 800-3200€ |
| Oltre 1.5 | 🚨 Arresto 6-12 mesi, confisca veicolo |

## Esempi di Uso

### Calcolo Gradazione
```
Cerca: "Negroni"
Risultato:
- Gradazione: 27.0% vol
- Alcol puro: 21.33 grammi
- Ingredienti: Gin 30ml (40°), Campari 30ml (25°), Vermouth 30ml (16°)
```

### Calcolo Alcolemia  
```
Cocktail: Negroni (21.33g alcol puro)
Persona: Uomo, 75kg, 180cm, 30 anni, stomaco vuoto

Risultati:
- TBW: 45.2 litri
- Alcolemia al picco: 0.47 g/L
- Stato: Entro i limiti (guida consentita)
- Azzeramento in: 3.1 ore
```

## Test Automatici

```bash
python test_tool.py
```

Include test per:
- Nuovo cocktail Te+
- Confronto Spritz classici vs veneziani  
- Simulazioni alcolemia uomo vs donna
- Verifica formula Widmark vs calcoli manuali

## Sicurezza e Responsabilità

**⚠️ AVVERTENZE IMPORTANTI:**
- I calcoli sono **teorici e approssimativi**
- L'alcolemia reale varia per fattori individuali
- **Mai guidare dopo aver bevuto** anche sotto i limiti
- **Usa sempre l'etilometro** per misure precise
- Il tool è per **scopi educativi** e prevenzione

## Formule e Precisione

### Vantaggi del Tool
- **Più preciso** delle tabelle standard (usa TBW personalizzato vs coefficienti fissi)
- **Considera l'età** (metabolismo rallenta con l'età)
- **Differenzia uomo/donna** (composizione corporea diversa)
- **Include altezza** (influenza distribuzione acqua corporea)
- **Correzione stomaco** (assorbimento ridotto a stomaco pieno)

### Limitazioni
- **Non sostituisce l'etilometro**
- **Non considera**: farmaci, malattie, tolleranza individuale
- **Basato su persona sana** con fegato funzionante
- **Margine di errore**: ±20-30% tipico per calcoli teorici

## Sviluppo Futuro

Possibili miglioramenti:
1. **Interfaccia web** per uso mobile
2. **Grafici** curva alcolemia nel tempo  
3. **Database espandibile** per nuovi cocktail
4. **Calcolo costi** ingredienti cocktail
5. **Integrazione calorie** per cocktail

## Struttura File

```
Gradiente alcolico/
├── database_ricette.csv      # Database 52 cocktail
├── gradazione_tool.py        # Tool principale con alcolemia
├── test_tool.py             # Test completi + alcolemia
├── requirements.txt         # Dipendenze
└── README.md               # Documentazione
```

## Changelog v2.0

### Nuove Funzionalità
- ✅ **Sistema alcolemia completo** con Formula Widmark + TBW
- ✅ **Te+ cocktail** di Origin Bassano del Grappa
- ✅ **Spritz corretti** (classici e veneziani)
- ✅ **Menu espanso** a 6 opzioni
- ✅ **Calcolo grammi alcol puro** per ogni cocktail
- ✅ **Limiti legali italiani** integrati
- ✅ **Test alcolemia** automatici

### Miglioramenti
- 🔄 **Database aggiornato**: da 51 a 52 cocktail
- 🔄 **Interface pulita**: rimossi tutti gli emoji
- 🔄 **Personalizzazione avanzata**: modifica anche tipi ingredienti
- 🔄 **Precisione aumentata**: TBW vs coefficienti fissi

---

**Bevi responsabilmente! Non guidare mai dopo aver bevuto alcol!**

*Tool sviluppato per educazione alla sicurezza stradale e consapevolezza del consumo di alcolici.*
