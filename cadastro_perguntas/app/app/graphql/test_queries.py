# Querys and Mutations to test
querie_usuario ='''
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

usuario_vazio_querie = '''
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

todos_comentarios_querie = '''
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

texto_biblico_querie = '''
    query{
        textoBiblico(
                referencia: "texto_biblico_referencia"
                versao: "ver1"
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