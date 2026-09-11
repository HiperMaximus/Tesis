# Tesis

Repositorio de los documentos de Tesis I y Tesis II de Maximiliano Garavito
Chtefan.

## Documentos

- `plan/`: plan de trabajo aprobado en Tesis I. Es un documento de referencia
  y no se modifica académicamente.
- `thesis/`: documento activo de Tesis II. Nació a partir del plan y contiene
  capítulos nuevos para resultados, análisis del espacio latente, discusión y
  conclusiones.
- `evidence/`: documentos recibidos de la universidad o del director.
- `artifacts/`: PDFs compilados y listos para consultar desde GitHub.

La estructura académica adoptada, su sustento institucional y la matriz de
reutilización del plan están en `docs/thesis_structure.md`.

Cada documento es autocontenido para poder alojarlo en un proyecto Overleaf
independiente.

## Flujo diario

La tesis está dividida por capítulos en `thesis/chapters/`. En VS Code, las
extensiones recomendadas son LaTeX Workshop y LTeX+. La configuración del repo
compila la tesis incrementalmente al guardar, conserva la caché y nunca limpia
automáticamente.

Para instalar las extensiones desde la terminal:

```bash
code --install-extension james-yu.latex-workshop
code --install-extension ltex-plus.vscode-ltex-plus
```

No se debe ejecutar `watch` al mismo tiempo que la compilación automática de VS
Code: ambos observarían los mismos cambios.

## Comandos

```bash
./scripts/document.sh build plan
./scripts/document.sh build thesis
./scripts/document.sh watch thesis
./scripts/document.sh draft thesis
./scripts/document.sh check plan
./scripts/document.sh check thesis
./scripts/document.sh check-all
./scripts/document.sh lint thesis
./scripts/document.sh grammar thesis
./scripts/document.sh render thesis
./scripts/document.sh clean thesis
```

- `build` reutiliza la caché y actualiza el PDF final solamente si cambió;
- `watch` recompila al guardar hasta presionar `Ctrl-C`;
- `draft` conserva el espacio de las figuras, pero no carga sus archivos y
  escribe únicamente en `build/<documento>-draft/`;
- `check` valida imágenes, referencias y la integridad del PDF final;
- `lint` ejecuta ChkTeX sobre todos los archivos `.tex`;
- `grammar` ejecuta LTeX+ localmente para ortografía y gramática;
- `render` genera PNGs de todas las páginas para revisión visual;
- `clean` se usa solo ante estados extraños de compilación. Conserva la caché
  compartida de TeX y los PDFs de `artifacts/`.

## Trabajar en un solo capítulo

Después de compilar una vez la tesis completa, copie el ejemplo local:

```bash
cp thesis/includeonly.local.tex.example thesis/includeonly.local.tex
```

Edite `thesis/includeonly.local.tex` para elegir uno o varios capítulos y use
`build`, `watch` o la compilación automática de VS Code. El PDF parcial queda en
`build/thesis/main.pdf`; el PDF final de `artifacts/` no se sobrescribe. Antes de
una validación final, elimine el archivo local:

```bash
rm thesis/includeonly.local.tex
./scripts/document.sh check thesis
```

Si cambia la selección mientras `watch` está activo, detenga el proceso con
`Ctrl-C` y vuelva a iniciarlo para aplicar el nuevo alcance.

## LTeX+ para agentes y terminal

LTeX+ no requiere VS Code. El servidor oficial incluye `ltex-cli-plus`, que
revisa archivos desde la terminal y funciona sin conexión después de instalarse.
La instalación reproducible y sin `sudo` queda dentro de `.tools/`:

```bash
./scripts/setup_ltex.sh
./scripts/document.sh grammar thesis
```

Las excepciones de vocabulario científico compartidas por VS Code y la terminal
viven en `.ltex-config.json` y `.vscode/settings.json`.

El análisis, los modelos, los notebooks y los datos permanecen en el repositorio
`equivariant-vae`. Este repositorio recibe únicamente texto, tablas y figuras
finales con procedencia verificable.

## Overleaf

Se usarán dos proyectos: `Tesis I - Plan aprobado` y `Tesis II - Documento de
tesis`. GitHub será la fuente de verdad. La sincronización se añadirá cuando
existan las URL Git de ambos proyectos y enviará exclusivamente `plan/` o
`thesis/`, nunca el repositorio completo.

Quarto es complementario: puede usarse para una versión HTML o un cuaderno de
resultados, pero la tesis oficial se compila desde LaTeX.
