import React from 'react';
import { GlobalStyle } from 'styles/globalStyles';
import { UserProvider } from './contexts/UserContext';
import Routes from './routes';

function App() {
  return (
    <>
      <GlobalStyle />
      <UserProvider>
        <Routes />
      </UserProvider>
    </>
  );
}

export default App;
