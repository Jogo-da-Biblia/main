# Querys and Mutations to test
query_usuario = """
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
    """

usuario_vazio_query = """
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
    """

query_usuarios = """
        query{
            users{
                id
                username
                email
            }
        }
    """

pergunta_aleatoria_query = """
        query perguntaAleatoriaQuery($temaId: Int){
            pergunta(temaId:$temaId){
                id
                enunciado
            }
        }
    """

todas_perguntas_query = """
        query{
            perguntas{
                id
                enunciado
                tema {
                    id
                    nome
                }
                tipoResposta
                referencia
                status
                criadoPor {
                    id
                    email
                }
                criadoEm
                revisadoPor {
                    id
                    email
                }
                revisadoStatus
                revisadoEm
                recusadoPor {
                    id
                    email
                }
                publicadoPor {
                    id
                    email
                }
                publicadoEm
                atualizadoEm
                alternativas {
                    id
                    texto
                    correta
                }
                alternativasCorretas {
                    id
                    texto
                    correta
                }
                comentarios {
                    id
                    email
                    phone
                    isWhatsapp
                    mensagem
                    criadoEm
                }
            }
        }
    """

todos_temas_query = """
    query{
        temas{
            id
            nome
            cor
        }
    }
    """


todos_comentarios_query = """
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
    """

texto_biblico_query = """
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
    """

novo_usuario_mutation = """
        mutation cadastrarUsuario($novoUsuario: UsuarioInput!) {
            cadastrarUsuario(
                novoUsuario: $novoUsuario
            ){
                usuario{
                    id
                    email
                }
            }	
        }
    """


editar_usuario_mutation = """
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
    """


alterar_permissoes_mutation = """
        mutation alterarPermissoes($userId: Int!, $role: RoleEnum! $action: ActionEnum!){
            alterarPermissoes(
                userId: $userId
                role: $role
                action: $action
            ){
                usuario{
                    id
                    isAdmin
                    isRevisor
                    isPublicador
                }
            }
        }
    """


recuperar_senha_mutation = """
        mutation recuperarSenha($userId: Int!, $email: String!){
            recuperarSenha(
                userId: $userId, 
                email: $email,
            ){
                mensagem
            }
        }
    """


cadastrar_pergunta_mutation = """
    mutation cadastrarPergunta($novaPergunta: PerguntaInput!){
        cadastrarPergunta(
            novaPergunta: $novaPergunta
        ){
            pergunta{
                id
            }
        }
    }
"""

editar_pergunta_mutation = """
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
    """

adicionar_comentario_mutation = """
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
    """


cadastrar_tema_mutation = """
    mutation cadastrarTema($novoTema: TemaInput!)
    {
            cadastrarTema(
                novoTema: $novoTema
                ){
                    tema{
                        id
                        nome
                        cor
                    }
                }
    }
    """


deletar_tema_mutation = """
    mutation deletarTema($temaId: Int!)
    {
        deletarTema(
            temaId: $temaId
            ){
                mensagem
            }
    }
    """
