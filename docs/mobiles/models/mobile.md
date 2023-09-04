# Mobile Model - Technical Document

> Note: You can find the implementation of this model in the [models.py](../../../src/mobiles/models.py) file.

## Mobile Model

The `Mobile` model inherits from the `BaseModel`, which provides common fields and functionalities for tracking creation
and update times. The model includes the following fields:

### Fields

| Field Name | Field Type                | Description                                                                                   |
|------------|---------------------------|-----------------------------------------------------------------------------------------------|
| `brand`    | ForeignKey to Brand       | The brand associated with the mobile model. (Related name: `mobiles`, On-Delete: `Cascade`)   |
| `model`    | CharField                 | The model name of the mobile. (Max length: 150, Unique)                                       |
| `country`  | ForeignKey to Nationality | The country associated with the mobile model. (Related name: `mobiles`, On-Delete: `Protect`) |
| `updated`  | DateTimeField             | The last time the instance was updated.                                                       |
| `created`  | DateTimeField             | The creation time of the instance.                                                            |

### Manager

The `Mobile` model is associated with a custom manager called `MobileManager`. The custom manager provides a custom
queryset method to optimize database queries by select_related `Brand` and `Nationality` objects when fetching `Mobile`
objects.

> Note: You can find the implementation of this manager in the [managers.py](../../../src/mobiles/managers.py) file.
