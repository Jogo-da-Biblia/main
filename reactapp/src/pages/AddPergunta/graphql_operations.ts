export const TEMAS_QUERY = `query {
  temas {
    edges {
      node {
        nome
        cor
      }
    }
  }
}`