from dvs_printf import list_of_str

def test_strlist():
    test_list = (["hello",["hello world","i am coder"]])
    assert list_of_str(test_list)==["hello","hello world","i am coder"]

def test_intFloteList():
    test_list = ([1234, 5678, 9876, 12.003244])
    assert list_of_str(test_list)==["1234","5678","9876","12.003244"]

def test_all_Types_List():
    test_list = ("hii, hello", "hello\nworld",  
       [1027221123, 98.637417, 51.01237,    
        ["hiii", 112233, 334455]],                                                  
        ("aaaaa","bbbbb","ccccc",11111,234552.00803),  )
    assert_list = ["hii, hello", "hello", "world",  
        "1027221123", "98.637417", "51.01237", "hiii", "112233", "334455",                                                                 
        "aaaaa", "bbbbb", "ccccc", "11111", "234552.00803" ]
    assert list_of_str(test_list) == assert_list

def test_dictList():
    Dictionarie = { "a":"it should work",
    "b":"abcdefg","c":"testing with \nThe newline character"  },  
    dict_list = ["a: it should work","b: abcdefg",
    "c: testing with ","The newline character"]
    assert list_of_str(Dictionarie) == dict_list

def test_setList():
    Dictionarie = list_of_str( 
    { "it should work","abcdefg",
    "testing with \nThe newline character"},)
    set_list = ["it should work","abcdefg",
    "testing with ","The newline character"]
    for i in set_list:
        if i in Dictionarie:assert True
        else:assert i == f"{i} is not in Dictionarie at (test_dictList)"
