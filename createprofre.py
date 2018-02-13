from profremanager import ProFreManager

if __name__=="__main__":
    try:
        pjId = 83004L
        pro= ProFreManager(pjId)
        pro.frmanage()
    except Exception, e:
        print e.message
#    pro.init_db()