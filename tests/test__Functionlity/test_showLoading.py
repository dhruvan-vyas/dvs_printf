from dvs_printf import ShowLoading, showLoading
import time

def test_ShowLoading():
    Loading_status = \
    ShowLoading(
        target=time.sleep,
        args=0.01,
        timeout=0.1,
        title_text="Loading_files",
        bar_color=["red", "orange", "blue"]   
    )
    assert Loading_status is None

def test_Deprocated_LogingBar():
    Loading_status = \
    showLoading(
        target=time.sleep,
        args=0.01,
        timeout=0.1,
        LoadingText="Loading_files",
        progressChar="◼︎"   
    )
    assert Loading_status is None