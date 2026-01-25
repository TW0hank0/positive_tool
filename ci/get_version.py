import tomllib
import os


def main():
    with open(
        os.path.join(os.path.dirname(__file__), "..", "pyproject.toml"), "rb"
    ) as f:
        d = tomllib.load(f)
    v: str = d["project"]["version"]
    print(v)


if __name__ == "__main__":
    main()
