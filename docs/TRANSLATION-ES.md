# PKForge · Traducción comunitaria al español

Esta rama añade el selector **Ajustes → Idioma / Language**, sin modificar los identificadores de menú ni los datos de partida.

## Idiomas

- Inglés (predeterminado).
- Español (en desarrollo).
- La preferencia local ui_language conserva la elección. Los textos aún no traducidos aparecen en inglés.

## Seguridad y límites

- Esta edición usa el paquete Android `org.pkforge.app.es`, independiente del oficial.
- No instala automáticamente los APK oficiales, que tienen otro paquete y firma.
- Cada ejecución del workflow genera una firma de prueba. Para cambiar de APK de pruebas, puede ser necesario desinstalar la edición española anterior. Haz copia de cualquier dato importante antes.
- Conserva copias de tus partidas antes de editarlas.
- La localización es parcial: quedan mensajes dinámicos y pantallas por traducir.

## Compilación

En Actions, abre la ejecución correcta de PKForge Spanish APK y descarga el artefacto PKForge-ES-APK. El ZIP contiene el APK.

## Para contribuir

Las traducciones están en src/PKForge.App/Services/AppLanguage.cs. Los nombres internos de opciones deben continuar en inglés, aunque la interfaz los muestre en español.

Traducción comunitaria no oficial basada en https://github.com/sofianeelhor/PKForge.
