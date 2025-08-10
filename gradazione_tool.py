import pandas as pd
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

class CalcolatoreAlcolemia:
    """Classe per calcolare l'alcolemia usando la formula di Widmark con TBW."""
    
    @staticmethod
    def calcola_tbw(peso: float, altezza: float, eta: int, genere: str) -> float:
        """
        Calcola il Total Body Water usando la formula di Watson.
        
        Args:
            peso: Peso in kg
            altezza: Altezza in cm  
            eta: Età in anni
            genere: 'uomo' o 'donna'
            
        Returns:
            TBW in litri
        """
        if genere.lower() in ['uomo', 'maschio', 'm']:
            # Formula Watson per uomini
            tbw = 2.447 - (0.09145 * eta) + (0.1074 * altezza) + (0.3362 * peso)
        else:
            # Formula Watson per donne  
            tbw = -2.097 + (0.1069 * altezza) + (0.2466 * peso)
        
        return max(tbw, 1.0)  # Evita valori negativi o troppo bassi
    
    @staticmethod
    def calcola_fattore_widmark(genere: str, peso: float, altezza: float, eta: int) -> float:
        """
        Calcola il fattore di Widmark corretto con TBW.
        
        Args:
            genere: 'uomo' o 'donna'
            peso: Peso in kg
            altezza: Altezza in cm
            eta: Età in anni
            
        Returns:
            Fattore di Widmark corretto
        """
        tbw = CalcolatoreAlcolemia.calcola_tbw(peso, altezza, eta, genere)
        return tbw / peso
    
    @staticmethod
    def calcola_alcolemia_singolo(grammi_alcol: float, genere: str, peso: float, 
                                 altezza: float, eta: int, minuti_trascorsi: int = 0,
                                 stomaco_pieno: bool = False) -> Dict:
        """
        Calcola l'alcolemia per un singolo drink.
        
        Args:
            grammi_alcol: Grammi di alcol puro ingeriti
            genere: 'uomo' o 'donna'
            peso: Peso in kg
            altezza: Altezza in cm  
            eta: Età in anni
            minuti_trascorsi: Minuti dalla assunzione
            stomaco_pieno: Se stomaco pieno (riduce assorbimento)
            
        Returns:
            Dizionario con risultati del calcolo
        """
        # Calcola il fattore di Widmark con TBW
        fattore_widmark = CalcolatoreAlcolemia.calcola_fattore_widmark(genere, peso, altezza, eta)
        
        # Tasso di eliminazione (g/L/ora) convertito in minuti
        if genere.lower() in ['uomo', 'maschio', 'm']:
            beta_per_minuto = 0.15 / 60  # 0.15 g/L/ora = 0.0025 g/L/min
        else:
            beta_per_minuto = 0.17 / 60  # 0.17 g/L/ora = 0.0028 g/L/min
        
        # Correzione per stomaco pieno (assorbimento ridotto del 30%)
        grammi_effettivi = grammi_alcol * (0.7 if stomaco_pieno else 1.0)
        
        # Formula di Widmark: Alcolemia = (Alcol / (Peso * Fattore_Widmark)) - (Beta * Tempo)
        alcolemia_iniziale = grammi_effettivi / (peso * fattore_widmark)
        alcolemia_attuale = max(0, alcolemia_iniziale - (beta_per_minuto * minuti_trascorsi))
        
        return {
            'alcolemia_picco': alcolemia_iniziale,
            'alcolemia_attuale': alcolemia_attuale,
            'grammi_alcol_effettivi': grammi_effettivi,
            'fattore_widmark': fattore_widmark,
            'beta_per_minuto': beta_per_minuto
        }
    
    @staticmethod
    def calcola_alcolemia_multipla(drinks_data: List[Dict], genere: str, peso: float, 
                                  altezza: float, eta: int, stomaco_pieno: bool = False) -> Dict:
        """
        Calcola l'alcolemia per drink multipli in un intervallo di tempo.
        
        Args:
            drinks_data: Lista di dict con {'nome': str, 'grammi_alcol': float, 'quantita': int}
            genere: 'uomo' o 'donna'
            peso: Peso in kg
            altezza: Altezza in cm
            eta: Età in anni
            stomaco_pieno: Se stomaco pieno durante tutta la sessione
            
        Returns:
            Dizionario con risultati del calcolo multiplo
        """
        # Calcola parametri base
        fattore_widmark = CalcolatoreAlcolemia.calcola_fattore_widmark(genere, peso, altezza, eta)
        tbw = CalcolatoreAlcolemia.calcola_tbw(peso, altezza, eta, genere)
        
        # Tasso di eliminazione per minuto
        if genere.lower() in ['uomo', 'maschio', 'm']:
            beta_per_minuto = 0.15 / 60
            beta_per_ora = 0.15
        else:
            beta_per_minuto = 0.17 / 60  
            beta_per_ora = 0.17
        
        # Calcola alcol totale da tutti i drink
        alcol_totale = 0
        dettaglio_drinks = []
        
        for drink in drinks_data:
            grammi_per_drink = drink['grammi_alcol']
            quantita = drink['quantita']
            alcol_drink = grammi_per_drink * quantita
            
            # Correzione stomaco pieno
            alcol_effettivo = alcol_drink * (0.7 if stomaco_pieno else 1.0)
            alcol_totale += alcol_effettivo
            
            dettaglio_drinks.append({
                'nome': drink['nome'],
                'quantita': quantita,
                'grammi_totali': alcol_drink,
                'grammi_effettivi': alcol_effettivo
            })
        
        # Calcola alcolemia totale al picco (senza smaltimento)
        alcolemia_picco = alcol_totale / (peso * fattore_widmark)
        
        # Funzione per calcolare alcolemia a qualsiasi momento
        def alcolemia_a_minuti(minuti_da_inizio):
            return max(0, alcolemia_picco - (beta_per_minuto * minuti_da_inizio))
        
        # Calcola quando tornerà sobrio (alcolemia = 0)
        minuti_azzeramento = int(alcolemia_picco / beta_per_minuto) if beta_per_minuto > 0 else 0
        
        # Calcola quando potrà guidare (alcolemia <= 0.5 g/L)
        limite_guida = 0.5
        if alcolemia_picco <= limite_guida:
            minuti_per_guidare = 0
        else:
            minuti_per_guidare = int((alcolemia_picco - limite_guida) / beta_per_minuto)
        
        return {
            'alcolemia_picco': round(alcolemia_picco, 3),
            'alcol_totale_grammi': round(alcol_totale, 1),
            'dettaglio_drinks': dettaglio_drinks,
            'fattore_widmark': round(fattore_widmark, 3),
            'tbw_litri': round(tbw, 1),
            'beta_per_ora': beta_per_ora,
            'minuti_azzeramento': minuti_azzeramento,
            'minuti_per_guidare': minuti_per_guidare,
            'ore_azzeramento': round(minuti_azzeramento / 60, 1),
            'ore_per_guidare': round(minuti_per_guidare / 60, 1),
            'funzione_alcolemia': alcolemia_a_minuti,
            'stato_legale_picco': CalcolatoreAlcolemia.get_stato_legale(alcolemia_picco)
        }
    
    @staticmethod  
    def calcola_alcolemia(grammi_alcol: float, genere: str, peso: float, 
                         altezza: float, eta: int, ore_trascorse: float = 0,
                         stomaco_pieno: bool = False) -> Dict:
        """
        Metodo di compatibilità per il test. Usa il sistema singolo ma con ore.
        """
        minuti_trascorsi = int(ore_trascorse * 60)
        result = CalcolatoreAlcolemia.calcola_alcolemia_singolo(
            grammi_alcol, genere, peso, altezza, eta, minuti_trascorsi, stomaco_pieno
        )
        
        tbw = CalcolatoreAlcolemia.calcola_tbw(peso, altezza, eta, genere)
        beta_per_ora = 0.15 if genere.lower() in ['uomo', 'maschio', 'm'] else 0.17
        
        # Calcola ore per azzeramento
        ore_azzeramento = result['alcolemia_picco'] / beta_per_ora if beta_per_ora > 0 else 0
        
        return {
            'alcolemia_picco': round(result['alcolemia_picco'], 3),
            'alcolemia_attuale': round(result['alcolemia_attuale'], 3),
            'fattore_widmark': round(result['fattore_widmark'], 3),
            'tbw_litri': round(tbw, 1),
            'ore_per_azzeramento': round(ore_azzeramento, 1),
            'stato_legale': CalcolatoreAlcolemia.get_stato_legale(result['alcolemia_attuale'])
        }
    
    @staticmethod
    def get_stato_legale(alcolemia: float) -> str:
        """Restituisce lo stato legale in base all'alcolemia."""
        if alcolemia == 0:
            return "Sobrio"
        elif alcolemia <= 0.5:
            return "Entro i limiti (guida consentita)"
        elif alcolemia <= 0.8:
            return "OLTRE I LIMITI - Sanzione amministrativa"
        elif alcolemia <= 1.5:
            return "OLTRE I LIMITI - Sanzione penale"
        else:
            return "OLTRE I LIMITI - Sanzione penale grave"


