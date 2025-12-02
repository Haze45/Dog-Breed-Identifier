import tensorflow as tf
import json
import pathlib

DATASET_PATH = 'Images' 
IMG_SIZE = (224, 224) 
BATCH_SIZE = 32
EPOCHS = 10 
VALIDATION_SPLIT = 0.2 
MODEL_SAVE_PATH = 'your_model_transfer.h5'
LABELS_SAVE_PATH = 'labels.json'

print(f"Loading images from: {DATASET_PATH}")
data_dir = pathlib.Path(DATASET_PATH)

if not data_dir.exists():
    print(f"Error: Dataset directory not found at '{DATASET_PATH}'")
    print("Please make sure your dataset folder is structured correctly and the path is right.")
    exit()

ds_train = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=VALIDATION_SPLIT,
    subset="training",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

ds_validation = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=VALIDATION_SPLIT,
    subset="validation",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = ds_train.class_names
num_classes = len(class_names)
print(f"Found {num_classes} classes (breeds).")
# print("Sample breeds:", class_names[:5])

def preprocess_data(image, label):
    # MobileNetV2 expects pixel values in the range [-1, 1]
    preprocessed_image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    return preprocessed_image, label


print("Applying preprocessing to the dataset...")
# Apply the function to both the training and validation datasets
ds_train = ds_train.map(preprocess_data, num_parallel_calls=tf.data.AUTOTUNE)
ds_validation = ds_validation.map(preprocess_data, num_parallel_calls=tf.data.AUTOTUNE)


AUTOTUNE = tf.data.AUTOTUNE
ds_train = ds_train.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
ds_validation = ds_validation.cache().prefetch(buffer_size=AUTOTUNE)

print("Building the model with MobileNetV2 base...")

preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

base_model = tf.keras.applications.MobileNetV2(
    input_shape=IMG_SIZE + (3,),
    include_top=False, 
    weights='imagenet'
)

base_model.trainable = False

# inputs = tf.keras.Input(shape=IMG_SIZE + (3,))
# x = preprocess_input(inputs) 
# x = base_model(x, training=False) 
# x = tf.keras.layers.GlobalAveragePooling2D()(x) 
# x = tf.keras.layers.Dropout(0.2)(x) 
# outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x) 

# model = tf.keras.Model(inputs, outputs)

model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

print("Compiling the model...")
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
model.summary()

print(f"\nStarting training for {EPOCHS} epochs...")
history = model.fit(
    ds_train,
    validation_data=ds_validation,
    epochs=EPOCHS
)
print("Training finished.")


# ---  Save the Trained Model and Labels ---
print(f"Saving model to {MODEL_SAVE_PATH}...")
model.save(MODEL_SAVE_PATH)
print("Model saved successfully.")

labels_dict = {str(i): name for i, name in enumerate(class_names)}

print(f"Saving labels to {LABELS_SAVE_PATH}...")
with open(LABELS_SAVE_PATH, 'w') as f:
    json.dump(labels_dict, f, indent=4)
print("Labels saved successfully.")


