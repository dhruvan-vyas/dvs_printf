from dvs_printf.__printf__ import divide_line

value = """The sun dipped below the horizon, casting a warm, golden hue across the tranquil lake. 
Birds chirped melodiously, their songs harmonizing with the gentle rustling of leaves in the evening breeze. 
Families gathered around picnic tables, laughter and conversation filling the air. Children chased fireflies, 
their joyful giggles echoing through the park. As the sky darkened, stars began to twinkle, 
reflecting in the water like tiny diamonds. The serene atmosphere offered a perfect end to a summer day, 
leaving everyone with a sense of peace and contentment, ready to face the new day with renewed energy and joy."""

expected_output = [
    'The sun dipped below the horizon, casting a warm, golden hue across the tranquil lake. \nBirds ', 
    'chirped melodiously, their songs harmonizing with the gentle rustling of leaves in the evening ', 
    'breeze. \nFamilies gathered around picnic tables, laughter and conversation filling the air. ', 
    'Children chased fireflies, \ntheir joyful giggles echoing through the park. As the sky darkened, ', 
    'stars began to twinkle, \nreflecting in the water like tiny diamonds. The serene atmosphere offered ', 
    'a perfect end to a summer day, \nleaving everyone with a sense of peace and contentment, ready to ', 
    'face the new day with renewed energy and joy.'
]

def test_divide_line():
    assert divide_line(value, 
    tem_len=100) == expected_output
    