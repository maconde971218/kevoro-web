"""Build a downloadable review bundle without deploying it or including repo internals."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PARTS = ('index.html', 'assets', 'marca', 'instagram', 'scripts/preview.mjs', 'package.json')
README = '''KEVORO — VISTA PREVIA PARA REVISIÓN

Este paquete no publica nada. Marca y contenido social están pendientes del CEO.
No contiene pacientes, contraseñas, sesiones ni conexiones a servicios reales.

Para abrir las tres páginas con sus interacciones:
1. Extraer esta carpeta.
2. Con Node.js instalado, abrir una terminal en esta carpeta y ejecutar: npm run dev
3. Abrir http://localhost:3000/ (web), http://localhost:3000/marca/ (marca)
   y http://localhost:3000/instagram/ (contenido para revisar).
4. Terminar el servidor con Ctrl+C.

No hace falta npm install. Abrir el HTML con doble clic no carga los módulos y
el contenido JSON de las galerías: usa el servidor local indicado.
La configuración de WhatsApp está vacía; los botones muestran contacto por correo.
El formulario prepara un borrador: no lo envía ni guarda datos.

Las capturas, trazas y resultados de pruebas se entregan en otro artefacto del PR.
preview-manifest.json contiene las huellas SHA-256 de los archivos de este ZIP.
'''


def build_archive(output, root=ROOT):
    files = []
    for relative in PUBLIC_PARTS:
        path = root / relative
        if path.is_symlink():
            raise ValueError(f'Symlinks are not allowed in the preview: {relative}')
        if not path.exists():
            raise ValueError(f'Missing preview file: {relative}')
        candidates = path.rglob('*') if path.is_dir() else [path]
        for candidate in candidates:
            if candidate.is_symlink():
                raise ValueError(f'Symlinks are not allowed in the preview: {candidate.relative_to(root)}')
            if candidate.is_file():
                if any(part.startswith('.') for part in candidate.relative_to(root).parts):
                    raise ValueError('Hidden files are not allowed in the public preview')
                files.append(candidate)
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = {}
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        for path in sorted(files):
            relative = str(path.relative_to(root))
            data = path.read_bytes()
            archive.writestr('kevoro-preview/' + relative, data)
            manifest[relative] = hashlib.sha256(data).hexdigest()
        archive.writestr('kevoro-preview/README-PREVIEW.txt', README)
        archive.writestr('kevoro-preview/preview-manifest.json', json.dumps(manifest, indent=2) + '\n')
    with ZipFile(output) as archive:
        invalid = archive.testzip()
        if invalid:
            raise ValueError('Invalid ZIP member: ' + invalid)
    return len(files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    count = build_archive(args.output)
    print(f'Preview ZIP verified: {args.output} ({count} public files; no deployment)')
