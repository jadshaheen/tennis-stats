import pytest

from tennis_stats import logic
from tennis_stats.utils import types

def test_sanitize_input_name():
    inp = 'Roger Federer'
    expected = types.Table.PLAYER, 'roger federer'
    assert(logic.sanitize_input(inp) == expected)

def test_sanitize_input_rankings():
    inp = 'Rank'
    expected = types.Table.RANKINGS, 'rank'
    assert(logic.sanitize_input(inp) == expected)

def test_sanitize_input_tournament():
    inp = 'roland garros'
    expected = types.Table.TOURNAMENT, 'French Open'
    assert(logic.sanitize_input(inp) == expected)

def test_sanitize_input_year():
    inp = '2019'
    expected = types.Table.YEAR, '2019'
    assert(logic.sanitize_input(inp) == expected)


def test_match_tournament_aussie():
    valid_1 = 'aussie open'
    valid_2 = 'australian open'
    match_string = 'Australian Open'

    assert(logic.match_tournament(valid_1) == match_string)
    assert(logic.match_tournament(valid_2) == match_string)

def test_match_tournament_french():
    valid_1 = 'french open'
    valid_2 = 'roland garros'
    match_string = 'French Open'

    assert(logic.match_tournament(valid_1) == match_string)
    assert(logic.match_tournament(valid_2) == match_string)

def test_match_tournament_wimbledon():
    valid_1 = 'wimbledon'
    match_string = 'Wimbledon'

    assert(logic.match_tournament(valid_1) == match_string)

def test_match_tournament_us():
    valid_1 = 'us open'
    valid_2 = 'u.s. open'
    match_string = 'U.S. Open'

    assert(logic.match_tournament(valid_1) == match_string)
    assert(logic.match_tournament(valid_2) == match_string)

def test_match_tournament_invalid():
    invalid_1 = 'aussieopen'
    invalid_2 = 'frenc open'
    invalid_3 = 'wimbdon'
    invalid_4 = 'u..s. open'

    assert(logic.match_tournament(invalid_1) == False)
    assert(logic.match_tournament(invalid_2) == False)
    assert(logic.match_tournament(invalid_3) == False)
    assert(logic.match_tournament(invalid_4) == False)


