# PriceHistory Model

> Note: You can find the implementation of this model in the [models.py](../../../src/mobiles/models.py) file.

## PriceHistory Model

The `PriceHistory` model inherits from the `BaseModel`, which provides common fields and functionalities for tracking
creation and update times. The model includes the following fields:

### Fields

| Field Name | Field Type            | Description                                                                                   |
|------------|-----------------------|-----------------------------------------------------------------------------------------------|
| variant    | ForeignKey to Variant | The variant associated with the price history. (Related name: `prices`, On-Delete: `Cascade`) |
| price      | DecimalField          | The price of the variant at a specific date. (Max digit: 9, Min value: 1)                     |
| status     | BooleanField          | The availability status of the variant.                                                       |
| date       | DateField             | The date when the price was recorded. (Default: `now`)                                        |
| updated    | DateTimeField         | The last time the instance was updated.                                                       |
| created    | DateTimeField         | The creation time of the instance.                                                            |

### Manager

The `PriceHistory` model is associated with a custom manager called `PriceHistoryManager`. The custom manager provides a
custom queryset method to optimize database queries by select_related `Variant` objects when fetching `PriceHistory`
objects.

> Note: You can find the implementation of this manager in the [managers.py](../../../src/mobiles/managers.py) file.

### Methods

+ `get_status_display`: Returns a string representation of the availability status of the variant. It returns "
  Available" if the `status` field is `True`, and "Not Available" if the `status` field is `False`.

+ `formatted_date()`: Returns a string representation of the `date` field in the format "YYYY-MM-DD,".
