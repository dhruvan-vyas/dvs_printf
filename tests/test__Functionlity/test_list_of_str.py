from dvs_printf import list_of_str

def test_strlist():
    test_list = ["hello", ["hello world", "i am coder"]]
    assert list_of_str(test_list) == ["hello", "hello world", "i am coder"]

def test_intFlote_List():
    test_list = [1234, 5678, [9.876, 2312, 1.3584], -1.2032]
    assert list_of_str(test_list) == ["1234", "5678", "9.876", "2312", "1.3584", "-1.2032"]

    test_list = [
        [ 1.1425223,   0.35365105, -0.4646716],
        [-2.0648264,  -1.82667883,  2.7352082],
        [ 3.0443907,  -0.11200905,  1.5386534] ]
    assert list_of_str(test_list,) == [
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
    assert list_of_str(test_list) == assert_list

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
    assert list_of_str((Dictionarie ,)) == dict_list

def test_set_list():
    test_set = {"apple", 42, 3.14159, "banana", "cherry", -987, "grape"}
    expected_list = ["-987", "3.14159", "42", "apple", "banana", "cherry", "grape"]
    for i in list_of_str(test_set):
        assert True if i in expected_list else i == f"{i}!!!", f"{i} is not in set at (expected_set_list)" 
