from dvs_printf import list_of_str
try:
    import numpy as np

    np_list = np.array([
        [[1,1,1],[2,2,2],[3,3,3]],
        [[4,4,4],[5,5,5],[6,6,6]],
        [[7,7,7],[8,8,8],[9,9,9]], 
    ],ndmin=1, dtype="int64")

    def test_arrayToList_numpy():
        assert list(list_of_str(np_list,)) == [
        '[[1 1 1]',' [2 2 2]',' [3 3 3]]', 
        '[[4 4 4]',' [5 5 5]',' [6 6 6]]',
        '[[7 7 7]',' [8 8 8]',' [9 9 9]]'] 
        
    list_getmat_true = [
        '[1, 1, 1]','[2, 2, 2]','[3, 3, 3]',
        '[4, 4, 4]','[5, 5, 5]','[6, 6, 6]', 
        '[7, 7, 7]','[8, 8, 8]','[9, 9, 9]']

    def test_getmat_true_numpy():
        assert list(list_of_str((np_list,),getmat= True ))==list_getmat_true
        assert list(list_of_str((np_list,),getmat="true"))==list_getmat_true
        
    def test_getmat_show_numpy():
        assert list(list_of_str((np_list,),getmat="true show info"))==list_getmat_true+ \
    ["<class 'numpy.ndarray' ",' dtype=int64 ',' shape=(3, 3, 3)>']


except:
    pass

# assert ['[1, 1, 1]', '[2, 2, 2]', '[3, 3, 3]', '[4, 4, 4]', '[5, 5, 5]', '[6, 6, 6]', '[7, 7, 7]', '[8, 8, 8]', '[9, 9, 9]', "<class 'torch.Tensor'>", 'dtype=torch.int64', 'shape=torch.Size([3, 3, 3])>'] == 
#        ['[1, 1, 1]', '[2, 2, 2]', '[3, 3, 3]', '[4, 4, 4]', '[5, 5, 5]', '[6, 6, 6]', '[7, 7, 7]', '[8, 8, 8]', '[9, 9, 9]', "<class 'torch.Tensor'", ' dtype=torch.int64 ', ' shape=torch.Size([3, 3, 3])>']
# list_getmat_true = [
#         '[1, 1, 1]','[2, 2, 2]','[3, 3, 3]',
#         '[4, 4, 4]','[5, 5, 5]','[6, 6, 6]', 
#         '[7, 7, 7]','[8, 8, 8]','[9, 9, 9]']
# np_list = np.array([
#         [[1,1,1],[2,2,2],[3,3,3]],
#         [[4,4,4],[5,5,5],[6,6,6]],
#         [[7,7,7],[8,8,8],[9,9,9]], 
#     ],ndmin=1, dtype="int64")

# L = list(list_of_str((np_list,),getmat="true show info"))
# print("this is from my List Function")
# print(L,end="\n")
# print(list_getmat_true + \
#     ["<class 'numpy.ndarray' ",'dtype=int64 ','shape=(3, 3, 3)>']
#     )
# print("this is What i'm chaking for")