# Estructura del documento de tesis

Estado: estructura base adoptada el 10 de septiembre de 2026.

## Criterio institucional

La UIS no prescribe un índice académico único para todos los trabajos de grado.
El instructivo de autoarchivo actualizado en julio de 2026 establece que la
estructura del contenido la define la Escuela y que el documento debe aplicar
uniformemente una norma de citación. El Comité de Trabajos de Grado de la EISI
es la instancia que define las características del informe final de Tesis II.

Esta estructura se apoya en:

- Biblioteca UIS, [entrega de trabajos de grado](https://biblioteca.uis.edu.co/entrega-trabajos-de-grado/index.html);
- Biblioteca UIS, [instructivo de autoarchivo, julio de 2026](https://documentos.uis.edu.co/wp-content/uploads/2026/07/instructivo-de-autoarchivo-de-trabajos-de-grado-y-tesis-doctorales.pdf);
- EISI, [Comité de Trabajos de Grado](https://ingsistemas.uis.edu.co/eisi/lector1.jsp?IdMenu=S95);
- un [trabajo de investigación de Ingeniería de Sistemas depositado en 2025](https://noesis.uis.edu.co/server/api/core/bitstreams/3930e61e-699d-424c-b455-bc6ecfdbc2df/content), usado solo como precedente de organización;
- el plan de Tesis I aprobado, conservado en `plan/`.

No se adopta un límite de páginas tomado de otra Escuela: no se encontró un
máximo general vigente publicado por la EISI. Antes de la entrega se debe
confirmar con el director o el Comité si existe una instrucción interna más
específica.

## Orden adoptado

| Orden | Parte | Archivo | Estado |
| --- | --- | --- | --- |
| 1 | Portada | `thesis/frontmatter/portada.tex` | Base lista |
| 2 | Portadilla | `thesis/frontmatter/portadilla.tex` | Base lista; verificar título académico del director |
| 3 | Dedicatoria | Por crear si se desea | Opcional |
| 4 | Agradecimientos | Por crear si se desea | Opcional |
| 5 | Contenido | Generado desde `thesis/main.tex` | Listo |
| 6 | Lista de figuras | Generada desde `thesis/main.tex` | Lista |
| 7 | Lista de tablas | Generada desde `thesis/main.tex` | Lista |
| 8 | Resumen | `thesis/frontmatter/resumen.tex` | Reutilizado; reescritura final pendiente |
| 9 | Abstract | `thesis/frontmatter/abstract.tex` | Reutilizado; traducir desde el resumen final |
| 10 | Introducción, sin numerar | `thesis/chapters/00_introduccion.tex` | Reutilizar y actualizar |
| 11 | 1. Planteamiento del problema y justificación | `thesis/chapters/01_planteamiento_problema.tex` | Reutilizar y ajustar al alcance real |
| 12 | 2. Objetivos | `thesis/chapters/02_objetivos.tex` | Conservar los aprobados salvo cambio formal |
| 13 | 3. Marco de referencia | `thesis/chapters/03_marco_referencia.tex` | Reorganizar y actualizar bibliografía |
| 14 | 4. Metodología | `thesis/chapters/04_metodologia.tex` | Reescribir como trabajo ejecutado |
| 15 | 5. Resultados | `thesis/chapters/05_resultados.tex` | Integrar evidencia aceptada |
| 16 | 6. Discusión | `thesis/chapters/06_discusion.tex` | Nuevo |
| 17 | 7. Conclusiones | `thesis/chapters/07_conclusiones.tex` | Nuevo |
| 18 | 8. Trabajo futuro | `thesis/chapters/08_trabajo_futuro.tex` | Nuevo |
| 19 | Bibliografía | Generada desde `thesis/references.bib` | Depurar y completar |
| 20 | Apéndices | Por incorporar si aportan reproducibilidad | Opcional |

La separación entre resultados y discusión facilita distinguir evidencia de
interpretación. El precedente EISI consultado combina ambas partes, pero la
norma institucional no obliga a hacerlo.

La portada y la portadilla son páginas distintas de manera intencional. La
primera identifica el trabajo, el autor y la institución; la segunda repite
esos datos e incorpora el propósito académico y la dirección, siguiendo la
organización observada en el precedente EISI y en las instrucciones de
autoarchivo consultadas.

## Reutilización del plan aprobado

Principio de edición: la tesis se construye transformando el plan, no
reescribiéndolo desde cero. Se conserva cada párrafo que siga siendo preciso y
se modifica únicamente lo necesario para pasar de propuesta a trabajo
ejecutado, actualizar evidencia o corregir alcance y precisión. El contenido
nuevo debe mantener la voz expositiva, el nivel de detalle y la terminología
del plan, sin reproducir sus errores gramaticales, afirmaciones desactualizadas
o promesas que los experimentos no sostienen.

| Contenido del plan | Destino en la tesis | Acción |
| --- | --- | --- |
| Motivación e introducción | Introducción | Reutilizar, actualizar cifras y eliminar lenguaje de propuesta |
| Planteamiento y justificación | Capítulo 1 | Reutilizar; ajustar la pregunta al modelo y evidencia finales |
| Objetivos | Capítulo 2 | Preservar texto aprobado; comprobar cumplimiento uno a uno |
| Fundamentos | Capítulo 3 | Reutilizar selectivamente y corregir precisión técnica |
| Trabajos previos | Capítulo 3 | Actualizar estado del arte y separar antecedentes de fundamentos |
| Metodología propuesta | Capítulo 4 | Usar como trazabilidad, no como texto final; describir lo ejecutado |
| Aspectos éticos | Sección 4.9 | Reutilizar después de verificar datos, licencias y desidentificación reales |
| Cronograma y presupuesto | Ninguno | Permanecen únicamente en el plan de Tesis I |
| Resumen y abstract | Hojas preliminares | Reescribir al finalizar resultados y conclusiones |

## Distribución de la evidencia experimental

- La metodología describe conjuntos de datos, preprocesamiento, modelos,
  entrenamiento, protocolos, métricas y trazabilidad.
- Resultados contiene reconstrucción, clasificación a nivel de WSI,
  segmentación de WSI a resolución de parche y análisis del espacio latente.
- La segmentación por parches se presenta como una grilla sobre la WSI; su
  evaluación no es exhaustiva porque no existen etiquetas densas para toda la
  lámina.
- Discusión conecta las cuatro líneas de evidencia, responde la pregunta de
  investigación y explicita limitaciones y amenazas a la validez.
- Conclusiones responde los objetivos; trabajo futuro no puede contener tareas
  necesarias para sostener conclusiones actuales.

## Decisiones pendientes de confirmación humana

1. Verificar la denominación completa del título académico del director para la
   portadilla y las notas del resumen.
2. Decidir si se incluirán dedicatoria y agradecimientos.
3. Confirmar con el director o el Comité EISI que se mantendrá IEEE como norma
   de citación. Se conserva provisionalmente porque el plan aprobado y trabajos
   recientes de la Escuela utilizan referencias numéricas.
4. Revisar si el título y los objetivos aprobados requieren una modificación
   formal por diferencias entre el protocolo y los experimentos ejecutados.
