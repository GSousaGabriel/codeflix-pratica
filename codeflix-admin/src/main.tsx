import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { BrowserRouter } from "react-router";
import { setupStore } from "./app/store.ts";
import { Provider } from "react-redux";
import KeycloackProvider from "./features/providers/keycloakProvider.tsx";

const store = setupStore();

createRoot(document.getElementById("root")!).render(
  <Provider store={store}>
    <KeycloackProvider>
      <StrictMode>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </StrictMode>
    </KeycloackProvider>
  </Provider>
);
