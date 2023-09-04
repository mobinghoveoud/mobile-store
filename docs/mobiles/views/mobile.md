# Mobile Views

> Note: You can find the implementation of these views in the [mobile_view.py](../../../src/mobiles/views/mobile_view.py) file.

## Table of Contents

+ [Mobile List View](#mobile-list-view)
+ [Mobile Create View](#mobile-create-view)
+ [Mobile Update View](#mobile-update-view)
+ [Mobile Delete View](#mobile-delete-view)

## Mobile List View

The `MobileListView` displays a paginated list of all mobile models available in the system.

### URLs

- URL: `/mobiles/mobile/`
- HTTP Method: `GET`
- Name: `mobiles:mobile-list`

### Template

- Template: `mobiles/mobile/list.html`

### Functionality

- Retrieves all mobile models from the database.
- Paginates the list to display 10 mobile models per page.
- Renders the `list.html` template with the paginated data.

## Mobile Create View

The `MobileCreateView` provides functionality to create a new mobile model.

### URLs

- URL: `/mobiles/mobile/create/`
- HTTP Method: `GET`, `POST`
- Name: `mobiles:mobile-create`

### Template

- Template: `mobiles/mobile/form.html`

### Form

- Form: `MobileForm`

### Functionality

- Renders an empty `MobileForm` for creating a new mobile model.
- On successful form submission, saves the new mobile model to the database and redirects to the `Mobile List View`.
- If the form submission is invalid, re-renders the `form.html` template with the populated form and error messages.

## Mobile Update View

The `MobileUpdateView` provides functionality to update an existing mobile model.

### URLs

- URL: `/mobiles/mobile/update/<int:pk>/`
- HTTP Method: `GET`, `POST`
- Name: `mobiles:mobile-update`

### Template

- Template: `mobiles/mobile/form.html`

### Form

- Form: `MobileForm`

### Functionality

- Retrieves the mobile model with the given `pk` from the database.
- Renders a populated `MobileForm` with the retrieved mobile model for updating.
- On successful form submission, saves the updated mobile model to the database and redirects to the `Mobile List View`.
- If the form submission is invalid, re-renders the `form.html` template with the populated form and error messages.

## Mobile Delete View

The `MobileDeleteView` provides functionality to delete an existing mobile model.

### URLs

- URL: `/mobiles/mobile/delete/<int:pk>/`
- HTTP Method: `POST`
- Name: `mobiles:mobile-delete`

### Functionality

- Retrieves the mobile model with the given primary key (`pk`) from the database.
- Deletes the retrieved mobile model from the database.
- Redirects to the `Mobile List View` after successful deletion.
