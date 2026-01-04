# Análise Comparativa de Cenários Epidemiológicos em um Modelo CA-SEIR com Diferentes Taxas de Transmissão (β)

Este projeto implementa uma simulação epidemiológica baseada no modelo **SEIR**, utilizando **Autômatos Celulares (CA)** para representar a propagação da influenza sazonal em uma grade bidimensional.

O programa gera automaticamente:

- Snapshots da evolução espacial (Cenário 1)
- Gráficos SEIR individuais para cada cenário
- Gráfico comparativo das curvas de infectados
- Todos os arquivos são salvos na pasta **resultados/**

---

## 1. Estrutura do Projeto

```
├── main.py
├── requirements.txt
├── resultados/
└── README.md
```

---

## 2. Criar Ambiente Virtual

### Criar ambiente:
```bash
python -m venv venv
```

### Ativar ambiente:

**Windows**
```bash
venv\Scripts\activate
```


## 3. Instalar Dependências

```bash
pip install -r requirements.txt
```


## 4. Executar o Projeto

```bash
python main.py
```

Após rodar, os arquivos serão criados na pasta:

```
/resultados
```

## 5. Sobre o Modelo Utilizado

### Modelo SEIR
Divide a população em:

- S — Suscetível  
- E — Exposto  
- I — Infectado  
- R — Recuperado  

### Autômatos Celulares
A população é representada por uma grade **100×100** onde cada célula:

- Interage com 8 vizinhos (vizinhança de Moore)
- Transita entre estados de acordo com β, σ e γ

### Parâmetros dos Cenários

| Cenário | β |
|--------|----|
| Cenário 1 | 0.10 |
| Cenário 2 | 0.18 |
| Cenário 3 | 0.35 |

---

## 6. Resultados Gerados

- **Evolução espacial** (Cenário 1)
- **Gráficos SEIR individuais**
- **Gráfico comparativo dos infectados**

Essas visualizações ajudam a entender como diferentes valores de β influenciam a propagação da epidemia.

---

## 7. Objetivo do Projeto

- Demonstrar o uso de autômatos celulares em epidemiologia  
- Explorar o impacto da taxa de transmissão β  
- Gerar visualizações didáticas e comparativas  
- Apoiar estudos e análises de surtos simulados  

---


