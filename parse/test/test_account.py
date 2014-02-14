"test the account module"

from parse.account import account_from_superpositions as function

from fixtures import Figures, Accounts, Superpositions

account = Accounts.get_random()
superpositions = Superpositions.from_account(account)

# TODO: implement check_function

def test_parses_known_numerals_to_accounts():
    "confirm known numerals recognized correctly"
    expected = account
    found = function(superpositions)
    assert expected == found

def test_parses_illegible_figures_to_accounts():
    "confirm accounts with unknown figures displayed correctly"
    superpositions = Superpositions.from_flawed_figures()
    account = '?' * len(Figures.flawed())  # TODO: use a full length account
    expected = account
    found = function(superpositions)
    assert expected == found

