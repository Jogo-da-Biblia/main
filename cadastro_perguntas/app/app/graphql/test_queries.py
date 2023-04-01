# Querys and Mutations to test
querie_usuario ='''
        query{
            user(id:user_id){
                id
                username
                email
                pontuacao    
                perguntas {
                    id
                    enunciado
                    status
                }
            }
        }
    '''

usuario_vazio_querie = '''
        query{
            user{
                id
                username
                email
                pontuacao    
                perguntas {
                    id
                    enunciado
                    status
                }
            }
        }
    '''

querie_usuarios = '''
        query{
            users{
                id
                username
                pontuacao
            }
        }
    '''

pergunta_aleatoria_querie = '''
        query{
            pergunta(temaId:1){
                id
                enunciado
            }
        }
    '''

todas_perguntas_querie = '''
        query{
            perguntas{
                id
                enunciado
            }
        }
    '''

texto_biblico_querie = '''
        query{
            textoBiblico(
                referencia: "te1 1:21"
                versao: "ver1"
            ){
                livro
                livroAbreviado
                versao
                versaoAbreviada
                capitulo
                versiculo
                texto
            }
        }
    '''

novo_usuario_mutation = '''
        mutation{
            cadastrarUsuario(
                email: "teste1@email.com"
                username: "ususaroteste1"
                isStaff: false
                password: "1938y"
            ){
                usuario{
                    id
                    email
                }
            }	
        }
    '''


editar_usuario_mutation = '''
        mutation{
            editarUsuario(
                id: user_id
                newUsername:"newusername"
                newEmail: "newemai1l@.com"
            ){
                usuario{
                    id
                    username
                    email
                }
            }
        }
    '''


reenviar_senha_mutation = '''
        mutation{
            recuperarSenha(
                usuarioId:user_id, 
                email:"user@email.com"
            ){
                mensagem
            }
        }
    '''


adicionar_nova_pergunta_mutation = '''
        mutation{
            cadastrarPergunta(
                enunciado:"Enunciaod da pergunta",
                outrasReferencias: "outras ref",
                referenciaRespostaId: referencia_id,
                temaId: tema_id,
                tipoResposta: "MES",
            ){
                pergunta{
                    id
                    tema{
                        nome
                    }
                    enunciado
                    tipoResposta
                    status
                    revisadoPor {
                        id
                        username
                        email
                    }
                }
            }
        }
    '''

editar_pergunta_mutation = '''
        mutation{
            editarPergunta(
                id:pergunta_id, 
                enunciado:"Novo enunciado",
                outrasReferencias: "novaOUtraRefe",
                referenciaRespostaId: referencia_id,
                temaId: tema_id,
                tipoResposta: "MES",
                status: true
            ){
                pergunta{
                    id
                    enunciado
                    revisadoPor{
                        id
                        username
                    }
                    status
                    revisadoPor {
                        id
                    }
                }
            }
        }
    '''