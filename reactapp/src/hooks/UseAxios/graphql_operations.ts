export const REFRESH_TOKEN_MUTATION = `mutation Refresh (token: String) {
  refreshToken (token: $token) {
    token
  }
}`