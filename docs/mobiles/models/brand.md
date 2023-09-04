# Brand Model

> Note: You can find the implementation of this model in the [models.py](../../../src/mobiles/models.py) file.

## Brand Model

The `Brand` model inherits from the `BaseModel`, which provides common fields and functionalities for tracking creation
and update times. The model includes the following fields:

### Fields

| Field Name    | Field Type                | Description                                                                               |
|---------------|---------------------------|-------------------------------------------------------------------------------------------|
| `name`        | CharField                 | The name of the brand. (Max length: 150)                                                  |
| `nationality` | ForeignKey to Nationality | The nationality associated with the brand. (Related name: `brands`, On-Delete: `Protect`) |
| `updated`     | DateTimeField             | The last time the instance was updated.                                                   |
| `created`     | DateTimeField             | The creation time of the instance.                                                        |

### Manager

The `Brand` model is associated with a custom manager called `BrandManager`. The custom manager provides a custom
queryset method to optimize database queries by select_related `Nationality` objects when fetching `Brand`
objects.

> Note: You can find the implementation of this manager in the [managers.py](../../../src/mobiles/managers.py) file.