class CalcolatoreGradazioneAlcolica:
    def __init__(self, path_database: str):
        """
        Inizializza il calcolatore con il database delle ricette.
        
        Args:
            path_database: Percorso al file CSV con le ricette dei cocktail
        """
        self.path_database = path_database
        self.database = None
        self.carica_database()
    
    def carica_database(self):
        """Carica il database delle ricette dal file CSV."""
        try:
            if not os.path.exists(self.path_database):
                raise FileNotFoundError(f"Database non trovato: {self.path_database}")
            
            self.database = pd.read_csv(self.path_database)
            print(f"Database caricato con successo: {len(self.database)} cocktail disponibili")
            
        except Exception as e:
            print(f"Errore nel caricamento del database: {e}")
            self.database = None
    
    def calcola_gradazione_base(self, ingredienti: List[Tuple[str, float, float]]) -> float:
        """
        Calcola la gradazione alcolica finale usando la formula del volume pesato.
        
        Args:
            ingredienti: Lista di tuple (nome, volume_ml, gradazione_%vol)
            
        Returns:
            Gradazione finale del cocktail (% vol)
        """
        alcol_totale_ml = 0
        volume_totale_ml = 0
        
        for nome, volume_ml, gradazione in ingredienti:
            if pd.isna(volume_ml) or pd.isna(gradazione):
                continue
            
            alcol_puro = volume_ml * (gradazione / 100)
            alcol_totale_ml += alcol_puro
            volume_totale_ml += volume_ml
        
        if volume_totale_ml == 0:
            return 0.0
            
        gradazione_finale = (alcol_totale_ml / volume_totale_ml) * 100
        return round(gradazione_finale, 2)
    
    def calcola_grammi_alcol_puro(self, ingredienti: List[Tuple[str, float, float]]) -> float:
        """
        Calcola i grammi di alcol puro nel cocktail.
        
        Args:
            ingredienti: Lista di tuple (nome, volume_ml, gradazione_%vol)
            
        Returns:
            Grammi di alcol puro (peso specifico etanolo = 0.789 g/ml)
        """
        alcol_totale_ml = 0
        
        for nome, volume_ml, gradazione in ingredienti:
            if pd.isna(volume_ml) or pd.isna(gradazione):
                continue
            
            alcol_puro_ml = volume_ml * (gradazione / 100)
            alcol_totale_ml += alcol_puro_ml
        
        # Peso specifico dell'etanolo = 0.789 g/ml
        grammi_alcol = alcol_totale_ml * 0.789
        return round(grammi_alcol, 2)
    
    def estrai_ingredienti_da_riga(self, riga) -> List[Tuple[str, float, float]]:
        """Estrae gli ingredienti da una riga del database."""
        ingredienti = []
        
        for i in range(1, 6):  # ingrediente_1 a ingrediente_5
            nome_col = f'ingrediente_{i}'
            ml_col = f'ml_{i}'
            grad_col = f'gradazione_{i}'
            
            if (nome_col in riga and 
                not pd.isna(riga[nome_col]) and 
                riga[nome_col] != ''):
                
                nome = riga[nome_col]
                volume = riga[ml_col] if not pd.isna(riga[ml_col]) else 0
                gradazione = riga[grad_col] if not pd.isna(riga[grad_col]) else 0
                
                ingredienti.append((nome, volume, gradazione))
        
        return ingredienti
    
    def cerca_cocktail(self, nome_cocktail: str) -> Optional[Dict]:
        """
        Cerca un cocktail nel database per nome (case-insensitive).
        
        Args:
            nome_cocktail: Nome del cocktail da cercare
            
        Returns:
            Dizionario con informazioni del cocktail o None se non trovato
        """
        if self.database is None:
            return None
        
        # Ricerca case-insensitive
        mask = self.database['nome_cocktail'].str.lower() == nome_cocktail.lower()
        risultati = self.database[mask]
        
        if len(risultati) == 0:
            return None
        
        riga = risultati.iloc[0]
        ingredienti = self.estrai_ingredienti_da_riga(riga)
        gradazione = self.calcola_gradazione_base(ingredienti)
        grammi_alcol = self.calcola_grammi_alcol_puro(ingredienti)
        
        return {
            'nome': riga['nome_cocktail'],
            'categoria': riga['categoria'],
            'ingredienti': ingredienti,
            'gradazione_calcolata': gradazione,
            'grammi_alcol_puro': grammi_alcol,
            'bicchiere_ml': riga['bicchiere_standard_ml'] if not pd.isna(riga['bicchiere_standard_ml']) else 'N/A',
            'note': riga['note'] if not pd.isna(riga['note']) else 'N/A'
        }
    
    def calcola_cocktail_personalizzato(self, 
                                      nome_base: str,
                                      modifiche: Dict[str, Dict] = None,
                                      ingredienti_extra: List[Tuple[str, float, float]] = None) -> Optional[Dict]:
        """
        Calcola la gradazione di un cocktail con modifiche personalizzate.
        
        Args:
            nome_base: Nome del cocktail base
            modifiche: Dizionario con modifiche agli ingredienti {indice: {'nome': str, 'volume': float, 'gradazione': float}}
            ingredienti_extra: Lista di ingredienti aggiuntivi
            
        Returns:
            Dizionario con il cocktail modificato
        """
        cocktail_base = self.cerca_cocktail(nome_base)
        if not cocktail_base:
            return None
        
        ingredienti_modificati = list(cocktail_base['ingredienti'])
        
        # Applica modifiche agli ingredienti
        if modifiche:
            for indice, nuovi_valori in modifiche.items():
                if 0 <= indice < len(ingredienti_modificati):
                    old_nome, old_volume, old_grad = ingredienti_modificati[indice]
                    nuovo_nome = nuovi_valori.get('nome', old_nome)
                    nuovo_volume = nuovi_valori.get('volume', old_volume)
                    nuova_gradazione = nuovi_valori.get('gradazione', old_grad)
                    ingredienti_modificati[indice] = (nuovo_nome, nuovo_volume, nuova_gradazione)
        
        # Aggiungi ingredienti extra
        if ingredienti_extra:
            ingredienti_modificati.extend(ingredienti_extra)
        
        nuova_gradazione = self.calcola_gradazione_base(ingredienti_modificati)
        grammi_alcol = self.calcola_grammi_alcol_puro(ingredienti_modificati)
        
        return {
            'nome': f"{cocktail_base['nome']} (Personalizzato)",
            'categoria': cocktail_base['categoria'],
            'ingredienti': ingredienti_modificati,
            'gradazione_calcolata': nuova_gradazione,
            'grammi_alcol_puro': grammi_alcol,
            'bicchiere_ml': cocktail_base['bicchiere_ml'],
            'note': f"{cocktail_base['note']} - Versione personalizzata"
        }
    
    def mostra_cocktail_disponibili(self) -> List[str]:
        """Restituisce la lista dei cocktail disponibili nel database."""
        if self.database is None:
            return []
        
        return sorted(self.database['nome_cocktail'].tolist())
    
    def cerca_per_categoria(self, categoria: str) -> List[str]:
        """Restituisce tutti i cocktail di una categoria specifica."""
        if self.database is None:
            return []
        
        mask = self.database['categoria'].str.lower() == categoria.lower()
        return sorted(self.database[mask]['nome_cocktail'].tolist())
    
    def mostra_dettagli_cocktail(self, info_cocktail: Dict):
        """Stampa in modo elegante i dettagli di un cocktail."""
        print(f"\n{info_cocktail['nome']}")
        print(f"Categoria: {info_cocktail['categoria']}")
        print(f"Bicchiere: {info_cocktail['bicchiere_ml']} ml")
        print(f"Gradazione Alcolica: {info_cocktail['gradazione_calcolata']}% vol")
        print(f"Alcol Puro: {info_cocktail['grammi_alcol_puro']} grammi")
        print(f"\nIngredienti:")
        
        for nome, volume, gradazione in info_cocktail['ingredienti']:
            if gradazione > 0:
                print(f"   • {nome}: {volume} ml ({gradazione}% vol)")
            else:
                print(f"   • {nome}: {volume} ml (analcolico)")
        
        if info_cocktail['note'] != 'N/A':
            print(f"\nNote: {info_cocktail['note']}")


