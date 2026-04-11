# Documentación de Calidad – NominaPro (prompt-calidad ejecutado)

## Estrategia de Testing
Pirámide: Unit > Integration > E2E.

## Tests Backend (pytest)
```
tests/unit/test_nomina_service.py
cases: happy path, salario integral <13SMMLV error, FSP trigger, transporte.
```

Cobertura objetivo 80% lógica nómina.

## Calidad Código
- Black + Ruff.
- Commits conventional.

Estado: Tests pendientes, lint ok.
