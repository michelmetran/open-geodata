## UV

O gerenciamento de pacotes é feito pelo [UV]()

```shell
# Ativa ambiente
.venv\Scripts\activate

uv sync --group docs
deactivate
```

<br>

---

## Testes

```shell
# Faz o teste do módulo de testes
python -m unittest discover tests -v
```