def gestisci_calcolo_alcolemia_multipla(calc: CalcolatoreGradazioneAlcolica):
    """Gestisce il calcolo dell'alcolemia per drink multipli."""
    print(f"\n=== CALCOLO ALCOLEMIA PER DRINK MULTIPLI ===")
    print("Calcola l'alcolemia per una serata con più drink!")
    
    try:
        # Raccolta dati personali
        print("\nInserisci i tuoi dati personali:")
        while True:
            genere = input("Genere (uomo/donna): ").strip().lower()
            if genere in ['uomo', 'donna', 'maschio', 'femmina', 'm', 'f']:
                break
            print("Inserisci 'uomo' o 'donna'")
        
        peso = float(input("Peso (kg): "))
        altezza = float(input("Altezza (cm): "))
        eta = int(input("Età (anni): "))
        
        print("\nCondizioni stomaco durante la serata:")
        print("1. Stomaco vuoto (digiuno)")
        print("2. Stomaco pieno (hai mangiato)")
        stomaco_scelta = input("Scegli (1/2): ").strip()
        stomaco_pieno = stomaco_scelta == "2"
        
        # Raccolta drink
        print(f"\n=== INSERIMENTO DRINK ===")
        print("Inserisci tutti i drink che hai bevuto (anche più dello stesso tipo)")
        print("L'ORDINE NON È IMPORTANTE - conta solo il totale!")
        
        drinks_data = []
        
        while True:
            nome_drink = input(f"\nNome cocktail {len(drinks_data)+1} (ENTER per finire): ").strip()
            if not nome_drink:
                break
            
            # Cerca il cocktail nel database
            info_cocktail = calc.cerca_cocktail(nome_drink)
            if not info_cocktail:
                print(f"Cocktail '{nome_drink}' non trovato! Riprova.")
                continue
            
            if info_cocktail['grammi_alcol_puro'] == 0:
                print(f"'{nome_drink}' è analcolico, non influenza l'alcolemia.")
                continue
            
            print(f"Trovato: {info_cocktail['nome']} ({info_cocktail['grammi_alcol_puro']}g alcol puro)")
            
            try:
                quantita = int(input(f"Quanti {info_cocktail['nome']} hai bevuto? "))
                if quantita <= 0:
                    print("Quantità deve essere positiva!")
                    continue
                
                drinks_data.append({
                    'nome': info_cocktail['nome'],
                    'grammi_alcol': info_cocktail['grammi_alcol_puro'],
                    'quantita': quantita
                })
                
                print(f"Aggiunto: {quantita}x {info_cocktail['nome']}")
                
            except ValueError:
                print("Inserisci un numero valido!")
        
        if not drinks_data:
            print("Nessun drink inserito!")
            return
        
        # Mostra riepilogo drink
        print(f"\n=== RIEPILOGO DRINK ===")
        for i, drink in enumerate(drinks_data, 1):
            alcol_totale = drink['grammi_alcol'] * drink['quantita']
            print(f"{i}. {drink['quantita']}x {drink['nome']} = {alcol_totale:.1f}g alcol")
        
        # Gestione tempo
        print(f"\n=== TIMING ===")
        print("In quanto tempo hai bevuto tutti questi drink?")
        durata_minuti = int(input("Durata totale in minuti (es: 120 per 2 ore): "))
        
        print("\nQuando hai bevuto il PRIMO drink?")
        minuti_primo = int(input("Minuti fa (es: 180 per 3 ore fa): "))
        
        # Calcolo alcolemia
        risultato = CalcolatoreAlcolemia.calcola_alcolemia_multipla(
            drinks_data, genere, peso, altezza, eta, stomaco_pieno
        )
        
        # Mostra risultati dettagliati
        print(f"\n" + "="*60)
        print(f"=== RISULTATI ALCOLEMIA MULTIPLA ===")
        print(f"="*60)
        
        print(f"\nDATI PERSONALI:")
        print(f"- TBW (Total Body Water): {risultato['tbw_litri']} litri")
        print(f"- Fattore Widmark: {risultato['fattore_widmark']}")
        print(f"- Tasso eliminazione: {risultato['beta_per_ora']} g/L/ora")
        
        print(f"\nDRINK CONSUMATI:")
        for drink in risultato['dettaglio_drinks']:
            print(f"- {drink['quantita']}x {drink['nome']}: {drink['grammi_effettivi']:.1f}g alcol effettivo")
        
        print(f"\nALCOL TOTALE: {risultato['alcol_totale_grammi']} grammi")
        if stomaco_pieno:
            print(f"(Ridotto del 30% per stomaco pieno)")
        
        # Calcola alcolemia attuale considerando il tempo
        minuti_da_fine = minuti_primo - durata_minuti
        alcolemia_attuale = risultato['funzione_alcolemia'](minuti_primo)
        alcolemia_fine_bevute = risultato['funzione_alcolemia'](minuti_da_fine)
        
        print(f"\nALCOLEMIA:")
        print(f"- Al picco (fine bevute): {risultato['alcolemia_picco']} g/L")
        print(f"- Attuale (ora): {alcolemia_attuale:.3f} g/L")
        print(f"- Stato legale: {CalcolatoreAlcolemia.get_stato_legale(alcolemia_attuale)}")
        
        # Tempi di smaltimento
        print(f"\nTEMPI DI SMALTIMENTO:")
        if alcolemia_attuale > 0:
            minuti_rimanenti_azzeramento = max(0, risultato['minuti_azzeramento'] - minuti_primo)
            minuti_rimanenti_guida = max(0, risultato['minuti_per_guidare'] - minuti_primo)
            
            if minuti_rimanenti_azzeramento > 0:
                ore_azz = minuti_rimanenti_azzeramento // 60
                min_azz = minuti_rimanenti_azzeramento % 60
                print(f"- Azzeramento completo: {ore_azz}h {min_azz}min")
            else:
                print(f"- Azzeramento completo: GIÀ SOBRIO")
            
            if minuti_rimanenti_guida > 0:
                ore_guida = minuti_rimanenti_guida // 60
                min_guida = minuti_rimanenti_guida % 60
                print(f"- Per guidare legalmente: {ore_guida}h {min_guida}min")
            else:
                print(f"- Per guidare legalmente: GIÀ POSSIBILE")
        else:
            print(f"- Sei già completamente sobrio!")
        
        # Simulazione timeline
        print(f"\n=== TIMELINE ALCOLEMIA ===")
        print("Evoluzione alcolemia nelle prossime ore:")
        
        for ore in [0, 1, 2, 3, 4, 6]:
            minuti_futuro = minuti_primo + (ore * 60)
            alcolemia_futura = risultato['funzione_alcolemia'](minuti_futuro)
            stato = CalcolatoreAlcolemia.get_stato_legale(alcolemia_futura)
            
            if alcolemia_futura > 0:
                print(f"- Tra {ore}h: {alcolemia_futura:.3f} g/L ({stato})")
            else:
                print(f"- Tra {ore}h: 0.000 g/L (Sobrio)")
                break
        
        print(f"\n" + "="*60)
        print(f"LIMITI LEGALI ITALIANI:")
        print(f"0.0-0.5 g/L: Guida OK | 0.5-0.8: Multa | 0.8-1.5: Penale | >1.5: Penale grave")
        print(f"="*60)
        
        print(f"\nATTENZIONE: Calcolo teorico! Usa sempre l'etilometro!")
        
    except ValueError:
        print("Errore: inserisci valori numerici validi")
    except Exception as e:
        print(f"Errore nel calcolo: {e}")


