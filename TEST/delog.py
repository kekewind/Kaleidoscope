import MyUtils


def fun1():
    def fun2():
        def fun3():
            MyUtils.delog(1, 2)
            MyUtils.log(1, 2)

        fun3()

    fun2()


fun1()
