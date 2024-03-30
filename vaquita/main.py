from services.server_svc import ServerSvc


def main():
    # Crear una instancia del servidor
    server = ServerSvc(host='::', port=12345)

    # Iniciar el servidor
    server.start_server()

    # Aceptar conexiones de forma continua
    server.accept_connections()


if __name__ == "__main__":
    main()