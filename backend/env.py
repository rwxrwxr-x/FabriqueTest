import environ

__all__ = ("env", "root")

env = environ.Env()
root = environ.Path(__file__) - 2

env.read_env(env.path("ENV_FILE_PATH", default=root.path(".env")())())
