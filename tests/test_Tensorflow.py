from dvs_printf import list_of_str
try:
    import tensorflow as tf
    tf_list = tf.Variable([
        [[1,1,1],[2,2,2],[3,3,3]],
        [[4,4,4],[5,5,5],[6,6,6]],
        [[7,7,7],[8,8,8],[9,9,9]],
    ], dtype=tf.float32)

    def test_arrayToList_tf():
        assert list_of_str((tf_list,))==[
    "<tf.Variable 'Variable:0' shape=(3, 3, 3) dtype=float32, numpy=", 
    'array([[[1., 1., 1.],','        [2., 2., 2.],','        [3., 3., 3.]],','',
    '       [[4., 4., 4.],','        [5., 5., 5.],','        [6., 6., 6.]],','', 
    '       [[7., 7., 7.],','        [8., 8., 8.],','        [9., 9., 9.]]], dtype=float32)>']
        
    test_tf_list=[
        '[1.0, 1.0, 1.0]','[2.0, 2.0, 2.0]','[3.0, 3.0, 3.0]', 
        '[4.0, 4.0, 4.0]','[5.0, 5.0, 5.0]','[6.0, 6.0, 6.0]', 
        '[7.0, 7.0, 7.0]','[8.0, 8.0, 8.0]','[9.0, 9.0, 9.0]']

    def test_getmat_true_tf():
        assert list_of_str((tf_list,),getmat= True )==test_tf_list
        assert list_of_str((tf_list,),getmat="true")==test_tf_list

    def test_getmat_show_tf():
        assert list_of_str((tf_list,),getmat="true show info")==test_tf_list+ \
    ["<class 'Tensorflow'", "dtype: 'float32' ",'shape: (3, 3, 3)>']
except:
    pass   


