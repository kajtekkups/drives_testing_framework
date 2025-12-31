#TODO: sprawdzić, czy można ustawić ograniczenia prędkości/torque
#TODO: Czym jest magnesowanie (str. 71)
#TODO: Ustalić czy nasz silnik sterowany jest za pomocą DTC
#TODO: Przemienniki w układzie nadrzędny-podrzędny
#TODO: Utrata komunikacji
NS = "ns=8"
SET_SPEED_NODE_ID =            f"{NS};i=1703958" # 022 Speed reference selection -> 026 Constant speed 1


#1.1 Zmierzona lub szacowana prędkość silnika w zależności - / real32 od używanego typu sprzężenia zwrotnego
ESTIMATED_SPEED_NODE_ID =      f"{NS};i=131073"  # 001 Actual values -> Motor speed estimated

#1.7 Prąd silnika
MOTOR_CURRENT = f"{NS};i=458753"
#1.10 Moment silnika
#1.14 moc wyjściowa przemiennika
#1.17 szacowana moc mechaniczna na wale silnika
#1.31 Zmierzona temperatura wpływającego powietrza chłodzącego. J
#1.72-1.74 prądy skuteczne faz
#1.104 Szacowany prąd czynny płynący przez moduł zasilający.
#1.106 Szacowany prąd bierny płynący przez moduł zasilający.

# parameter 1.001
MOTOR_SPEED_USED = f"{NS};i=65537"
# parameter 1.002
MOTOR_SPEED_ESTIMATED = f"{NS};i=131073"
# parameter 1.004
ENCODER_1_SPEED_FILTERED = f"{NS};i=262145"
# parameter 1.005
ENCODER_2_SPEED_FILTERED = f"{NS};i=327681"
# parameter 1.003
MOTOR_SPEED_PERCENT = f"{NS};i=196609"
# parameter 1.007
MOTOR_CURRENT = f"{NS};i=458753"
# parameter 1.006
OUTPUT_FREQUENCY = f"{NS};i=393217"
# parameter 1.008
MOTOR_CURRENT_PERCENT_OF_MOTOR_NOM = f"{NS};i=524289"
# parameter 1.010
MOTOR_TORQUE = f"{NS};i=655361"
# parameter 1.013
OUTPUT_VOLTAGE = f"{NS};i=851969"
# parameter 1.011
DC_VOLTAGE = f"{NS};i=720897"
# parameter 1.014
OUTPUT_POWER = f"{NS};i=917505"
# parameter 1.015
OUTPUT_POWER_PERCENT_OF_MOTOR_NOM = f"{NS};i=983041"
# parameter 1.020
MOTOR_SHAFT_POWER = f"{NS};i=1314113"
# parameter 1.021
U_PHASE_CURRENT = f"{NS};i=1376257"
# parameter 1.022
V_PHASE_CURRENT = f"{NS};i=1441793"
# parameter 1.023
W_PHASE_CURRENT = f"{NS};i=1507329"
# parameter 1.029
SPEED_CHANGE_RATE = f"{NS};i=1900545"
# parameter 1.030
NOMINAL_TORQUE_SCALE = f"{NS};i=1966081"
# parameter 1.031
AMBIENT_TEMPERATURE = f"{NS};i=2031617"
# parameter 1.080
BACK_EMF_VOLTAGE = f"{NS};i=5242881"
# parameter 1.102
LINE_CURRENT = f"{NS};i=6684673"



# parameter 5.004
MAIN_FAN_ON_TIME_COUNTER = f"{NS};i=262149"
# parameter 5.002
RUN_TIME_COUNTER = f"{NS};i=131077"
# parameter 5.010
CONTROL_BOARD_TEMPERATURE = f"{NS};i=655365"
# parameter 5.011
INVERTER_TEMPERATURE = f"{NS};i=720901"
# parameter 5.012
IGBT_PHASE_U_TEMPERATURE = f"{NS};i=786437"
# parameter 5.014
IGBT_PHASE_W_TEMPERATURE = f"{NS};i=917509"
# parameter 5.013
IGBT_PHASE_V_TEMPERATURE = f"{NS};i=851973"
# parameter 5.015
INT_BOARD_TEMPERATURE = f"{NS};i=983045"
# parameter 5.018
CONTROL_BOARD_HUMIDITY = f"{NS};i=1179653"
# parameter 5.048
CONTROL_BOARD_TEMPERATURE_WARNING = f"{NS};i=3145733"
# parameter 5.050
IGBT_MAXIMUM_TEMPERATURE = f"{NS};i=3276805"
# parameter 5.066
PU_POWER_SUPPLY_TEMPERATURE = f"{NS};i=4325381"
# parameter 5.143
FLASH_MEMORY_USED_LIFETIME = f"{NS};i=9371653"
# parameter 5.201
MAXIMUM_MODULE_EARTH_CURRENT = f"{NS};i=13172741"
# parameter 5.032
FAN_ON_TIME_COUNTER_SECONDS = f"{NS};i=2097157"
# parameter 5.031
RUN_TIME_COUNTER_SECONDS = f"{NS};i=2031621"
# parameter 5.030
ON_TIME_COUNTER_SECONDS =f"{NS};i=1966085"



