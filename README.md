# Medical Tables API (CID-10 & SIGTAP) 🏥

Microsserviço de alta performance para consulta de tabelas médicas oficiais brasileiras. 
Fornece busca textual inteligente e consulta por código para:
1.  **CID-10** (Classificação Internacional de Doenças)
2.  **SIGTAP** (Tabela Unificada de Procedimentos do SUS)

## 🚀 Funcionalidades

*   ⚡ **Ultra Rápido**: Todo o banco de dados é carregado na memória RAM na inicialização.
*   🔍 **Busca Híbrida**: Pesquise por código (ex: `F32`) ou descrição (ex: `Depressão`) no mesmo endpoint.
*   🐋 **Docker Ready**: Pronto para rodar isolado ou em orquestração.

---

## 🛠️ Endpoints

### 1. Consultar CID-10

#### Busca (Search)
*   **Método:** `GET`
*   **URL:** `/cid/search?q={termo}`
*   **Parâmetros:** `q` (mínimo 3 caracteres)

**Exemplo de Resposta:**
```json
{
  "count": 2,
  "results": [
    {"codigo": "F32", "descricao": "Episódios depressivos"},
    {"codigo": "F33", "descricao": "Transtorno depressivo recorrente"}
  ]
}
```

#### Código Exato
*   **Método:** `GET`
*   **URL:** `/cid/code/{codigo}`

---

### 2. Consultar Procedimentos (SIGTAP)

#### Busca (Search)
*   **Método:** `GET`
*   **URL:** `/sigtap/search?q={termo}`
*   **Parâmetros:** `q` (mínimo 3 caracteres)

#### Código Exato
*   **Método:** `GET`
*   **URL:** `/sigtap/code/{codigo}`

---

## 💻 Exemplos de Código

### Python (Requests)
```python
import requests

API_URL = "http://api-cid.gtmedics.com"

def buscar_cid(termo):
    response = requests.get(f"{API_URL}/cid/search", params={"q": termo})
    if response.status_code == 200:
        return response.json()
    return None

def buscar_procedimento(termo):
    response = requests.get(f"{API_URL}/sigtap/search", params={"q": termo})
    if response.status_code == 200:
        return response.json()
    return None

# Uso
print(buscar_cid("Ansiedade"))
print(buscar_procedimento("Biopsia de tireoide"))
```

### TypeScript (Axios / Fetch)
```typescript
interface MedicalItem {
  codigo: string;
  nome?: string;      // No SIGTAP chama 'nome'
  descricao?: string; // No CID chama 'descricao'
}

interface SearchResponse {
  count: number;
  results: MedicalItem[];
}

const API_BASE = "http://api-cid.gtmedics.com";

async function searchTable(type: 'cid' | 'sigtap', query: string) {
  try {
    const res = await fetch(`${API_BASE}/${type}/search?q=${encodeURIComponent(query)}`);
    if (!res.ok) throw new Error("Erro na busca");
    
    const data: SearchResponse = await res.json();
    return data.results;
  } catch (err) {
    console.error(err);
    return [];
  }
}

// Uso
searchTable('cid', 'F32').then(console.log);
searchTable('sigtap', 'Hemograma').then(console.log);
```

---

## 🐳 Como Rodar

Este serviço faz parte do stack `docker-compose.fastapi.yml`.

```bash
# Subir apenas este serviço
docker compose -f ../docker-compose.fastapi.yml up -d --build api_cid
```

## 📜 Licença

MIT License

Copyright (c) 2026 GTELL

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.