def gestisci_calcolo_alcolemia_singolo(info_cocktail: Dict):
    """Gestisce il calcolo dell'alcolemia per un singolo cocktail."""
    print(f"\n=== CALCOLO ALCOLEMIA PER {info_cocktail['nome'].upper()} ===")
    print("Per calcolare l'alcolemia in modo preciso, inserisci i tuoi dati:")
    
    try:
        # Raccolta dati personali
        while True:
            genere = input("Genere (uomo/donna): ").strip().lower()
            if genere in ['uomo', 'donna', 'maschio', 'femmina', 'm', 'f']:
                break
            print("Inserisci 'uomo' o 'donna'")
        
        peso = float(input("Peso (kg): "))
        altezza = float(input("Altezza (cm): "))
        eta = int(input("Età (anni): "))
        
        print("\nStomaco:")
        print("1. Vuoto (digiuno da almeno 3 ore)")
        print("2. Pieno (hai mangiato di recente)")
        stomaco_scelta = input("Scegli (1/2): ").strip()
        stomaco_pieno = stomaco_scelta == "2"
        
        minuti_trascorsi = int(input("Minuti trascorsi dall'assunzione (0 se lo bevi ora): ") or "0")
        
        # Usa il sistema per drink multipli con 1 solo drink
        drinks_data = [{
            'nome': info_cocktail['nome'],
            'grammi_alcol': info_cocktail['grammi_alcol_puro'],
            'quantita': 1
        }]
        
        risultato = CalcolatoreAlcolemia.calcola_alcolemia_multipla(
            drinks_data, genere, peso, altezza, eta, stomaco_pieno
        )
        
        # Calcola alcolemia attuale considerando il tempo trascorso
        alcolemia_attuale = risultato['funzione_alcolemia'](minuti_trascorsi)
        
        # Mostra risultati
        print(f"\n=== RISULTATI ALCOLEMIA ===")
        print(f"Alcol puro nel drink: {risultato['alcol_totale_grammi']} grammi")
        print(f"TBW (Total Body Water): {risultato['tbw_litri']} litri")
        print(f"Fattore Widmark: {risultato['fattore_widmark']}")
        print(f"\nAlcolemia al picco: {risultato['alcolemia_picco']} g/L")
        print(f"Alcolemia attuale: {alcolemia_attuale:.3f} g/L")
        print(f"Stato legale: {CalcolatoreAlcolemia.get_stato_legale(alcolemia_attuale)}")
        
        if alcolemia_attuale > 0:
            minuti_rimanenti_azzeramento = max(0, risultato['minuti_azzeramento'] - minuti_trascorsi)
            minuti_rimanenti_guida = max(0, risultato['minuti_per_guidare'] - minuti_trascorsi)
            
            if minuti_rimanenti_azzeramento > 0:
                ore_azz = minuti_rimanenti_azzeramento // 60
                min_azz = minuti_rimanenti_azzeramento % 60
                print(f"\nTempo per azzeramento completo: {ore_azz}h {min_azz}min")
            else:
                print(f"\nSei già completamente sobrio!")
            
            if minuti_rimanenti_guida > 0:
                ore_guida = minuti_rimanenti_guida // 60
                min_guida = minuti_rimanenti_guida % 60
                print(f"Tempo per guidare legalmente: {ore_guida}h {min_guida}min")
            else:
                print(f"Puoi già guidare legalmente (sotto 0.5 g/L)")
        
        print(f"\n=== LIMITI LEGALI ITALIANI ===")
        print(f"0.0 - 0.5 g/L: Guida consentita")
        print(f"0.5 - 0.8 g/L: Multa 527-2108€, sospensione patente 3-6 mesi")
        print(f"0.8 - 1.5 g/L: Arresto fino a 6 mesi, multa 800-3200€")
        print(f"Oltre 1.5 g/L: Arresto 6 mesi-1 anno, confisca veicolo")
        
        print(f"\nATTENZIONE: Questo è un calcolo teorico!")
        print(f"L'alcolemia reale può variare per fattori individuali.")
        print(f"In caso di dubbi, usa sempre l'etilometro!")
        
    except ValueError:
        print("Errore: inserisci valori numerici validi")
    except Exception as e:
        print(f"Errore nel calcolo: {e}")


