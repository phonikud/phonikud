from phonikud.utils import mark_vocal_shva, normalize
from phonikud import phonemize
import pandas as pd
from phonikud import lexicon
from pathlib import Path

BASE_PATH = Path(__file__).parent


def test_vocal_shva():
    df = pd.read_csv(BASE_PATH / "./shva_test_tables/words.csv")
    for row in df.itertuples():
        src_word = row.word
        dst_word = src_word.replace(lexicon.VOCAL_SHVA_DIACRITIC, "")
        dst_word = mark_vocal_shva(dst_word)

        # Normalize
        src_word = normalize(src_word)
        dst_word = normalize(dst_word)

        assert dst_word == src_word


def test_vocal_shva_only_on_shva():
    # No Shva on the first letter, Shva that stays silent, already marked
    for word in ["לִי", "מָה", "וּ|בַיִת", "שְׁתַּיִם", "לְ\u05bdהָכִין"]:
        assert normalize(mark_vocal_shva(word)) == normalize(word)


def test_phonemize_predicts_vocal_shva():
    assert phonemize("לְהָכִין", schema="plain") == "lehaxˈin"
    assert phonemize("לְהָכִין", schema="plain", predict_vocal_shva=False) == "lhaxˈin"
    assert phonemize("וּ|בַיִת", schema="plain") == "uvajˈit"
