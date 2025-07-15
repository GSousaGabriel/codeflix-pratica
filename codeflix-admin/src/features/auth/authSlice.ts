import { createSlice } from "@reduxjs/toolkit";
import type { RootState } from "../../app/store";

const initialState = {
  isAuthenticated: false,
  isLoading: false,
  token: null,
  user: null,
};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setAuthenticaded: (state, action) => {
      state.isAuthenticated = action.payload;
    },
    setIsLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    setToken: (state, action) => {
      state.token = action.payload;
    },
    setUser: (state, action) => {
      state.user = action.payload;
    },
  },
});

export const { setAuthenticaded, setIsLoading, setToken, setUser } =
  authSlice.actions;

export const selectIsAthenticated = (state: RootState) =>
  state.auth.isAuthenticated;
export const selectIsLoading = (state: RootState) => state.auth.isLoading;
