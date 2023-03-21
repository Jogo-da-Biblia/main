## Queries
- user 
    ```graphql
    query{
        user(id:1){
            id
            username
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

