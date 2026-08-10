
# Welcome to the dvs_printf Tests

# These imports are needed for functionality tests
from dvs_printf import init, printf, ShowLoading, list_of_str


# (Optiona)l imports for compatibility tests
# import numpy
# import torch
# import tensorflow
# import pandas


# from dvs_printf import list_of_str

# try:
#     import numpy as np

#     np_list = np.array([
#         [[1,1,1],[2,2,2],[3,3,3]],
#         [[4,4,4],[5,5,5],[6,6,6]],
#         [[7,7,7],[8,8,8],[9,9,9]], 
#     ],ndmin=1, dtype="int64")

#     list_getmat_true = [
#         '[1, 1, 1]','[2, 2, 2]','[3, 3, 3]',
#         '[4, 4, 4]','[5, 5, 5]','[6, 6, 6]', 
#         '[7, 7, 7]','[8, 8, 8]','[9, 9, 9]']

#     print( list_of_str((np_list,),getmat="true show info"))
#     print(list_getmat_true+ \
#     ["<class 'numpy.ndarray'",'dtype=int64 ','shape=(3, 3, 3)>'])
# except:
#     pass

# try:
#     import pandas as df 

#     pd_list = df.DataFrame({
#         'A': [[1, 1, 1], [2, 2, 2], [3, 3, 3]],
#         'B': [[4, 4, 4], [5, 5, 5], [6, 6, 6]],
#         'C': [[7, 7, 7], [8, 8, 8], [9, 9, 9]],
#     })


#     test_pd_list = [
#         '[1, 1, 1]', '[4, 4, 4]', '[7, 7, 7]', 
#         '[2, 2, 2]', '[5, 5, 5]', '[8, 8, 8]', 
#         '[3, 3, 3]', '[6, 6, 6]', '[9, 9, 9]'] 

#     print( list_of_str((pd_list,),getmat="true show info"))
#     print( test_pd_list + \
#     ["<class 'pandas'", ' shape=(3, 3) >', 'A: object', 'B: object', 'C: object', 'dtype: object'])
# except:
#     pass

# try:
#     import torch as pt 

#     pt_list = pt.tensor([
#         [[1,1,1],[2,2,2],[3,3,3]],
#         [[4,4,4],[5,5,5],[6,6,6]],
#         [[7,7,7],[8,8,8],[9,9,9]], 
#     ],dtype=pt.int64)

#     test_pt_list=[
#     '[1, 1, 1]', '[2, 2, 2]', '[3, 3, 3]', 
#     '[4, 4, 4]', '[5, 5, 5]', '[6, 6, 6]', 
#     '[7, 7, 7]', '[8, 8, 8]', '[9, 9, 9]']

#     print( list_of_str((pt_list,),getmat="true show info"))
#     print(test_pt_list + \
#     ["<class 'torch.Tensor'", ' dtype=torch.int64 ', ' shape=torch.Size([3, 3, 3])>'])
# except:
#     pass


import tensorflow as tf
tf_list = tf.Variable([
    [[1,1,1],[2,2,2],[3,3,3]],
    [[4,4,4],[5,5,5],[6,6,6]],
    [[7,7,7],[8,8,8],[9,9,9]],
], dtype=tf.float32)


test_tf_list=[
    '[1.0, 1.0, 1.0]','[2.0, 2.0, 2.0]','[3.0, 3.0, 3.0]', 
    '[4.0, 4.0, 4.0]','[5.0, 5.0, 5.0]','[6.0, 6.0, 6.0]', 
    '[7.0, 7.0, 7.0]','[8.0, 8.0, 8.0]','[9.0, 9.0, 9.0]']

print( list(list_of_str((tf_list,),getmat="true show info")))
print(test_tf_list+ \
["<class 'Tensorflow' ", "dtype: 'float32' ",'shape: (3, 3, 3)>'])


