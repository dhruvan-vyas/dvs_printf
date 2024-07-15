from dvs_printf import showLoading
import time

def test_LogingBar():
    Loading_status = \
    showLoading(
        target=time.sleep,
        args = (3),
        LoadingText="Loading_files",
        progressChar="◼︎"   
    )
    assert Loading_status == 0

