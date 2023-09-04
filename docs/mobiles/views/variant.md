# Variant Views

> Note: You can find the implementation of these views in the [variant_view.py](../../../src/mobiles/views/variant_view.py) file.

## Table of Contents

+ [Variant List View](#variant-list-view)
+ [Variant Create View](#variant-create-view)
+ [Variant Update View](#variant-update-view)
+ [Variant Delete View](#variant-delete-view)

## Variant List View

The `VariantListView` displays a paginated list of all variants of mobile models available in the system. Each variant
is related to its corresponding mobile model and includes information about the mobile's country and brand.

### URLs

- URL: `/mobiles/variant/`
- HTTP Method: `GET`
- Name: `mobiles:variant-list`

### Template

- Template: `mobiles/variant/list.html`

### Functionality

- Retrieves all variants of mobile models from the database, including their associated mobile model, country, and brand
  information.
- Paginates the list to display 10 variants per page.
- Renders the `list.html` template with the paginated data.

## Variant Create View

The `VariantCreateView` provides functionality to create a new variant for a mobile model.

### URLs

- URL: `/mobiles/variant/create/`
- HTTP Method: `GET`, `POST`
- Name: `mobiles:variant-create`

### Template

- Template: `mobiles/variant/form.html`

### Form

- Form: `VariantForm`

### Functionality

- Renders an empty `VariantForm` for creating a new variant.
- On successful form submission, saves the new variant to the database and redirects to the `Variant List View`.
- If the form submission is invalid, re-renders the `form.html` template with the populated form and error messages.

## Variant Update View

The `VariantUpdateView` provides functionality to update an existing variant of a mobile model.

### URLs

- URL: `/mobiles/variant/update/<int:pk>/`
- HTTP Method: `GET`, `POST`
- Name: `mobiles:variant-update`

### Template

- Template: `mobiles/variant/form.html`

### Form

- Form: `VariantForm`

### Functionality

- Retrieves the variant with the given `pk` from the database.
- Renders a populated `VariantForm` with the retrieved variant for updating.
- On successful form submission, saves the updated variant to the database and redirects to the `Variant List View`.
- If the form submission is invalid, re-renders the `form.html` template with the populated form and error messages.

## Variant Delete View

The `VariantDeleteView` provides functionality to delete an existing variant of a mobile model.

### URLs

- URL: `/mobiles/variant/delete/<int:pk>/`
- HTTP Method: `POST`
- Name: `mobiles:variant-delete`

### Functionality

- Retrieves the variant with the given primary key (`pk`) from the database.
- Deletes the retrieved variant from the database.
- Redirects to the `Variant List View` after successful deletion.
