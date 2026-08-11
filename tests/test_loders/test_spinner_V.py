

# import time
# from sys import stdout
# import sys

# from dvs_printf.Loaders.Spinner import Spinner, SpinnerConfig
# from dvs_printf.Loaders._SpinnerFrems import SpinnerFrems
# from time import sleep, time
 
# def long_running_task(duration, progress_updater=None):
#     """A dummy function to simulate a long-running process."""
#     progress = 0
#     start_time = time()
#     while time() - start_time < duration:
#         sleep(0.1)
#         if progress_updater:
#             # Update progress every 100ms
#             progress = ((time() - start_time) / duration) * 100
#             progress_updater.update(progress)

#     # progress_updater.updat(progress)
#     return f"The task took {duration} seconds to complete."

# def another_task(a, b):
#     """Another dummy function to show argument passing."""
#     sleep(2)
#     return a + b

# if __name__ == "__main__":
# #     # print("--- Example 1: `dual` style with time and percentage ---")
#     spinner_percentage = Spinner(
#             config = SpinnerConfig(
#                 attrs=["bold","italic"],
#                 title_color="yellowlime",
#                 spinner_color="yellowlime",
#                 title="Analyzing data", 
#                 style=SpinnerFrems.arrow, 
#                 animation_position='dual', 
#                 timeout=5,
#                 reversed_timer=True,
#                 show_timer=True,
#                 error_message_color="scarlet",
#                 stay=False
#             ),
#             # show_percentage=True, 
#         )

#     print("--- Example 1: ---")
#     result = spinner_percentage.run(long_running_task, duration=4, progress_updater=True)
#     print(f"Final Result: {result} 1.")

#     print("--- Example 2: `after` position with reverse time ---")
#     spinner_dual = Spinner(title="Processing files...", stay=False,style="bouncingBall",animation_position='after', show_progress=True, show_timer=True, reversed_timer=False, timeout=4)
#     result = spinner_dual.run(long_running_task, duration=3, progress_updater=True)
#     print(f"Final Result: {result} 2.")

#     print("--- Example 3: `after` position with reverse time ---")
#     spinner_reverse = Spinner(title="Preparing data...",stay=False, style='bar', animation_position='after', show_timer=True, reversed_timer=True, timeout=5)
#     result = spinner_reverse.run(long_running_task, duration=4)
#     print(f"Final Result: {result} 3.")

#     print("--- Example 4: `before` position with just percentage ---")
#     spinner_percentage = Spinner(title="Analyzing data...", style='growVertical', animation_position='before', show_progress=True, timeout=3,
#                                 stay=False
#                                 )
#     result = spinner_percentage.run(long_running_task, duration=2)
#     print(f"Final Result: {result} 4.")
    
#     print("--- Example 5: Using the decorator ---")
#     spinner_decorator = Spinner(
#         stay=False,
#         title="Calculating...", style='hearts', animation_position='after', show_timer=True, timeout=6,
#     )

#     @spinner_decorator.decorator
#     def decorated_task(x, y):
#         sleep(3)
#         return x * y

#     result = decorated_task(5, 7)
#     print(f"Final Result: {result} 5.")



# # A simple function that takes a few seconds to run
# def my_long_running_task(duration):
#     print("Starting a long-running task...")
#     start_time = time()
#     sleep(duration)
#     end_time = time()
#     print(f"Task finished in {end_time - start_time:.2f} seconds.")
#     return "Task completed successfully!"

# # A function that raises an error
# def my_error_task():
#     print("Starting a task that will fail...")
#     sleep(2)
#     raise ValueError("Something went wrong!")
#     return "This will never be returned."
 
# # # A function with a progress updater
# def my_progress_task(duration, progress_updater):
#     print("Starting a progress-based task...")
#     steps = 10
#     for i in range(steps):
#         sleep(duration / steps)
#         progress = (i + 1) / steps * 100
#         progress_updater.set_progress(progress)
#     return "Progress task is complete!"


# # Test Case 1: Custom Style and Colors
# print("\n--- Test 1: Custom Style and Colors ---")
# result = Spinner(
#     config=SpinnerConfig(
#         title="Working",
#         style="arrow3",
#         spinner_color=("red", "pink"),
#         timer_color="orange",
#         timeout=5
#     )
# ).run(my_long_running_task, 2)
# print(f"Result: {result}")


# # Test Case 2: Timeout
# print("\n--- Test 2: Timeout Scenario ---")
# try:
#     # This task will run for 5 seconds, but the spinner will time out at 3
#     result = Spinner(
#         config=SpinnerConfig(

#         title="Timing out",
#         style="moon",
#         timeout=3,
#         stay=False
#         )
#     )(my_long_running_task, 5)
#     print(f"Result: {result}\n")
# except Exception as e:
#     print(f"Caught an expected error: {e}\n")


# # Test Case 3: Exception Handling
# print("\n--- Test 3: Exception Handling ---")
# try:
#     # This task will run and raise an error
#     Spinner(
#         spinnerText="Error",
#         style="shark",
#         stay=True
#     )(my_error_task)
# except ValueError as e:
#     print(f"Caught an expected error: {e}\n")


# # # Test Case 4: Injecting a Progress Updater
# print("\n--- Test 4: Progress Injection ---")
# result = Spinner(
#     config=SpinnerConfig(
#         inject_progress=True,
#         style=SpinnerFrems.simpleDots,
#         title="Custom Progress",
#         title_color="orange",
#         spinner_color="green",
#         progress_color="red",
#         timer_color="skyblue",
#         animation_position="above"
#     ),
#     stay=True,
#     timeout=5
# )(my_progress_task, 3, progress_updater=True,)
# print(f"Result: {result}\n")


