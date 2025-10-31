# vocabulary-cardgame

![demo](https://github.com/user-attachments/assets/867b600e-cc8a-498f-808b-dd797539412a)

Este proyecto es un sencillo juego de repaso de vocabulario en inglés mediante tarjetas en CLI (línea de comandos).

---

## ¿Cómo funciona?

1. Tienes un archivo CSV que actúa como tu **base de datos de vocabulario**.  
   - Debe tener **dos columnas**:
     - `english`: la palabra en inglés.  
     - `spanish`: su traducción al español.  
   - Puedes editar o reemplazar el archivo de ejemplo, siempre que **mantengas el nombre y las columnas**.

   **Ejemplo:**

   | new word | translation |
   |-----------|-------------|
   | To hoard     | Acumular    |
   | Allegedly    | Presuntamente |
   | Snuggled    | Acurrucado     |

2. Cuando ejecutas el script por primera vez, se crea un archivo JSON que almacena los **pesos y estadísticas de aprendizaje** de cada palabra.  
   Por ejemplo:

   ```json
   {
     "To hoard ": {
       "seen": 0,
       "success": 0
     }
   }

3. Se selecciona una palabra al azar, con una probabilidad dada por el histórico de tu rendimiento:

- Si fallas una palabra, su probabilidad de volver a salir aumenta.
- Si la aciertas repetidamente, aparecerá con menos frecuencia.

Tú indicas si te sabías o no la palabra, y el programa actualiza las estadísticas en el JSON. 

## Cálculo de la probabilidad de aparición

Cada palabra tiene un peso dinámico, que determina con qué frecuencia puede salir. El peso se calcula según el número de veces que has visto la palabra (seen) y las veces que la has acertado (success).

\[
w = 
\begin{cases} 
1.0 & \text{si } seen = 0 \\[2mm]
\max(0.1, 1 - \frac{success}{seen}) & \text{si } seen > 0
\end{cases}
\]

- Si nunca has visto la palabra, su peso es **1.0** (máxima probabilidad).  
- Si la has visto varias veces y la aciertas a menudo, el peso **disminuye**.  
- Nunca baja de **0.1**, para que todas las palabras sigan apareciendo de vez en cuando.

**Ejemplos:**

1. Visto 5 veces, acertado 2 veces:

\[
w = 1 - \frac{2}{5} = 0.6
\]

2. Visto 5 veces, acertado todas las veces:

\[
w = 1 - \frac{5}{5} = 0 \Rightarrow \max(0.1, 0) = 0.1
\]


