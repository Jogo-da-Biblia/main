# Querys and Mutations to test
query_usuario ='''
        query usuarioQuery($userId: Int!){
            user(id:$userId){
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
        query perguntaAleatoriaQuery($temaId: Int){
            pergunta(temaId:$temaId){
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
    query textoBiblicoQuery($textoBiblicoReferencia: String!){
        textoBiblico(
                referencia: $textoBiblicoReferencia
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
        mutation cadastrarUsuario($email: String!, $username: String!, $password: String!, $isStaff: Boolean) {
            cadastrarUsuario(
                email: $email
                username: $username
                isStaff: $isStaff
                password: $password
            ){
                usuario{
                    id
                    email
                }
            }	
        }
    '''


editar_usuario_mutation = '''
        mutation editarUsuarioMutation($userId: Int!){
            editarUsuario(
                id: $userId
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
        mutation reenviarSenhaMutation($userId: Int!){
            recuperarSenha(
                usuarioId: $userId, 
                email:"user@email.com"
            ){
                mensagem
            }
        }
    '''


adicionar_nova_pergunta_mutation = '''
        mutation adicionarNovaPerguntaMutation($temaId: Int!, $referenciaId: Int!, $tipoResposta: String!){
            cadastrarPergunta(
                enunciado:"Enunciaod da pergunta",
                outrasReferencias: "outras ref",
                referenciaRespostaId: $referenciaId,
                temaId: $temaId,
                tipoResposta: $tipoResposta,
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
        mutation editarPerguntaMutation($perguntaId: Int!, $temaId: Int!, $referenciaId: Int!){
            editarPergunta(
                id:$perguntaId, 
                enunciado:"Novo enunciado",
                outrasReferencias: "novaOUtraRefe",
                referenciaRespostaId: $referenciaId,
                temaId: $temaId,
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
    mutation adicionarComentarioMutation($perguntaId: Int!){
            adicionarComentario(
                mensagem: "mensagem",
                perguntaId: $perguntaId,
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