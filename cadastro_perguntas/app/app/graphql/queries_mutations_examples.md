## Queries
- user 
    ```graphql
    query{
        user(id:1){
            usuario{
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
    ```
    Tambem pode ser sem especificar o id, nesse caso ele retorna os dados do usuario logado
    ```graphql
    query{
        user{
            usuario{
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
    ```

- users
    ```graphql
    query{
        users{
            usuario{
                id
                username
                pontuacao
            }
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

- textoBiblico
    ```graphql
    query{
        textoBiblico(
            referencia: "Gn 1:26; Ex 10:5"
            versao: "acf"
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
    ```
    O campo `versao` tem como padrão o valor "ara", logo, pode ser vazio
    ```graphql
    query{
        textoBiblico(
            referencia: "Gn 1:26; Ex 10:5"
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