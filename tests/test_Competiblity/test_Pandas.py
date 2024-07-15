from dvs_printf import list_of_str
try:
    import pandas as df 

    pd_list = df.DataFrame({
        'A': [[1, 1, 1], [2, 2, 2], [3, 3, 3]],
        'B': [[4, 4, 4], [5, 5, 5], [6, 6, 6]],
        'C': [[7, 7, 7], [8, 8, 8], [9, 9, 9]],
    })

    def test_arrayToList_pd():
        assert list_of_str((pd_list,)) == [
        '           A          B          C', 
        '0  [1, 1, 1]  [4, 4, 4]  [7, 7, 7]', 
        '1  [2, 2, 2]  [5, 5, 5]  [8, 8, 8]', 
        '2  [3, 3, 3]  [6, 6, 6]  [9, 9, 9]'] 

    test_pd_list = [
        '[1, 1, 1]', '[4, 4, 4]', '[7, 7, 7]', 
        '[2, 2, 2]', '[5, 5, 5]', '[8, 8, 8]', 
        '[3, 3, 3]', '[6, 6, 6]', '[9, 9, 9]'] 

    def test_getmat_true_pd():
        assert list_of_str((pd_list,),getmat= True )==test_pd_list
        assert list_of_str((pd_list,),getmat="true")==test_pd_list

    def test_getmat_show_pd():
        assert list_of_str((pd_list,),getmat="true show info")== test_pd_list + \
    ["<class 'pandas'", ' shape=(3, 3) >', 'A: object', 'B: object', 'C: object', 'dtype: object']
except:
    pass