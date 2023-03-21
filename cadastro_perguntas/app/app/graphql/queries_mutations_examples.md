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
            id
            username
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
        recuperarSenha(userId:1){
            user{
                id
                email
            }
        }
    }
    ```