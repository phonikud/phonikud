from phonikud.expander import Expander
from phonikud.utils import remove_nikud


def test_numbers():
    expander = Expander()
    text = expander.expand_text("35")
    assert "שלושים" in remove_nikud(text)


def test_teens_are_expanded_as_one_unit():
    expander = Expander()
    # num2words returns "שתים עשרה" for 12; both words must get nikud
    text = expander.expand_text("12")
    assert remove_nikud(text) == "שתים עשרה"
    assert all(word != remove_nikud(word) for word in text.split())
    assert remove_nikud(expander.expand_text("113")) == "מאה ושלוש עשרה"


def test_currency_symbol_follows_number():
    expander = Expander()
    assert remove_nikud(expander.expand_text("$50")).split()[-1] == "dˈolar"
    assert remove_nikud(expander.expand_text("₪50")).split()[-1] == "ʃˈekel"
