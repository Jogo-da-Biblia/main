import GraphQLClientProvider from 'contexts/GraphQLContext';
import { GlobalStyle } from 'styles/globalStyles';
import { UserProvider } from './contexts/UserContext';
import Routes from './routes';

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
