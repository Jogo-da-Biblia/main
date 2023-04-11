# Querys and Mutations to test
query_usuario ='''
        query{
            user(id:user_id){
                id
                username
                email
                pontuacao    
                perguntasCriadas {
                id
                enunciado
                }
                perguntasRevisadas{
                id
                enunciado
                }
                perguntasPublicadas{
                    id
                    enunciado
                }
            }
        }
    '''

usuario_vazio_query = '''
        query{
            user{
                id
                username
                email
                pontuacao    
                perguntasCriadas {
                id
                enunciado
                }
                perguntasRevisadas{
                id
                enunciado
                }
                perguntasPublicadas{
                    id
                    enunciado
                }
            }
        }
    '''

query_usuarios = '''
        query{
            users{
                id
                username
                pontuacao
            }
        }
    '''

pergunta_aleatoria_query = '''
        query{
            pergunta(temaId:tema_id){
                id
                enunciado
            }
        }
    '''

todas_perguntas_query = '''
        query{
            perguntas{
                id
                enunciado
            }
        }
    '''

todos_comentarios_query = '''
    query{
        comentarios{
            id
            mensagem
            email
            phone
            pergunta {
                id
                enunciado
            }
        }
    }
    '''

texto_biblico_query = '''
    query{
        textoBiblico(
                referencia: "texto_biblico_referencia"
                versao: "ara"
            ){
                livro{
                    nome
                    sigla
                    testamento{
                        nome
                    }
                }
                versao{
                    nome	
                    sigla
                }
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
                tipoResposta: "tipo_resposta",
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

adicionar_comentario_mutation = '''
    mutation{
            adicionarComentario(
                mensagem: "mensagem",
                perguntaId: pergunta_id,
                phone: "12345678911",
                isWhatsapp: true
                ){
                comentario{
                    phone
                    isWhatsapp
                    email
                    mensagem
                    pergunta{
                        id
                        enunciado
                    }
                }
            }
        }
    '''