import { vi } from "vitest";
import { keycloak } from "../../keycloakConfig";
import { configureStore } from "@reduxjs/toolkit";
import { authSlice } from "../auth/authSlice";
import { render } from "@testing-library/react";
import KeycloackProvider from "./keycloakProvider";
import { Provider } from "react-redux";

vi.mock("../keycloakConfig");

const mockKeycloak = keycloak as ReturnType<typeof vi.mocked<typeof keycloak>>;

describe("KeycloakProvider", () => {
  beforeEach(() => {
    mockKeycloak.init.mockReset();
    mockKeycloak.loadUserInfo.mockReset();
  });

  test("should initialize keycloak and set user data on successfull auth", async () => {
    mockKeycloak.init.mockResolvedValue(true);
    mockKeycloak.loadUserInfo.mockResolvedValue({
      sub: "123",
      name: "John Doe",
      email: "teste@test.com",
    });

    const store = configureStore({
      reducer: { auth: authSlice.reducer },
    });

    render(
      <Provider store={store}>
        <KeycloackProvider>Test</KeycloackProvider>
      </Provider>
    );

    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(mockKeycloak.init).toHaveBeenCalledTimes(1);
    expect(mockKeycloak.loadUserInfo).toHaveBeenCalledTimes(1);
    expect(store.getState().auth.isAuthenticated).toBe(true);
    expect(store.getState().auth.user).toEqual({
      id: "123",
      name: "John Doe",
      email: "teste@test.com",
    });
    expect(store.getState().auth.user).toEqual({
      sub: "123",
      name: "John Doe",
      email: "teste@test.com",
    });
  });

  test("should initialize keycloak and fail to login", async () => {
    mockKeycloak.init.mockResolvedValue(false);

    const store = configureStore({
      reducer: { auth: authSlice.reducer },
    });

    render(
      <Provider store={store}>
        <KeycloackProvider>Test</KeycloackProvider>
      </Provider>
    );

    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(mockKeycloak.init).toHaveBeenCalledTimes(1);
    expect(mockKeycloak.loadUserInfo).toHaveBeenCalledTimes(0);
    expect(store.getState().auth.isAuthenticated).toBe(false);
    expect(store.getState().auth.user).toBeNull();
  });

  test("should initialize keycloak and gives error and do not athenticate", async () => {
    const originalConsoleError = console.error;
    console.error = vi.fn();
    mockKeycloak.init.mockRejectedValue(new Error("Error"));

    const store = configureStore({
      reducer: { auth: authSlice.reducer },
    });

    render(
      <Provider store={store}>
        <KeycloackProvider>Test</KeycloackProvider>
      </Provider>
    );

    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(mockKeycloak.init).toHaveBeenCalledTimes(1);
    expect(mockKeycloak.loadUserInfo).not.toHaveBeenCalled();
    expect(store.getState().auth.isAuthenticated).toBe(false);
    expect(store.getState().auth.user).toBeNull();

    console.error(originalConsoleError);
  });

  test("should initialize keycloak and set token when it expires", async () => {
    const mockUpdateToken = vi.fn().mockResolvedValue(true);
    mockKeycloak.updateToken = mockUpdateToken;

    const store = configureStore({
      reducer: { auth: authSlice.reducer },
    });

    render(
      <Provider store={store}>
        <KeycloackProvider>Test</KeycloackProvider>
      </Provider>
    );

    if (!mockKeycloak.onTokenExpired) {
      throw new Error("onTokenExpired is not defined");
    }

    await vi.waitFor(() => expect(mockUpdateToken).toHaveBeenCalledTimes(1));
    mockKeycloak.onTokenExpired();
    expect(mockUpdateToken).toHaveBeenCalledWith(70);
    expect(store.getState().auth.token).toBe(mockKeycloak.token);
  });
});
