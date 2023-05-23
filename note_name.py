from enum import Enum
from math import log
 
class NoteName(Enum):

    C_0 = 0
    C_SHARP_0 = 1
    D_FLAT_0 = 1
    D_0 = 2
    D_SHARP_0 = 3
    E_FLAT_0 = 3
    E_0 = 4
    F_0 = 5
    F_SHARP_0 = 6
    G_FLAT_0 = 6
    G_0 = 7
    G_SHARP_0 = 8
    A_FLAT_0 = 8
    A_0 = 9
    A_SHARP_0 = 10
    B_FLAT_0 = 10
    B_0 = 11

    C_1 = 12
    C_SHARP_1 = 13
    D_FLAT_1 = 13
    D_1 = 14
    D_SHARP_1 = 15
    E_FLAT_1 = 15
    E_1 = 16
    F_1 = 17
    F_SHARP_1 = 18
    G_FLAT_1 = 18
    G_1 = 19
    G_SHARP_1 = 20
    A_FLAT_1 = 20
    A_1 = 21
    A_SHARP_1 = 22
    B_FLAT_1 = 22
    B_1 = 23

    C_2 = 24
    C_SHARP_2 = 25
    D_FLAT_2 = 25
    D_2 = 26
    D_SHARP_2 = 27
    E_FLAT_2 = 27
    E_2 = 28
    F_2 = 29
    F_SHARP_2 = 30
    G_FLAT_2 = 30
    G_2 = 31
    G_SHARP_2 = 32
    A_FLAT_2 = 32
    A_2 = 33
    A_SHARP_2 = 34
    B_FLAT_2 = 34
    B_2 = 35

    C_3 = 36
    C_SHARP_3 = 37
    D_FLAT_3 = 37
    D_3 = 38
    D_SHARP_3 = 39
    E_FLAT_3 = 39
    E_3 = 40
    F_3 = 41
    F_SHARP_3 = 42
    G_FLAT_3 = 42
    G_3 = 43
    G_SHARP_3 = 44
    A_FLAT_3 = 44
    A_3 = 45
    A_SHARP_3 = 46
    B_FLAT_3 = 46
    B_3 = 47

    C_4 = 48
    C_SHARP_4 = 49
    D_FLAT_4 = 49
    D_4 = 50
    D_SHARP_4 = 51
    E_FLAT_4 = 51
    E_4 = 52
    F_4 = 53
    F_SHARP_4 = 54
    G_FLAT_4 = 54
    G_4 = 55
    G_SHARP_4 = 56
    A_FLAT_4 = 56
    A_4= 57
    A_SHARP_4 = 58
    B_FLAT_4 = 58
    B_4 = 59

    C_5 = 60
    C_SHARP_5 = 61
    D_FLAT_5 = 61
    D_5 = 62
    D_SHARP_5 = 63
    E_FLAT_5 = 63
    E_5 = 64
    F_5 = 65
    F_SHARP_5 = 66
    G_FLAT_5 = 66
    G_5 = 67
    G_SHARP_5 = 68
    A_FLAT_5 = 68
    A_5 = 69
    A_SHARP_5 = 70
    B_FLAT_5 = 70
    B_5 = 71

    C_6 = 72
    C_SHARP_6 = 73
    D_FLAT_6 = 73
    D_6 = 74
    D_SHARP_6 = 75
    E_FLAT_6 = 75
    E_6 = 76
    F_6 = 77
    F_SHARP_6 = 78
    G_FLAT_6 = 78
    G_6 = 79
    G_SHARP_6 = 80
    A_FLAT_6 = 80
    A_6 = 81
    A_SHARP_6 = 82
    B_FLAT_6 = 82
    B_6 = 83

def note_name_to_freq(note_name: NoteName) -> float:
    return round(440 * 1.059463**(note_name.value - NoteName.A_4.value), 2)

def freq_to_note_name(freq: float) -> NoteName:
    return NoteName(round(log((freq/440), 1.059463) + NoteName.A_4.value))