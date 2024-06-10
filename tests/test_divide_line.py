from dvs_printf.__printf__ import divide_line

asert_i = """# The sun dipped below the horizon, casting a warm, golden hue across the tranquil lake. 
# Birds chirped melodiously, their songs harmonizing with the gentle rustling of leaves in the evening breeze. 
# Families gathered around picnic tables, laughter and conversation filling the air. Children chased fireflies, 
# their joyful giggles echoing through the park. As the sky darkened, stars began to twinkle, 
# reflecting in the water like tiny diamonds. The serene atmosphere offered a perfect end to a summer day, 
# leaving everyone with a sense of peace and contentment, ready to face the new day with renewed energy and joy."""

asert_j = [
 '# The sun dipped below the horizon, casting a warm, golden hue across the tranquil lake. \n# Birds ', 
 'chirped melodiously, their songs harmonizing with the gentle rustling of leaves in the evening ', 
 'breeze. \n# Families gathered around picnic tables, laughter and conversation filling the air. ', 
 'Children chased fireflies, \n# their joyful giggles echoing through the park. As the sky darkened, ', 
 'stars began to twinkle, \n# reflecting in the water like tiny diamonds. The serene atmosphere ', 
 'offered a perfect end to a summer day, \n# leaving everyone with a sense of peace and contentment, ', 
 'ready to face the new day with renewed energy and joy.'
]

def test_divide_line():
    assert divide_line(asert_i, 100) == asert_j
    