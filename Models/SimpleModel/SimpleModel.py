import Models.SimpleModel.SimpleModelDatasetBuilder as SimpleModelDatasetBuilder

from keras import *
import numpy as np


class SimpleModel(object):

    def train(self):
        dataset_builder = SimpleModelDatasetBuilder.SimpleModelDataSetBuilder()
        dataset_path = dataset_builder.prepare_dataset()

        data = np.load(dataset_path)
        x = data['x']
        y = data['y']

        min_inputs = Input(shape=(250, 4), name='minute_inputs')
        min_conv1_1 = layers.Conv1D(50, 50, padding='same')(min_inputs)
        min_conv1_2 = layers.Conv1D(50, 21, padding='same')(min_inputs)
        min_conv1_3 = layers.Conv1D(50, 11, padding='same')(min_inputs)
        min_conv1 = layers.concatenate([min_conv1_1, min_conv1_2, min_conv1_3])
        min_conv2_1 = layers.Conv1D(50, 50, padding='same')(min_conv1)
        min_conv2_2 = layers.Conv1D(50, 21, padding='same')(min_conv1)
        min_conv2_3 = layers.Conv1D(50, 11, padding='same')(min_conv1)
        min_conv2 = layers.concatenate([min_conv2_1, min_conv2_2, min_conv2_3])
        min_conv3_1 = layers.Conv1D(50, 50, padding='same')(min_conv2)
        min_conv3_2 = layers.Conv1D(50, 21, padding='same')(min_conv2)
        min_conv3_3 = layers.Conv1D(50, 11, padding='same')(min_conv2)
        min_conv3 = layers.concatenate([min_conv3_1, min_conv3_2, min_conv3_3])
        min_flat1 = layers.Flatten()(min_conv3)
        min_dense1 = layers.Dense(1024, activation='softmax')(min_flat1)
        min_dense2 = layers.Dense(1024, activation='softmax')(min_dense1)

        hour_inputs = Input(shape=(250, 4), name='hour_inputs')
        hour_conv1_1 = layers.Conv1D(50, 50, padding='same')(hour_inputs)
        hour_conv1_2 = layers.Conv1D(50, 21, padding='same')(hour_inputs)
        hour_conv1_3 = layers.Conv1D(50, 11, padding='same')(hour_inputs)
        hour_conv1 = layers.concatenate([hour_conv1_1, hour_conv1_2, hour_conv1_3])
        hour_conv2_1 = layers.Conv1D(50, 50, padding='same')(hour_conv1)
        hour_conv2_2 = layers.Conv1D(50, 21, padding='same')(hour_conv1)
        hour_conv2_3 = layers.Conv1D(50, 11, padding='same')(hour_conv1)
        hour_conv2 = layers.concatenate([hour_conv2_1, hour_conv2_2, hour_conv2_3])
        hour_conv3_1 = layers.Conv1D(50, 50, padding='same')(hour_conv2)
        hour_conv3_2 = layers.Conv1D(50, 21, padding='same')(hour_conv2)
        hour_conv3_3 = layers.Conv1D(50, 11, padding='same')(hour_conv2)
        hour_conv3 = layers.concatenate([hour_conv3_1, hour_conv3_2, hour_conv3_3])
        hour_flat1 = layers.Flatten()(hour_conv3)
        hour_dense1 = layers.Dense(1024, activation='softmax')(hour_flat1)
        hour_dense2 = layers.Dense(1024, activation='softmax')(hour_dense1)

        day_inputs = Input(shape=(250, 4), name='day_inputs')
        day_conv1_1 = layers.Conv1D(50, 50, padding='same')(day_inputs)
        day_conv1_2 = layers.Conv1D(50, 21, padding='same')(day_inputs)
        day_conv1_3 = layers.Conv1D(50, 11, padding='same')(day_inputs)
        day_conv1 = layers.concatenate([day_conv1_1, day_conv1_2, day_conv1_3])
        day_conv2_1 = layers.Conv1D(50, 50, padding='same')(day_conv1)
        day_conv2_2 = layers.Conv1D(50, 21, padding='same')(day_conv1)
        day_conv2_3 = layers.Conv1D(50, 11, padding='same')(day_conv1)
        day_conv2 = layers.concatenate([day_conv2_1, day_conv2_2, day_conv2_3])
        day_conv3_1 = layers.Conv1D(50, 50, padding='same')(day_conv2)
        day_conv3_2 = layers.Conv1D(50, 21, padding='same')(day_conv2)
        day_conv3_3 = layers.Conv1D(50, 11, padding='same')(day_conv2)
        day_conv3 = layers.concatenate([day_conv3_1, day_conv3_2, day_conv3_3])
        day_flat1 = layers.Flatten()(day_conv3)
        day_dense1 = layers.Dense(1024, activation='softmax')(day_flat1)
        day_dense2 = layers.Dense(1024, activation='softmax')(day_dense1)

        merged_concat = layers.concatenate([min_dense2, hour_dense2, day_dense2])
        merged_dense1 = layers.Dense(2048, activation='softmax')(merged_concat)
        merged_dense2 = layers.Dense(2048, activation='softmax')(merged_dense1)
        merged_dense3 = layers.Dense(3, activation='softmax')(merged_dense2)

        model = Model(input=[min_inputs, hour_inputs, day_inputs], outputs=merged_dense3)
        model.compile(optimizer='rmsprop',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        one_hot_labels = utils.to_categorical(y, num_classes=3)
        model.fit(np.split(x, 3, axis=-1), one_hot_labels, epochs=10, batch_size=32)


if __name__ == '__main__':
    simple_model = SimpleModel()
    simple_model.train()