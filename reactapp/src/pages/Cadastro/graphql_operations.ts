export const CADASTRO_MUTATION = `mutation CreateUser ($username: String!, $email: String!, $phone: String!,  $password: String!) {
    createUser (username: $username, email: $email, phone: $phone, password: $password) {
      user {
        username
      }
    }
  }`