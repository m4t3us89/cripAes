import os
import base64
import hashlib
from Crypto.Cipher import AES
import time

def limpa(): #LIMPA TERMINAL
    os.system('cls')  

def entrada(): #ENTRADA USUARIO E SENHA
     return [ raw_input("Digite o usuario: "), raw_input("Digite a senha: ") ]

def valida_usuario(login,senha): #VALIDA USUARIO E SENHA (SENHA == (HASH(SENHA+SALT)))
    usuario = open('usuario.txt','r').readlines()
    return usuario[0].replace('\n','') == login and usuario[1].replace('\n','') == hashlib.md5( senha + usuario[2].replace('\n','') ).hexdigest()    

def criptar(chave):
    #criando uma instancia AES. 
    #Primeiro parametro a CHAVE de 16bytes.
    #segundo parametro modo ECB de criptografia AES
    aes = AES.new(chave, AES.MODE_ECB)

    #recebe o arquivo a ser criptografado
    arquivo = raw_input('\nDigite o nome do arquivo a ser Criptografado: ')

    #ler o arquivo
    arq_entrada = open(arquivo, "r")
    arq_entrada = arq_entrada.read()

    #O modo ECB so permite que o tamanho do nosso arquivo seja multiplo do tamanho da nossa chave
    #Caso nao seja completamos com o caracteres '#' 
    cryptoSaida = arq_entrada+'#'*(16-len(arq_entrada)%16)

    #criptografando o arquivo corrigido
    #alem disso vamos colocar os dados criptografados
    #em uma forma que caracteres estranhos nao aparecam
    texto_cifrado = base64.b32encode(aes.encrypt(cryptoSaida))

    #nesta etapa eh realizado os passos anteriores mas desta vez no titulo
    titulo_novo=base64.b32encode(aes.encrypt(arquivo+'#'*(16-len(arquivo)%16)))

    arq_saida = open(titulo_novo,'w')
    arq_saida.write(texto_cifrado)
    arq_saida.close()
    return titulo_novo

def decriptar(chave):
    #criando uma instancia AES. 
    #Primeiro parametro a CHAVE de 16bytes.
    #segundo parametro modo ECB de criptografia AES
    aes = AES.new(chave, AES.MODE_ECB)

    #recebe o arquivo a ser criptografado
    arquivo = raw_input('\nDigite o nome do arquivo para ser Decriptografado: ')


    #ler o arquivo
    arq_entrada = open(arquivo, "r")
    #esta etapa iremos decodificar os caracteres para sua forma original
    arq_entrada = base64.b32decode(arq_entrada.read())

    #vamos recuperar o nome do arquivo e retirar os 
    #caracteres adicionais que colocamos na etapa passada
    titulo_antigo=aes.decrypt(base64.b32decode(arquivo))
    titulo_antigo=titulo_antigo.rstrip('#')

    #vamos repetir o processo para o conteudo do arquivo
    texto_recuperado=aes.decrypt(arq_entrada)
    texto_recuperado=texto_recuperado.rstrip('#')
    
    r = True
    novo_titulo = ''
    
    try: #TRATAMENTO CASO A CHAVE ESTEJA INCORRETA
        #e por fim vamos recriar o arquivo na sua forma original apenas renomeando o titulo
        t = titulo_antigo.split('.')
        novo_titulo = t[0] + '_new.' + t[1]
        arq_saida2 = open( novo_titulo ,"w")
        arq_saida2.write(texto_recuperado)
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
        
  
   