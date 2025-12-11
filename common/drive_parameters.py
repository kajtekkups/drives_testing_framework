#TODO: sprawdzić, czy można ustawić ograniczenia prędkości/torque

#1.1 Zmierzona lub szacowana prędkość silnika w zależności - / real32 od używanego typu sprzężenia zwrotnego

#1.7 Prąd silnika
#1.10 Moment silnika
#1.14 moc wyjściowa przemiennika
#1.17 szacowana moc mechaniczna na wale silnika
#1.31 Zmierzona temperatura wpływającego powietrza chłodzącego. J
#1.72-1.74 prądy skuteczne faz
#1.104 Szacowany prąd czynny płynący przez moduł zasilający.
#1.106 Szacowany prąd bierny płynący przez moduł zasilający.

# 3 - wartości zadane
# 4 - błędy
# 6 - słowa strowania - może wykożystać je do uruchamiania i zatrzymywania testu?
# 7 - informacje systemowe - Można wykożystać do identyfikacji przetwornika/ sprawdzania, czy sterujemy dobrym przemiennikiem


# 19 - tryby pracy
# 20 - Start/Stop/Kierunek
# 22 - wybór wartości zadanej prędkości
# 23 - Rampa wartości zadanej prędkości
# 24 - Warunkowa wartość zadana prędkości
# 25 - Sterowawnie prędkością
# 26 - Ustawienia wartości zadanej momentu

# 28,29, 32, 36, 37, 40, 41, 43, 44, 45, 46, 60, 90, 95  - przeczytać

# 30 - Limity
# 32 - funkcje błędu
# 35 - ochrona termiczna
# 49 - port komunikacyjny
# 58 - Wbudowany modół komunikacyjny
# 91, 92, 93 - modół enkodera
# 97, 98, 99  - ustawienia modelu silnika
# 200 - bezpieczeństwo
    
#TODO: dodać automatyczne wyłączanie silnika w przypadku utraty komunikacji?

#5.1 licznik czasu włąćzenia?
#5.2 Licznik czasu pracy


# Interesting data:
#5.4 Licznik czasu włącz. went.
#5.10 Temp. karty sterowania
#5.11 Szacowana temperatura przemiennika częstotliwości 
#5.111 Szacowana temperatura modułu zasilającego jako wartość procentowa limitu błędu
