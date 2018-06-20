# JUSTLETIC CODING GUIDELINES

## Logging

- **debug**: Info not needed for regular operation, but useful in development
- **info**: Info that's helpful during regular operation.
- **warning**: Info that could be problematic, but is non-urgent.
- **error**: Info that is important and likely requires prompt attention.
- **critical**: I don't find myself using this in practice, but if you need one higher than error, here it is

## Template architecture

- Extendable templates
    - Only purpose is to be extended. An extendable is never called from a view and other templates never extend a template that is not an extendable
    - **Naming convention:** Start name with double underscore (e.g. `__base.html`)
    - `__base.html` contains the html scaffolding all pages should contain
    - *Layout templates* start with _ _ l _

- Includable templates
    - Only purpose is to be included in page templates
    - Constitute the building blocks of the site that are then glued together in page templates
    - Includable templates should be ready to make it easy to:
        - Use the particular module on multiple pages
        - Override a particular module without having to change other templates

- Page templates
    - Main purpose is to be the glue that holds everything together
    - Page templates are the only type called directly from views
