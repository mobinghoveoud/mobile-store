# Brand Views - Technical Document

> Note: You can find the implementation of these views in the [brand_view.py](../../../src/mobiles/views/brand_view.py) file.

## Table of Contents

+ [Brand List View](#brand-list-view)
+ [Brand Create View](#brand-create-view)
+ [Brand Update View](#brand-update-view)
+ [Brand Delete View](#brand-delete-view)

## Brand List View

The `BrandListView` displays a paginated list of all mobile brands available in the system.

### URLs

- URL: `/mobiles/brand/`
- HTTP Method: `GET`
- Name: `mobiles:brand-list`

### Template

- Template: `mobiles/brand/list.html`

### Functionality

- Retrieves all mobile brands from the database.
- Paginates the list to display 10 brands per page.
- Renders the `list.html` template with the paginated data.

## Brand Create View

The `BrandCreateView` provides functionality to create a new mobile brand.

### URLs

- URL: `/mobiles/brand/create/`
- HTTP Method: `GET`, `POST`
- Name: `mobiles:brand-create`

### Template

- Template: `mobiles/brand/form.html`

### Form

- Form: `BrandForm`

### Functionality

- Renders an empty `BrandForm` for creating a new mobile brand.
- On successful form submission, saves the new brand to the database and redirects to the `Brand List View`.
- If the form submission is invalid, re-renders the `form.html` template with the populated form and error messages.

## Brand Update View

The `BrandUpdateView` provides functionality to update an existing mobile brand.

### URLs

- URL: `/mobiles/brand/update/<int:pk>/`
- HTTP Method: `GET`, `POST`
- Name: `mobiles:brand-update`

### Template

- Template: `mobiles/brand/form.html`

### Form

- Form: `BrandForm`

### Functionality

- Retrieves the mobile brand with the given `pk` from the database.
- Renders a populated `BrandForm` with the retrieved brand for updating.
- On successful form submission, saves the updated brand to the database and redirects to the `Brand List View`.
- If the form submission is invalid, re-renders the `form.html` template with the populated form and error messages.

## Brand Delete View

The `BrandDeleteView` provides functionality to delete an existing mobile brand.

### URLs

- URL: `/mobiles/brand/delete/<int:pk>/`
- HTTP Method: `POST`
- Name: `mobiles:brand-delete`

### Functionality

- Retrieves the mobile brand with the given primary key (`pk`) from the database.
- Deletes the retrieved brand from the database.
- Redirects to the `Brand List View` after successful deletion.
