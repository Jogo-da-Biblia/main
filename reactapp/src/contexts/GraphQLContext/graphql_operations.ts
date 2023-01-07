export const VERIFY_TOKEN_MUTATION = `mutation Verify ($token: String) {
  verifyToken (token: $token) {
    payload
  }
}`

export const ME_QUERY = `query {
  me{
    username
    email
    name
    phone
  }
}`