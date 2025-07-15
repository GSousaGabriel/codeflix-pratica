import Keycloak from "keycloak-js";

const keycloakConfig= {
    url: "http://localhost:8082/auth",
    realm: "codeflix",
    clientId: "codeflix-admin",

}

export const keycloak = new Keycloak(keycloakConfig);
