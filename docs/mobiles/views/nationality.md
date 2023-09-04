# Nationality Views

> Note: You can find the implementation of these views in the [nationality_view.py](../../../src/mobiles/views/nationality_view.py) file.

## Table of Contents

+ [Nationality List View](#nationality-list-view)
+ [Nationality Create View](#nationality-create-view)
+ [Nationality Update View](#nationality-update-view)
+ [Nationality Delete View](#nationality-delete-view)

## Nationality List View

The `NationalityListView` displays a paginated list of all nationalities available in the system.

### URLs

- URL: `/mobiles/nationality/`
- HTTP Method: `GET`
- Name: `mobiles:nationality-list`

### Template

- Template: `mobiles/nationality/list.html`

### Functionality

- Retrieves all nationalities from the database.
- Paginates the list to display 10 nationalities per page.
- Renders the `list.html` template with the paginated data.

## Nationality Create View

The `NationalityCreateView` provides functionality to create a new nationality.

### URLs

- URL: `/mobiles/nationality/create/`
- HTTP Method: `GET`, `POST`
- Name: `mobiles:nationality-create`

### Template

- Template: `mobiles/nationality/form.html`

### Form

- Form: `NationalityForm`

### Functionality

- Renders an empty `NationalityForm` for creating a new nationality.
- On successful form submission, saves the new nationality to the database and redirects to the `Nationality List View`.
- If the form submission is invalid, re-renders the `form.html` template with the populated form and error messages.

## Nationality Update View

The `NationalityUpdateView` provides functionality to update an existing nationality.

### URLs

- URL: `/mobiles/nationality/update/<int:pk>/`
- HTTP Method: `GET`, `POST`
- Name: `mobiles:nationality-update`

### Template

- Template: `mobiles/nationality/form.html`

### Form

- Form: `NationalityForm`

### Functionality

- Retrieves the nationality with the given `pk` from the database.
- Renders a populated `NationalityForm` with the retrieved nationality for updating.
- On successful form submission, saves the updated nationality to the database and redirects to
  the `Nationality List View`.
- If the form submission is invalid, re-renders the `form.html` template with the populated form and error messages.

## Nationality Delete View

The `NationalityDeleteView` provides functionality to delete an existing nationality.

### URLs

- URL: `/mobiles/nationality/delete/<int:pk>/`
- HTTP Method: `POST`
- Name: `mobiles:nationality-delete`

### Functionality

- Retrieves the nationality with the given primary key (`pk`) from the database.
- Deletes the retrieved nationality from the database.
- Redirects to the `Nationality List View` after successful deletion.
