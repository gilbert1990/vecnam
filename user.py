from web3 import Web3
from decouple import config
import json
import hashlib
from datetime import datetime

# Conexión a una red Ethereum local 
w3=Web3(Web3.HTTPProvider(config('WEB3_URL')))

# Dirección del contrato
contract=''
with open(config('CONTRACT_ABI'), encoding='utf-8') as f:
    contract = json.load(f).get('abi')

contrato = w3.eth.contract(address='0xC8C6A1C87A90615af9bC8c1a25331c9F92238F53', abi=contract) 


def userCreate(name, document, date_document, email,rol,password,birthdate):
    # Obtén la fecha actual
    fecha_actual = datetime.now()
    if datetime.strptime(birthdate, "%Y-%m-%d") < fecha_actual and datetime.strptime(date_document, "%Y-%m-%d") < fecha_actual:
        # Llamar a la función createUser del contrato para crear el usuario
        try:
            prueba=  contrato.functions.createUser(name,birthdate, int(document), date_document, email,rol,hashlib.md5(password.encode('utf-8')).hexdigest()).transact({'from': config('CONTRACT_USER')})
            # Clave privada de tu cuenta
            private_key = '9c9f8668c42f441ca16e8fc69e182d67'
            
            # Firmar la transacción
            signed_txn = w3.eth.account.signTransaction(transaction, private_key)
            
            # Enviar la transacción firmada a través de Infura
            tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            return {'message':'Usuario creado correctamete',"code":200}
        except Exception as e:
            return {'message':str(e),"code":400}
    else:
        return {'message':'Las fechas deben ser menor a la actual.',"code":400}
    
def userAuth(documento_usuario, password, rol):
    # Llamar a la función createUser del contrato para crear el usuario
    try:
        contrato.functions.authenticateUser(int(documento_usuario), hashlib.md5(password.encode('utf-8')).hexdigest(), rol).transact({'from': config('CONTRACT_USER')})
        return {'message':'Usuario creado correctamete',"code":200}
    except Exception as e:
       
        return {'message':str(e),"code":400}
    
def getUser(document_user):
    user= contrato.functions.getUserInfoByDocument(int(document_user)).call({'from': config('CONTRACT_USER')})
    medicalHistory=contrato.functions.getMedicalHistoryAddress(user[8]).call({'from': config('CONTRACT_USER')})
    familyHistory=contrato.functions.getFamilyHistoryAddress(user[8]).call({'from': config('CONTRACT_USER')})
    user_info={'user':user,'medicalHistory':medicalHistory,'familyHistory':familyHistory}

    return user_info

def registerMedical(address,alcohol,smoke,physical_activity,contraceptives,fracture,surgery):
    try:
        contrato.functions.setMedicalHistory(int(alcohol),int(smoke),int(physical_activity),int(contraceptives),int(fracture),surgery,address).transact({'from': config('CONTRACT_USER')})
        return {'message':'Usuario editado',"code":200}
    except Exception as e:
        return {'message':str(e),"code":400}
    
def registerFamily( address, diabetes,
         hypertension,
         heart,
         respiratory,
         alzheimer,
         cardiovascular,
         cancer):
    try:
        contrato.functions.setFamilyHistory(int(diabetes),int(hypertension),int(heart),int(respiratory),int(alzheimer),int(cardiovascular),int(cancer),address).transact({'from': config('CONTRACT_USER')})
        return {'message':'Usuario editado',"code":200}
    except Exception as e:
        return {'message':str(e),"code":400}
    
def lista_usuarios():
    try:
        lista = contrato.functions.getAllUserNames().call({'from': config('CONTRACT_USER')})
        return lista
    except Exception as e:
        return []