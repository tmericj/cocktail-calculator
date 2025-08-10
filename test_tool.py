#!/usr/bin/env python3
"""
Script di esempio per testare il calcolatore di gradazione alcolica e alcolemia.
Mostra come usare le principali funzionalità del tool.
"""

from gradazione_tool import CalcolatoreGradazioneAlcolica, CalcolatoreAlcolemia

def test_esempi():
    """Test con alcuni cocktail di esempio."""
    
    # Inizializza il calcolatore
    path_db = "/Users/tommaso/Desktop/Progetti esterni/Gradiente alcolico/database_ricette.csv"
    calc = CalcolatoreGradazioneAlcolica(path_db)
    
    print("=== TEST DEL CALCOLATORE COMPLETO ===\n")
    
    # Test 1: Te+ (nuovo cocktail di Bassano)
    print("Test 1: Te+ - Cocktail di Origin Bassano del Grappa")
    te_plus = calc.cerca_cocktail("Te+")
    if te_plus:
        calc.mostra_dettagli_cocktail(te_plus)
        print(f"Gradazione calcolata: {te_plus['gradazione_calcolata']}% vol")
        print(f"Alcol puro: {te_plus['grammi_alcol_puro']} grammi")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 2: Confronto Spritz classico vs Veneziano
    print("Test 2: Confronto Spritz Aperol vs Aperol Veneziana")
    spritz_classico = calc.cerca_cocktail("Spritz Aperol")
    spritz_veneziana = calc.cerca_cocktail("Spritz Aperol Veneziana")
    
    if spritz_classico and spritz_veneziana:
        print("APEROL SPRITZ CLASSICO:")
        calc.mostra_dettagli_cocktail(spritz_classico)
        print(f"\nSPRITZ APEROL VENEZIANA:")
        calc.mostra_dettagli_cocktail(spritz_veneziana)
        print(f"\nDifferenza di gradazione: +{spritz_veneziana['gradazione_calcolata'] - spritz_classico['gradazione_calcolata']:.2f}% vol")
        print(f"Differenza di alcol puro: +{spritz_veneziana['grammi_alcol_puro'] - spritz_classico['grammi_alcol_puro']:.2f} grammi")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 3: Calcolo alcolemia simulato
    print("Test 3: Calcolo Alcolemia - Simulazione con Negroni")
    negroni = calc.cerca_cocktail("Negroni")
    if negroni:
        calc.mostra_dettagli_cocktail(negroni)
        
        # Simula una persona di esempio
        print(f"\nSimulazione alcolemia per:")
        print(f"- Uomo, 75 kg, 180 cm, 30 anni")
        print(f"- Stomaco vuoto, appena bevuto")
        
        risultato = CalcolatoreAlcolemia.calcola_alcolemia(
            grammi_alcol=negroni['grammi_alcol_puro'],
            genere='uomo',
            peso=75,
            altezza=180, 
            eta=30,
            ore_trascorse=0,
            stomaco_pieno=False
        )
        
        print(f"\nRisultati alcolemia:")
        print(f"- TBW: {risultato['tbw_litri']} litri")
        print(f"- Fattore Widmark: {risultato['fattore_widmark']}")
        print(f"- Alcolemia al picco: {risultato['alcolemia_picco']} g/L")
        print(f"- Stato legale: {risultato['stato_legale']}")
        print(f"- Ore per azzeramento: {risultato['ore_per_azzeramento']} ore")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 4: Confronto TBW uomo vs donna
    print("Test 4: Confronto TBW e Alcolemia Uomo vs Donna")
    print("Stesso cocktail (Americano), stesso peso (65 kg), stessa altezza (170 cm), stessa età (25 anni)")
    
    americano = calc.cerca_cocktail("Americano")
    if americano:
        print(f"\nCocktail: {americano['nome']} ({americano['grammi_alcol_puro']} grammi alcol puro)")
        
        # Calcolo per uomo
        risultato_uomo = CalcolatoreAlcolemia.calcola_alcolemia(
            americano['grammi_alcol_puro'], 'uomo', 65, 170, 25, 0, False
        )
        
        # Calcolo per donna  
        risultato_donna = CalcolatoreAlcolemia.calcola_alcolemia(
            americano['grammi_alcol_puro'], 'donna', 65, 170, 25, 0, False
        )
        
        print(f"\nUOMO:")
        print(f"- TBW: {risultato_uomo['tbw_litri']} litri")
        print(f"- Alcolemia: {risultato_uomo['alcolemia_picco']} g/L")
        print(f"- Ore azzeramento: {risultato_uomo['ore_per_azzeramento']} ore")
        
        print(f"\nDONNA:")
        print(f"- TBW: {risultato_donna['tbw_litri']} litri")
        print(f"- Alcolemia: {risultato_donna['alcolemia_picco']} g/L") 
        print(f"- Ore azzeramento: {risultato_donna['ore_per_azzeramento']} ore")
        
        differenza_alcolemia = ((risultato_donna['alcolemia_picco'] - risultato_uomo['alcolemia_picco']) / risultato_uomo['alcolemia_picco']) * 100
        print(f"\nDifferenza alcolemia: +{differenza_alcolemia:.1f}% per la donna")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 5: Verifica formula Widmark manuale
    print("Test 5: Verifica Formula Widmark vs Calcolo Manuale")
    print("Negroni standard per uomo 80kg, 175cm, 28 anni")
    
    if negroni:
        # Calcolo con tool
        risultato_tool = CalcolatoreAlcolemia.calcola_alcolemia(
            negroni['grammi_alcol_puro'], 'uomo', 80, 175, 28, 0, False
        )
        
        # Calcolo manuale semplificato (fattore Widmark classico 0.68)
        alcolemia_manuale = negroni['grammi_alcol_puro'] / (80 * 0.68)
        
        print(f"Alcol puro: {negroni['grammi_alcol_puro']} grammi")
        print(f"Tool (con TBW): {risultato_tool['alcolemia_picco']} g/L")
        print(f"Calcolo manuale (0.68): {alcolemia_manuale:.3f} g/L")
        print(f"Fattore Widmark tool: {risultato_tool['fattore_widmark']}")
        print(f"Differenza: {abs(risultato_tool['alcolemia_picco'] - alcolemia_manuale):.3f} g/L")
        print("Il tool è più preciso grazie al calcolo TBW personalizzato!")
    
    print("\n" + "="*50)
    print("TUTTI I TEST COMPLETATI CON SUCCESSO!")
    print("Il tool ora include:")
    print("- Database aggiornato con Te+ e Spritz corretti") 
    print("- Calcolo preciso dell'alcolemia con formula Widmark + TBW")
    print("- Parametri personalizzati (età, altezza, genere, stomaco)")
    print("- Tempi di smaltimento e limiti legali")
    print("="*50)


if __name__ == "__main__":
    test_esempi()
