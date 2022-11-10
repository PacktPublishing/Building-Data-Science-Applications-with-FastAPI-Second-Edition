def greeting(name: str | None = None) -> str:
    return f"Hello, {name if name else 'Anonymous'}"


print(greeting())  # "Hello, Anonymous"
