# Price History Views

> Note: You can find the implementation of these views in the [price_view.py](../../../src/mobiles/views/price_view.py) file.

## Table of Contents

+ [PriceHistory List View](#pricehistory-list-view)
+ [PriceHistory Create View](#pricehistory-create-view)
+ [PriceHistory Update View](#pricehistory-update-view)
+ [PriceHistory Delete View](#pricehistory-delete-view)

## PriceHistory List View

The `PriceHistoryListView` displays a paginated list of all price histories of mobile variants available in the system.
Each price history is related to its corresponding variant and includes information about the variant's mobile model.

### URLs

- URL: `/mobiles/price-history/`
- HTTP Method: `GET`
- Name: `mobiles:price-history-list`

### Template

- Template: `mobiles/price_history/list.html`

### Functionality

- Retrieves all price histories of mobile variants from the database, including their associated variant and mobile
  model information.
- Paginates the list to display 10 price histories per page.
- Renders the `list.html` template with the paginated data.

## PriceHistory Create View

The `PriceHistoryCreateView` provides functionality to create a new price history for a mobile variant.

### URLs

- URL: `/mobiles/price-history/create/`
- HTTP Method: `GET`, `POST`
- Name: `mobiles:price-history-create`

### Template

- Template: `mobiles/price_history/form.html`

### Form

- Form: `PriceHistoryForm`

### Functionality

- Renders an empty `PriceHistoryForm` for creating a new price history.
- On successful form submission, saves the new price history to the database and redirects to
  the `PriceHistory List View`.
- If the form submission is invalid, re-renders the `form.html` template with the populated form and error messages.

## PriceHistory Update View

The `PriceHistoryUpdateView` provides functionality to update an existing price history of a mobile variant.

### URLs

- URL: `/mobiles/price-history/update/<int:pk>/`
- HTTP Method: `GET`, `POST`
- Name: `mobiles:price-history-update`

### Template

- Template: `mobiles/price_history/form.html`

### Form

- Form: `PriceHistoryForm`

### Functionality

- Retrieves the price history with the given `pk` from the database.
- Renders a populated `PriceHistoryForm` with the retrieved price history for updating.
- On successful form submission, saves the updated price history to the database and redirects to
  the `PriceHistory List View`.
- If the form submission is invalid, re-renders the `form.html` template with the populated form and error messages.

## PriceHistory Delete View

The `PriceHistoryDeleteView` provides functionality to delete an existing price history of a mobile variant.

### URLs

- URL: `/mobiles/price-history/delete/<int:pk>/`
- HTTP Method: `POST`
- Name: `mobiles:price-history-delete`

### Functionality

- Retrieves the price history with the given primary key (`pk`) from the database.
- Deletes the retrieved price history from the database.
- Redirects to the `PriceHistory List View` after successful deletion.
