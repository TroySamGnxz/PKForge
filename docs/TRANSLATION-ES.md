# PKForge · Traducción comunitaria al español

Esta rama añade el selector **Ajustes → Idioma / Language**, sin modificar los identificadores de menú ni los datos de partida.

## Idiomas

- Español (predeterminado en esta compilación comunitaria).
- Inglés (disponible desde Ajustes).
- La preferencia local ui_language conserva la elección. Los textos aún no traducidos aparecen en inglés.

## Seguridad y límites

- Esta edición usa el paquete Android `org.pkforge.app.es`, independiente del oficial.
- No instala automáticamente los APK oficiales, que tienen otro paquete y firma.
- A partir de la V6, el workflow reutiliza una identidad de firma propia con `actions/cache` y guarda una copia de recuperación cifrada. **La V5 y anteriores están firmadas con otra clave y necesitan una única reinstalación**, exportando previamente los datos de la app.
- La caché de GitHub puede caducar, así que conserva fuera del repositorio un respaldo privado de la clave y su contraseña. Nunca publiques el almacén de claves ni el archivo de contraseña.
- Comprueba que los siguientes APK tengan el mismo SHA-256 de certificado que la V6 antes de instalarlos encima.
- Conserva copias de tus partidas antes de editarlas.
- La localización es parcial: quedan mensajes dinámicos y pantallas por traducir.

## Compilación

En Actions, abre la ejecución correcta de PKForge Spanish APK y descarga el artefacto PKForge-ES-APK. El ZIP contiene el APK.

## Para contribuir

Las traducciones de interfaz están en `src/PKForge.App/Services/AppLanguage.cs`. Los nombres internos de opciones deben continuar en inglés, aunque la interfaz los muestre en español.

Los nombres oficiales de especies, movimientos, habilidades, objetos, naturalezas y Poké Balls proceden de las tablas españolas de PKHeX en `GameDataService.cs`. Los textos y entradas de Pokédex se generan en CI mediante `tools/DexFacts/build_es.py` desde datos de PokeAPI (BSD-3-Clause), con inglés de respaldo. Los recursos españoles son de presentación y **no** alteran el formato de las partidas.

Traducción comunitaria no oficial basada en https://github.com/sofianeelhor/PKForge.
