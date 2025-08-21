## UV

O gerenciamento de pacotes é feito pelo [UV]()

```shell
# Cria Ambiente
uv venv --python 3.12.08

# Ativa ambiente
.venv\Scripts\activate

uv sync --group docs --group dev
deactivate
```

<br>

---

## Testes

```shell
# Faz o teste do módulo de testes
python -m unittest discover tests -v
```
