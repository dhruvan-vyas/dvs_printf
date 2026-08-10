from dvs_printf import list_of_str


def test_list_array_single():
    list_array = [1,1,1]
    assert (list(list_of_str((list_array,),getmat=True)) == [
                '[1, 1, 1]'
            ])
    
def test_list_array_1D():
    list_array = [[1,1,1],[2,2,2],[3,3,3]]
    assert (list(list_of_str((list_array,),getmat=True)) == [
                '[1, 1, 1]', '[2, 2, 2]', '[3, 3, 3]'
            ])
    
def test_list_array():
    list_array =[
    [[1,1,1],[2,2,2],[3,3,3]],
    [[4,4,4],[5,5,5],[6,6,6]],
    [[7,7,7],[8,8,8],[9,9,9]],]
    assert (list(list_of_str((list_array,),getmat=True))==[
        '[1, 1, 1]', '[2, 2, 2]', '[3, 3, 3]', 
        '[4, 4, 4]', '[5, 5, 5]', '[6, 6, 6]', 
        '[7, 7, 7]', '[8, 8, 8]', '[9, 9, 9]'])
   
