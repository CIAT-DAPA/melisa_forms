import os 

config = {}

if os.getenv('DEBUG', "true").lower() == "true":
    config['DEBUG'] = True
    config['HOST'] = 'localhost'
    config['PORT'] = 5002
    config['CONNECTION_DB']='mongodb://root:s3cr3t@localhost:27017/testmelissa?authSource=admin'
    config['CONNECTION_DB2']='mongodb://root:s3cr3t@localhost:27017/bk?authSource=admin'
else:
    config['DEBUG'] = False
    config['HOST'] = '0.0.0.0'
    config['PORT'] = os.getenv('MELISA_ADMIN_PORT')
    config['CONNECTION_DB']=os.getenv('CONNECTION_DB')
    config['CONNECTION_DB2']=os.getenv('CONNECTION_DB2')
