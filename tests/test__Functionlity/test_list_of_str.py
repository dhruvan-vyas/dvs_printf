# from dvs_printf import list_of_str
from os import get_terminal_size
import re
pattern = re.compile(r'[\x00-\x1F\x7F-\x9F]')
from dvs_printf import list_of_str

# def list_of_str(values: tuple, getmat: bool | str | None = False) -> list[str]:
#     handlers = {
#         dict: lambda x: [f"{k}: {v}" for k, v in x.items()],
#         list: lambda x: list_of_str(tuple(x), getmat),
#         tuple: lambda x: list_of_str(x, getmat),
#         set: lambda x: list_of_str(tuple(x), getmat),
#         str: lambda x: list_of_str(x.split("\n")),
#         "default": lambda x: str(x).split("\n")
#     }
#     result = []
#     for value in values:
#         handler = handlers.get(type(value), handlers["default"])
#         result.extend(handler(value))
#     return result

# def divide_line(string: str, tem_len: int = 80) -> list[str]:
#     result = []
#     while len(string) >= tem_len:
#         cut_index = max(i for i in range(tem_len) if string[:tem_len][i] == " ") or tem_len
#         result.append(string[:cut_index])
#         string = string[cut_index:].lstrip()
#     result.append(string)
#     return result
# import re

# # Assuming pattern is defined to clean up the strings, or can be removed if not needed
# # pattern = re.compile(r"some_pattern")  # Replace with your actual pattern if needed, or omit

# try:tem_len = get_terminal_size()[0] - 2  
# except:tem_len = 80

# def list_of_str(values: tuple, getmat: bool | str | None = False) -> list[str]:
#     def handle_dict(d: dict):
#         result = []
#         for k, v in d.items():
#             result.extend(f"{k}: {v}".split("\n")) 
#         return result
#     print("doing --- ones")
#     handlers = {
#         dict: lambda x: handle_dict(x), 
#         # dict: lambda x: list_of_str_2([f"{k}: {v}".split("\n") for k,v in x.items()]), 
#         list: lambda x: list_of_str(tuple(x), getmat),
#         tuple: lambda x: list_of_str(x, getmat),
#         set: lambda x: list_of_str(tuple(x), getmat),
#         str: lambda x: x.split("\n") if pattern else x.split("\n"),
#     }

#     result = []
#     for value in values:
#         for item in handlers.get(type(value), lambda x: str(x).split("\n"))(value):
#             if len(item) > tem_len:
#                 result.extend(divide_line(item, tem_len))
#             else:
#                 result.append(item)
#     return result


# Dictionarie = {
#         "name": "Johnny Depp",
#         "profession": "Actor & Musician.",
#         "bio": "Passionate about coding\nLoves open-source projects"
#     }
# dict_list = [
#     "name: Johnny Depp", 
#     "profession: Actor & Musician.",
#     "bio: Passionate about coding", 
#     "Loves open-source projects"
# ]

# print(list_of_str_2((Dictionarie,)))
# print(dict_list)


def test_strlist():
    test_list = ["hello", ["hello world", "i am coder"]]
    assert list(list_of_str(test_list)) == ["hello", "hello world", "i am coder"]

def test_intFlote_List():
    test_list = [1234, 5678, [9.876, 2312, 1.3584], -1.2032]
    assert list(list_of_str(test_list)) == ["1234", "5678", "9.876", "2312", "1.3584", "-1.2032"]

    test_list = [
        [ 1.1425223,   0.35365105, -0.4646716],
        [-2.0648264,  -1.82667883,  2.7352082],
        [ 3.0443907,  -0.11200905,  1.5386534] ]
    assert list(list_of_str(test_list,)) == [
        "1.1425223",   "0.35365105", "-0.4646716",
        "-2.0648264",  "-1.82667883", "2.7352082",
        "3.0443907",  "-0.11200905", "1.5386534" ]

def test_all_Types_List():
    test_list = (
        "Greetings, world", "hello\nfrom dvs_printf world",  
        [1234567890, 3.14159, 2.71828, ("nested", 2001, 2002, 2003)],                                                  
        ["apple", "banana", "cherry"], {1: 42, 2: 98.7654}, True, False, None
    )
    assert_list = [
        "Greetings, world", "hello", "from dvs_printf world", 
        "1234567890", "3.14159", "2.71828", "nested", "2001", "2002", "2003", 
        "apple", "banana", "cherry", "1: 42", "2: 98.7654", "True", "False", "None"
    ]
    assert list(list_of_str(test_list)) == assert_list

def test_dict_list():
    Dictionarie = {
        "name": "Johnny Depp",
        "profession": "Actor & Musician.",
        "bio": "Passionate about coding\nLoves open-source projects"
    }
    dict_list = [
        "name: Johnny Depp", 
        "profession: Actor & Musician.",
        "bio: Passionate about coding", 
        "Loves open-source projects"
    ]
    assert list(list_of_str((Dictionarie ,))) == dict_list

def test_set_list():
    test_set = {"apple", 42, 3.14159, "banana", "cherry", -987, "grape"}
    expected_list = ["-987", "3.14159", "42", "apple", "banana", "cherry", "grape"]
    for i in list_of_str(test_set):
        assert True if i in expected_list else i == f"{i}!!!", f"{i} is not in set at (expected_set_list)" 


