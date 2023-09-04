# Base Model

> Note: You can find the implementation of this model in the [models.py](../../../src/mobiles/models.py) file.

The `BaseModel` is an abstract model that serves as the base model for other models within the application. It provides
common fields and methods that can be inherited and used by other models.

### Fields

- `updated`: `DateTimeField` - Represents the last update time of the model instance.

- `created`: `DateTimeField` - Represents the creation time of the model instance.

### Methods

- `formatted_created()`: Returns a formatted string representation of the `created` field in the
  format `YYYY-MM-DD HH:MM`.

- `formatted_updated()`: Returns a formatted string representation of the `updated` field in the
  format `YYYY-MM-DD HH:MM`.

### Meta Options

The `BaseModel` is an abstract model, and it includes the following `Meta` options:

- `abstract`: This option is set to `True`, indicating that the `BaseModel` is an abstract model and cannot be used to
  create database tables. Instead, it is meant to be inherited by other models.

- `ordering`: The default ordering for model instances based on the `created` field. In this case, the instances are
  ordered in ascending order based on their **creation time**.
