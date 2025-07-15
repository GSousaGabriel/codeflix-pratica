import { useEffect, type ReactNode } from "react";
import { useDispatch } from "react-redux";
import { keycloak } from "../../keycloakConfig";
import { setAuthenticaded, setToken, setUser } from "../auth/authSlice";

const KeycloackProvider = ({ children }: { children: ReactNode }) => {
  const dispatch = useDispatch();

  useEffect(() => {
    const updateToken = async (refresh = false) => {
      try {
        if (refresh) {
          const refreshed = await keycloak.updateToken(70);
          if (refreshed) {
            dispatch(setToken(keycloak.token));
          }
        }
      } catch (error) {
        console.error("Failed to refresh token", error);
      }
    };

    const initKeycloak = async () => {
      try {
        const isAuth = await keycloak.init({
          onLoad: "login-required",
        });

        if (isAuth) {
          dispatch(setAuthenticaded(true));
          dispatch(setToken(keycloak.token));
          const user = await keycloak.loadUserInfo();
          dispatch(setUser(user));
        } else {
          dispatch(setAuthenticaded(false));
        }
      } catch (e) {
        console.log("Keycloak initialization failed: ", e);
        dispatch(setAuthenticaded(false));
      }
    };
    keycloak.onTokenExpired = () => {
      updateToken(true);
    };

    initKeycloak();
  }, [dispatch]);

  return <>{children}</>;
};

export default KeycloackProvider;
