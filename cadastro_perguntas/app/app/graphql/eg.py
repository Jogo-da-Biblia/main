# Querys and Mutations to test
query_usuario ='''
        query usuarioQuery($userId: Int!){
            user(id:$userId){
                id
                username
                email
                isActive
                perguntasEnviadas {
                    id
                    enunciado
                }
                perguntasRevisadas{
                    id
                    enunciado
                }
                perguntasRecusadas{
                    id
                    enunciado
                }
                perguntasPublicadas{
                    id
                    enunciado
                }
                pontuacao
                isAdmin
                isRevisor
                isPublicador
            }
        }
    '''

usuario_vazio_query = '''
        query{
            user{
                id
                username
                email
                isActive
                perguntasEnviadas {
                    id
                    enunciado
                }
                perguntasRevisadas{
                    id
                    enunciado
                }
                perguntasRecusadas{
                    id
                    enunciado
                }
                perguntasPublicadas{
                    id
                    enunciado
                }
                pontuacao
                isAdmin
                isRevisor
                isPublicador
            }
        }
    '''

query_usuarios = '''
        query{
            users{
                id
                username
                email
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
        mutation cadastrarUsuario($email: String!, $username: String!, $password: String!, $name: String!, $phone: String!, $isWhatsapp: Boolean) {
            cadastrarUsuario(
                email: $email
                username: $username
                password: $password
                name: $name
                phone: $phone
                isWhatsapp: $isWhatsapp
            ){
                usuario{
                    id
                    email
                }
            }	
        }
    '''


editar_usuario_mutation = '''
        mutation editarUsuario($userId: Int!, $email: String, $username: String, $password: String, $name: String, $phone: String, $isWhatsapp: Boolean){
            editarUsuario(
                userId: $userId
                email: $email
                username: $username
                password: $password
                name: $name
                phone: $phone
                isWhatsapp: $isWhatsapp
            ){
                usuario{
                    id
                    username
                    email
                }
            }
        }
    '''


recuperar_senha_mutation = '''
        mutation recuperarSenha($userId: Int!, $email: String!){
            recuperarSenha(
                userId: $userId, 
                email: $email,
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