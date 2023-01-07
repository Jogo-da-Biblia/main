export const LOGIN_MUTATION = `mutation ObtainJSONWebToken ($username: String!, $password: String!) {
    tokenAuth (username: $username, password: $password) {
      token
    }
  }`