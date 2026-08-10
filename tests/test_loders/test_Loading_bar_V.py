# from dvs_printf.Loaders.Spinner import  Spinner, SpinnerConfig, SpinnerFrems, ProgressUpdater
# from dvs_printf.loaders.Loading_bar import LoadingBar, LoadingBarConfig
# from time import sleep, time

# def test(A=5, progress_updater=None):
#     a = A/100
#     for i in range(1,100):
#         progress_updater.set_progress(i)
#         sleep(a)


#         print("Shoud Not Print On Console:",i)

#     return f"A: {A}"

# lod = LoadingBar(
#     config=LoadingBarConfig(
#         title_text="hello world",
#         title_color=["red", "blue",],
#         bar_color  =["red", "blue",],
#         bar_style='grow',
#         # bar_gradient_style='Loki',
#         # bar_gradient_style=LoadingBarConfig.GradientStyles.cyberwave,
#         grid_rotation_speed=4,
#         timeout=6,
#         full_screen_mode=False,
#         stay=False,
#         # FPS=25,
        
#     )
# )


# lod(
#     test, 
#     progress_updater = True,
# )

