## Queries
- user 
    ```graphql
    query{
        user(id:1){
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
    ```
    Tambem pode ser sem especificar o id, nesse caso ele retorna os dados do usuario logado
    ```graphql
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
    ```

- users
    ```graphql
    query{
        users{
            user{
                id
                username
                score
            }
        }
    }
    ```

- pergunta
    ```graphql
    query{
        pergunta(tema:"1"){
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
        ){
            textos{
            livro
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
            user{
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
            user{
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
            userId:2, 
            email:"user@email.com"
        ){
            message
        }
    }
    ```