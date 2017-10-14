import os
import base64
import hashlib
from Crypto.Cipher import AES
import time

def limpa(): 
    os.system('cls')  

def entrada():
     return [ raw_input("Digite o usuario: "), raw_input("Digite a senha: ") ]

def valida_usuario(login,senha): 
    usuario = open('usuario.txt','r').readlines()
    return usuario[0].replace('\n','') == login and usuario[1].replace('\n','') == hashlib.md5( senha + usuario[2].replace('\n','') ).hexdigest()    

def criptar(chave):
    aes = AES.new(chave, AES.MODE_ECB)
    arquivo = raw_input('\nDigite o nome do arquivo a ser Criptografado: ')

    arq_entrada = open(arquivo, "r")
    arq_entrada = arq_entrada.read()

    cryptoSaida = arq_entrada+'#'*(16-len(arq_entrada)%16)

    conteudo = base64.b32encode(aes.encrypt(cryptoSaida))

    titulo_novo=base64.b32encode(aes.encrypt(arquivo+'#'*(16-len(arquivo)%16)))

    arq_saida = open(titulo_novo,'w')
    arq_saida.write(conteudo)
    arq_saida.close()
    return titulo_novo

def decriptar(chave):
    aes = AES.new(chave, AES.MODE_ECB)

    arquivo = raw_input('\nDigite o nome do arquivo para ser Decriptografado: ')

    arq_entrada = open(arquivo, "r")
    arq_entrada = base64.b32decode(arq_entrada.read())

    titulo_antigo=aes.decrypt(base64.b32decode(arquivo))
    titulo_antigo=titulo_antigo.rstrip('#')

    conteudo_recuperado=aes.decrypt(arq_entrada)
    conteudo_recuperado=conteudo_recuperado.rstrip('#')
    
    r = True
    novo_titulo = ''
    
    try: #TRATAMENTO CASO A CHAVE ESTEJA INCORRETA#
        t = titulo_antigo.split('.')
        novo_titulo = t[0] + '_new.' + t[1]
        arq_saida2 = open( novo_titulo ,"w")
        arq_saida2.write(conteudo_recuperado)
    except:
        r = False
    return [r , novo_titulo]   

if __name__ == "__main__":
    #0123456789ABCDEF
    retorno = entrada()
    while True:
        if valida_usuario(retorno[0],retorno[1]):
            print('Aguarde...')
            time.sleep(2)
            #limpa() 
            acao = raw_input('\nDigite E para Encripitar ou D para Decripitar: ')
            chave = raw_input('\nDigite a chave de 16bytes: ')
            if acao.upper() == 'E': 
               print('\nArquivo Criptografado com sucesso: ===> '+criptar(chave)) 
            else:
               msg = decriptar(chave)
               if msg[0]:
                   print('\nArquivo Decriptografado com sucesso: ===>'+msg[1])
               else:
                   print('\nFalha, CHAVE incorreta')                   
        else:
            limpa()
            print('Usuario ou Senha incorreto, tente novamente')
            retorno = entrada()    
        
  
   