# 19 - tryby pracy
# 19.1 - Aktualny tryb pracy read (prędkością, moment, kombinacje, sterowanie skalarne,
# 19.11 -  wybór źródła zewnętrznego miejsca sterowania
# 19.12-19.16 - wybór trybu sterowania dla danego typu sterowania (upewnić się najpierw, jak będę sterował)
# 19.17 - blokada sterowania lokalnego

# parameter 19.001 
ACTUAL_OPERATION_MODE = f"{NS};i=65555"
# parameter 19.011 
EXT1_EXT2_SELECTION = f"{NS};i=720915"
# parameter 19.012 
EXT1_CONTROL_MODE = f"{NS};i=786451"
# parameter 19.014 
EXT2_CONTROL_MODE = f"{NS};i=917523"
# parameter 19.016 
LOCAL_CONTROL_MODE = f"{NS};i=1048595"
# parameter 19.017 
LOCAL_CONTROL_DISABLE = f"{NS};i=1114131"




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

# parameter 20.001 
EXT1_COMMANDS = f"{NS};i=65556"
# parameter 20.002 
EXT1_START_TRIGGER_TYPE = f"{NS};i=131092"
# parameter 20.003 
EXT1_IN1_SOURCE = f"{NS};i=196628"
# parameter 20.011 
RUN_ENABLE_STOP_MODE = f"{NS};i=720916"
# parameter 20.012 
RUN_ENABLE_1_SOURCE = f"{NS};i=786452"
# parameter 20.023 
POSITIVE_SPEED_ENABLE = f"{NS};i=1507348"
# parameter 20.024 
NEGATIVE_SPEED_ENABLE = f"{NS};i=1572884"


# 21.1 Tryb startu (jeżeli silnik sterowany jest DTC) W przypadku silników zmagnesamitrwałymiisynchro
# nicznych silników reluktancyjnych należy użyć trybu
# startu Automatyczny!!!
# TODO: poczytać o rozruchu silnika
# 21.3 Tryb zatrzymania
# 21.4 Tryb zatrzymania awaryjnego
# 21.5 Żródło zatrzymania awaryjnego
# 21.6 Limit prędkości zerowej
# TODO 21.7-21.18 po przeczytaniu Czym jest magnesowanie (str. 71)

# parameter 21.001 
START_MODE = f"{NS};i=65557"
# parameter 21.003 
STOP_MODE = f"{NS};i=196629"
# parameter 21.004 
EMERGENCY_STOP_MODE = f"{NS};i=262165"
# parameter 21.005 
EMERGENCY_STOP_SOURCE = f"{NS};i=327701"
# parameter 21.006 
ZERO_SPEED_LIMIT = f"{NS};i=393237"
# parameter 21.023 
SMOOTH_START = f"{NS};i=1507349"
# parameter 21.024 
SMOOTH_START_CURRENT = f"{NS};i=1572885"
# parameter 21.025 
SMOOTH_START_SPEED = f"{NS};i=1638421"
# parameter 21.037 
MOTOR_TEMPERATURE_ESTIMATION = f"{NS};i=2424853"


# 22 - wybór wartości zadanej prędkości (Strona 695)
# 22.21 - funkcja stałej prędkości
# 22.22 - 22.24 Wybór, której stałej prędkości urzywać (jedna z 7)
# 22.51, 22.52 22.53 - ustawienia prędkości krytycznej

# parameter 22.021 
CONSTANT_SPEED_FUNCTION = f"{NS};i=1376278"
# parameter 22.022 
CONSTANT_SPEED_SEL1 = f"{NS};i=1441814"
# parameter 22.051 
CRITICAL_SPEED_FUNCTION = f"{NS};i=3342358"
# parameter 22.052 
CRITICAL_SPEED_1_LOW = f"{NS};i=3407894"



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



