# Nationality Model

> Note: You can find the implementation of this model in the [models.py](../../../src/mobiles/models.py) file.

## Nationality Model

The `Nationality` model inherits from the `BaseModel`, which provides common fields and functionalities for tracking
creation and update times. The model includes the following fields:

### Fields

| Field Name | Field Type    | Description                                    |
|------------|---------------|------------------------------------------------|
| `name`     | CharField     | The name of the nationality. (Max length: 150) |
| `updated`  | DateTimeField | The last time the instance was updated.        |
| `created`  | DateTimeField | The creation time of the instance.             |
