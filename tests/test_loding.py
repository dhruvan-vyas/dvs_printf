from dvs_printf import showLoding
import time

def test_SleepLoging():
    assert 0 == showLoding(target=time.sleep,
        args = (1),
        lodingText="Loding_files",
        lodingChar="◼︎"   
    )

