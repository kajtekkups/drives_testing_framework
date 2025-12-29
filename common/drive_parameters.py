#TODO: sprawdzić, czy można ustawić ograniczenia prędkości/torque
#TODO: Czym jest magnesowanie (str. 71)
#TODO: Ustalić czy nasz silnik sterowany jest za pomocą DTC
#TODO: Przemienniki w układzie nadrzędny-podrzędny
#TODO: Utrata komunikacji

#1.1 Zmierzona lub szacowana prędkość silnika w zależności - / real32 od używanego typu sprzężenia zwrotnego
#1.7 Prąd silnika
#1.10 Moment silnika
#1.14 moc wyjściowa przemiennika
#1.17 szacowana moc mechaniczna na wale silnika
#1.31 Zmierzona temperatura wpływającego powietrza chłodzącego. J
#1.72-1.74 prądy skuteczne faz
#1.104 Szacowany prąd czynny płynący przez moduł zasilający.
#1.106 Szacowany prąd bierny płynący przez moduł zasilający.


#5.4 Licznik czasu włącz. went.
#5.10 Temp. karty sterowania
#5.11 Szacowana temperatura przemiennika częstotliwości 
#5.111 Szacowana temperatura modułu zasilającego jako wartość procentowa limitu błędu

# 19 - tryby pracy
# 19.1 - Aktualny tryb pracy read (prędkością, moment, kombinacje, sterowanie skalarne,
# 19.11 -  wybór źródła zewnętrznego miejsca sterowania
# 19.12-19.16 - wybór trybu sterowania dla danego typu sterowania (upewnić się najpierw, jak będę sterował)
# 19.17 - blokada sterowania lokalnego

# 20 - Start/Stop/Kierunek - 
# 20.1 komendy Zew1 - ustawienie sterowania (start/stop/kierunek) dla źródła zewnętrznego 1:
        # Proponuje: 20.6 - wyłączone sterowanie zewnętrzne 2
        # [1] We1: start i sterowanie kierunkiem za pomocą znaku wartości zadanej
        # [2] We1:start;We2:kierunek 
# 20.2 Definiuje, czy sygnał startu dla zewnętrznego miejsca sterowania ZEW1 jest wyzwalany przez zbocze, czy poziom.(patrz docs i 20.1)
# 20.3 Ustawienie warości dla We1 (patrz 20.1)
# 20.4 Ustawienie warości dla We1 (patrz 20.1) (być może nie będzie potrzebne, gdy wybierzemy 1 opcje)
# 20.11 - Sygnał zatrzymania, gdy wyłączono sygnał zezwolenia na bieg (20.12)
# 20.12 - źródło zezwolenia na bieg
# 20.19 - zezwolenie na start (chyba nie potrzebne) 
# 20.23 - zezwoleni na dodatnią wartość zadaną (można wykożystać dla bezpieczeństwa na stanowisku testowym)
# 20.23 - zezwoleni na ujemną wartość zadaną (można wykożystać dla bezpieczeństwa na stanowisku testowym)
# 20.25 - bieg próbny (sprawdzić do czego służy)

# 21.1 Tryb startu (jeżeli silnik sterowany jest DTC) W przypadku silników zmagnesamitrwałymiisynchro
# nicznych silników reluktancyjnych należy użyć trybu
# startu Automatyczny!!!
# TODO: poczytać o rozruchu silnika
# 21.3 Tryb zatrzymania
# 21.4 Tryb zatrzymania awaryjnego
# 21.5 Żródło zatrzymania awaryjnego
# 21.6 Limit prędkości zerowej
# TODO 21.7-21.18 po przeczytaniu Czym jest magnesowanie (str. 71)
# 

# 22 - wybór wartości zadanej prędkości (Strona 695)
# 22.21 - funkcja stałej prędkości
# 22.22 - 22.24 Wybór, której stałej prędkości urzywać (jedna z 7)
# 22.51, 22.52 22.53 - ustawienia prędkości krytycznej


# 58 - Wbudowany modół komunikacyjny (zobaczyć pod którym jest opcua)





# 3 - wartości zadane
# 4 - błędy
# 6 - słowa strowania - może wykożystać je do uruchamiania i zatrzymywania testu?
# 7 - informacje systemowe - Można wykożystać do identyfikacji przetwornika/ sprawdzania, czy sterujemy dobrym przemiennikiem





# 23 - Rampa wartości zadanej prędkości
# 24 - Warunkowa wartość zadana prędkości
# 25 - Sterowawnie prędkością
# 26 - Ustawienia wartości zadanej momentu

# 28,29, 32, 36, 37, 40, 41, 43, 44, 45, 46, 60, 90, 95  - przeczytać

# 30 - Limity
# 32 - funkcje błędu
# 35 - ochrona termiczna
# 49 - port komunikacyjny
# 91, 92, 93 - modół enkodera
# 97, 98, 99  - ustawienia modelu silnika
# 200 - bezpieczeństwo
    
#TODO: dodać automatyczne wyłączanie silnika w przypadku utraty komunikacji?

#5.1 licznik czasu włąćzenia?
#5.2 Licznik czasu pracy



