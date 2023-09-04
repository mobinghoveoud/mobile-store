# Variant Model

> Note: You can find the implementation of this model in the [models.py](../../../src/mobiles/models.py) file.

## Variant Model

The `Variant` model inherits from the `BaseModel`, which provides common fields and functionalities for tracking
creation and update times. The model includes the following fields:

### Fields

| Field Name | Field Type             | Description                                                                                    |
|------------|------------------------|------------------------------------------------------------------------------------------------|
| `mobile`   | ForeignKey to Mobile   | The mobile model associated with the variant. (Related name: `variants`, On-Delete: `Cascade`) |
| `color`    | CharField              | The color of the mobile variant. (Max length: 100)                                             |
| `size`     | FloatField             | The screen size of the mobile variant. (Min value: 1)                                          |
| `image`    | ImageField             | The image of the mobile variant. (Image file name: Mobile model name + UUID)                   |
| `updated`  | DateTimeField          | The last time the instance was updated.                                                        |
| `created`  | DateTimeField          | The creation time of the instance.                                                             |

### Manager

The `Variant` model is associated with a custom manager called `VariantManager`. The custom manager provides a custom
queryset method to optimize database queries by select_related `Mobile` objects when fetching `Variant` objects.

> Note: You can find the implementation of this manager in the [managers.py](../../../src/mobiles/managers.py) file.

### Image Upload Path Function

The `mobile_image_path()` function is used to determine the upload path for the `image` field of the `Variant` model.
The function generates a unique path based on the mobile model name and a random UUID to prevent filename collisions and
maintain uniqueness for each uploaded image.

### Signals

The `Variant` model includes two signals, `pre_save` and `post_delete`, which are used to handle automatic deletion of
images associated with variant instances.

> Note: You can find the implementation of these signals in the [signals.py](../../../src/mobiles/signals.py) file.

+ `auto_delete_image_on_delete`: This signal is triggered after a `Variant` instance is deleted. When a `Variant`
  instance is deleted, the associated image file is automatically deleted from the storage to avoid orphaned files.

+ `auto_delete_image_on_change`: This signal is triggered before a `Variant` instance is saved. If the `image`
  field has changed, the signal will automatically delete the old image associated with the variant to keep the storage
  clean from unused images.