def main():
    """Interfaccia principale del tool."""
    print("=== CALCOLATORE GRADAZIONE ALCOLICA E ALCOLEMIA ===")
    print("Tool completo per cocktail e sicurezza stradale con drink multipli\n")
    
    # Percorso al database - Modifica questo percorso se necessario
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path_db = os.path.join(script_dir, "database_ricette.csv")
    
    # Inizializza il calcolatore
    calc = CalcolatoreGradazioneAlcolica(path_db)
    
    if calc.database is None:
        print("Impossibile continuare senza il database. Controlla il percorso del file.")
        return
    
    while True:
        print("\n" + "="*70)
        print("MENU PRINCIPALE:")
        print("1. Cerca un cocktail per nome")
        print("2. Mostra tutti i cocktail disponibili")
        print("3. Cerca per categoria")
        print("4. Calcola cocktail personalizzato")
        print("5. Calcola alcolemia per cocktail singolo")
        print("6. Calcola alcolemia per drink multipli (NOVITÀ!)")
        print("7. Esci")
        print("="*70)
        
        scelta = input("\nScegli un'opzione (1-7): ").strip()
        
        if scelta == "1":
            nome = input("\nInserisci il nome del cocktail: ").strip()
            
            if not nome:
                print("Nome non valido!")
                continue
            
            info = calc.cerca_cocktail(nome)
            if info:
                calc.mostra_dettagli_cocktail(info)
                
                # Opzione per calcolare alcolemia
                if info['grammi_alcol_puro'] > 0:
                    calcola_alc = input("\nVuoi calcolare l'alcolemia? (s/n): ").strip().lower()
                    if calcola_alc.startswith('s'):
                        gestisci_calcolo_alcolemia_singolo(info)
            else:
                print(f"Cocktail '{nome}' non trovato!")
                print("Usa l'opzione 2 per vedere tutti i cocktail disponibili")
        
        elif scelta == "2":
            cocktail_list = calc.mostra_cocktail_disponibili()
            print(f"\nCocktail disponibili ({len(cocktail_list)}):")
            for i, cocktail in enumerate(cocktail_list, 1):
                print(f"{i:2d}. {cocktail}")
        
        elif scelta == "3":
            print("\nCategorie disponibili:")
            categorie = sorted(calc.database['categoria'].unique())
            for i, cat in enumerate(categorie, 1):
                print(f"{i}. {cat}")
            
            try:
                scelta_cat = int(input("\nScegli una categoria (numero): ")) - 1
                if 0 <= scelta_cat < len(categorie):
                    categoria = categorie[scelta_cat]
                    cocktail_cat = calc.cerca_per_categoria(categoria)
                    print(f"\nCocktail in '{categoria}':")
                    for cocktail in cocktail_cat:
                        print(f"   • {cocktail}")
                else:
                    print("Scelta non valida!")
            except ValueError:
                print("Inserisci un numero valido!")
        
        elif scelta == "4":
            nome_base = input("\nNome del cocktail base: ").strip()
            cocktail_base = calc.cerca_cocktail(nome_base)
            
            if not cocktail_base:
                print(f"Cocktail base '{nome_base}' non trovato!")
                continue
            
            print(f"\nCocktail base trovato: {cocktail_base['nome']}")
            print("Ingredienti attuali:")
            for i, (nome, volume, grad) in enumerate(cocktail_base['ingredienti']):
                print(f"   {i+1}. {nome}: {volume} ml ({grad}% vol)")
            
            print("\nVuoi modificare gli ingredienti? (s/n)")
            if input().lower().startswith('s'):
                modifiche = {}
                
                for i, (nome, volume, grad) in enumerate(cocktail_base['ingredienti']):
                    print(f"\nIngrediente {i+1}: {nome} ({volume} ml, {grad}% vol)")
                    
                    # Modifica nome ingrediente
                    nuovo_nome = input(f"Nuovo ingrediente (ENTER per mantenere '{nome}'): ").strip()
                    if not nuovo_nome:
                        nuovo_nome = nome
                    
                    # Modifica volume
                    nuovo_volume_str = input(f"Nuovo volume (ENTER per mantenere {volume} ml): ").strip()
                    try:
                        nuovo_volume = float(nuovo_volume_str) if nuovo_volume_str else volume
                    except ValueError:
                        print(f"Volume non valido, mantengo {volume} ml")
                        nuovo_volume = volume
                    
                    # Modifica gradazione
                    nuova_grad_str = input(f"Nuova gradazione (ENTER per mantenere {grad}% vol): ").strip()
                    try:
                        nuova_grad = float(nuova_grad_str) if nuova_grad_str else grad
                    except ValueError:
                        print(f"Gradazione non valida, mantengo {grad}% vol")
                        nuova_grad = grad
                    
                    # Salva modifiche se ci sono stati cambiamenti
                    if nuovo_nome != nome or nuovo_volume != volume or nuova_grad != grad:
                        modifiche[i] = {
                            'nome': nuovo_nome,
                            'volume': nuovo_volume,
                            'gradazione': nuova_grad
                        }
                
                # Aggiungi ingredienti extra
                print("\nVuoi aggiungere ingredienti extra? (s/n)")
                ingredienti_extra = []
                if input().lower().startswith('s'):
                    while True:
                        nome_extra = input("Nome ingrediente extra (ENTER per finire): ").strip()
                        if not nome_extra:
                            break
                        
                        try:
                            volume_extra = float(input("Volume (ml): "))
                            grad_extra = float(input("Gradazione (% vol): "))
                            ingredienti_extra.append((nome_extra, volume_extra, grad_extra))
                        except ValueError:
                            print("Valori non validi, ingrediente non aggiunto.")
                
                info_personalizzato = calc.calcola_cocktail_personalizzato(
                    nome_base, 
                    modifiche if modifiche else None,
                    ingredienti_extra if ingredienti_extra else None
                )
                if info_personalizzato:
                    calc.mostra_dettagli_cocktail(info_personalizzato)
                    
                    # Opzione per calcolare alcolemia
                    if info_personalizzato['grammi_alcol_puro'] > 0:
                        calcola_alc = input("\nVuoi calcolare l'alcolemia? (s/n): ").strip().lower()
                        if calcola_alc.startswith('s'):
                            gestisci_calcolo_alcolemia_singolo(info_personalizzato)
            else:
                calc.mostra_dettagli_cocktail(cocktail_base)
        
        elif scelta == "5":
            nome = input("\nInserisci il nome del cocktail per calcolare l'alcolemia: ").strip()
            
            if not nome:
                print("Nome non valido!")
                continue
            
            info = calc.cerca_cocktail(nome)
            if info:
                if info['grammi_alcol_puro'] > 0:
                    calc.mostra_dettagli_cocktail(info)
                    gestisci_calcolo_alcolemia_singolo(info)
                else:
                    print(f"'{info['nome']}' è analcolico, non calcolo alcolemia necessario.")
            else:
                print(f"Cocktail '{nome}' non trovato!")
        
        elif scelta == "6":
            gestisci_calcolo_alcolemia_multipla(calc)
        
        elif scelta == "7":
            print("\nGrazie per aver usato il Calcolatore di Gradazione Alcolica e Alcolemia!")
            print("Bevi responsabilmente e non guidare mai sotto l'effetto dell'alcol!")
            break
        
        else:
            print("Opzione non valida. Scegli tra 1-7.")


if __name__ == "__main__":
    main()

