```bash
docker volume create keycloak_data

docker run -p 8001:8001 \
    -e KC_BOOTSTRAP_ADMIN_USERNAME=admin \
    -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin \
    -v keycloak_data:/opt/keycloak/data \
    quay.io/keycloak/keycloak:26.2.5 start-dev --http-port=8001
```