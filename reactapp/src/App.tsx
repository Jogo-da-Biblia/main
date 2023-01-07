import GraphQLClientProvider from 'contexts/GraphQLContext';

import { UserProvider } from './contexts/UserContext';
import Routes from './routes';

import { GlobalStyle } from 'global/styles/globalStyles';

function App() {
  return (
    <>
      <GlobalStyle />
      <GraphQLClientProvider>
        <UserProvider>
          <Routes />
        </UserProvider>
      </GraphQLClientProvider>
    </>
  );
}

export default App;
