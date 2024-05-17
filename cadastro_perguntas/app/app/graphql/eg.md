## Queries
- user 
    ```graphql
    query{
        user(id:1){
            id
            username
            email
            pontuacao    
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
        }
    }
    ```
    Tambem pode ser sem especificar o id, nesse caso ele retorna os dados do usuario logado
    ```graphql
    query{
        user{
            id
            username
            email
            pontuacao    
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
        }
    }
    ```

- users
    ```graphql
    query{
        users{
            id
            username
            pontuacao
        }
    }
    ```

- pergunta
    ```graphql
    query{
        pergunta(temaId:1){
            id
            enunciado
        }
    }
    ```

- perguntas
    ```graphql
    query{
        perguntas{
            id
            enunciado
        }
    }
    ```

- comentarios
    ```graphql
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
    ```

- textoBiblico
    ```graphql
      query{
          textoBiblico(
                referencia: "Gn 1:26; Ex 10:5"
                versao: "ara"
            ){
                livro{
                    nome
                    sigla
                    testamento{
                    id
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
    ```
    O campo `versao` tem como padrão o valor "ara", logo, pode ser vazio
    ```graphql
      query{
          textoBiblico(
                referencia: "Gn 1:26; Ex 10:5"
            ){
                livro{
                    nome
                    sigla
                    testamento{
                        id
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
    ```


## Mutations
- cadastrarUsuario
    ```graphql
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
    ```

- editarUsuario
    ```graphql
    mutation{
        editarUsuario(
            id: 12
            newUsername:"newusername"
            newEmail: "newemai1l@.com"
            newIsStaff: true
            newPassword: "newpassword"
        ){
            usuario{
                id
                username
            }
        }
    }
    ```

- recuperarSenha
    ```graphql
    mutation{
        recuperarSenha(
            usuarioId:2, 
            email:"user@email.com"
        ){
            mensagem
        }
    }
    ```

- cadastrarPergunta
    ```graphql
    mutation{
        cadastrarPergunta(
            enunciado:"Enunciaod da pergunta",
            outrasReferencias: "outras ref",
            referenciaRespostaId: 1,
            temaId: 1,
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
    ```

- editarPergunta
    ```graphql
    mutation{
        editarPergunta(
            id:1, 
            enunciado:"Novo enunciado",
            outrasReferencias: "novaOUtraRefe",
            referenciaRespostaId: 1,
            temaId: 1,
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
    ```

- adicionarComentario, lembrando que se o usuario estiver logado será utilizado o email cadastrado
    ```graphql
    mutation{
        adicionarComentario(
            email: "algumemail@email.com"
            mensagem: "mensagem",
            perguntaId: 1,
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
    ```