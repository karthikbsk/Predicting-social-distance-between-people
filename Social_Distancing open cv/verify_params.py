import os
# import logging
# logger = logging.getLogger("intent_ner")

class VerifyValidateParams:

    @staticmethod
    def create_folders_if_doesnot_exist():
        try:
            if 'static' not in os.listdir():
                os.mkdir('static')
            # else:
            #      print("already static exists...")   
            if 'input' not in os.listdir('static'):
                os.mkdir('static/input')
            # else:
            #     print("input exists")    
                
            if 'output' not  in os.listdir('static'):
                os.mkdir('static/output')

        except Exception as e:
            # logger.error(str(e))
            print(str(e))
            
# VerifyValidateParams.create_folders_if_doesnot_exist()
            
