# Querys and Mutations to test
user_query ='''
        query{
            user(id:user_id){
                user{
                    id
                    username
                    email
                }
                perguntas {
                    id
                    enunciado
                    status
                }
            }
        }
    '''

empty_user_query = '''
        query{
            user{
                user{
                    id
                    username
                    email
                }
                perguntas {
                    id
                    enunciado
                    status
                }
            }
        }
    '''

users_query = '''
        query{
            users{
                user{
                    id
                    username
                    score
                }
        }
    }
    '''

random_pergunta_query = '''
        query{
        pergunta(temaId:1){
            id
            enunciado
        }
    }
    '''

all_perguntas_query = '''
        query{
        perguntas{
            id
            enunciado
        }
    }
    '''

texto_biblico_query = '''
        query{
        textoBiblico(
            referencia: "te1 1:21"
            versao: "ver1"
        ){
            textos{
                livro
                livroAbreviado
                versao
                versaoAbreviada
                capitulo
                versiculo
                texto
            }
        }
    }
    '''

new_user_mutation = '''
        mutation{
        cadastrarUsuario(
            email: "teste1@email.com"
            username: "ususaroteste1"
            isStaff: false
            password: "1938y"
        ){
            user{
            id
            email
            }
        }	
    }
    '''


edit_user_mutation = '''
        mutation{
        editarUsuario(
            id: user_id
            newUsername:"newusername"
            newEmail: "newemai1l@.com"
        ){
            user{
                id
                username
                email
            }
        }
    }
    '''


resend_password_mutation = '''
        mutation{
        recuperarSenha(
            userId:user_id, 
            email:"user@email.com"
        ){
            message
        }
    }
    '''


add_new_pergunta_mutation = '''
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

edit_pergunta_mutation = '''
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