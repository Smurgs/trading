import Models.SimpleModel.SimpleModelDatasetBuilder as SimpleModelDatasetBuilder

from keras import *
import numpy as np


class SimpleModel2(object):

    def train(self):
        dataset_builder = SimpleModelDatasetBuilder.SimpleModelDataSetBuilder()
        dataset_path = dataset_builder.prepare_dataset()

        data = np.load(dataset_path)
        x = data['x']
        y = data['y']

        x = np.split(x, 3, axis=-1)[0]
        x = np.split(x, 4, axis=-1)[0]

        min_inputs = Input(shape=(250, 1), name='minute_inputs')
        min_conv1_1 = layers.Conv1D(30, 50, padding='same')(min_inputs)
        min_conv1_2 = layers.Conv1D(30, 21, padding='same')(min_inputs)
        min_conv1_3 = layers.Conv1D(30, 11, padding='same')(min_inputs)
        min_conv1 = layers.concatenate([min_conv1_1, min_conv1_2, min_conv1_3])
        min_conv1 = layers.MaxPool1D(10)(min_conv1)
        min_conv2_1 = layers.Conv1D(30, 50, padding='same')(min_conv1)
        min_conv2_2 = layers.Conv1D(30, 21, padding='same')(min_conv1)
        min_conv2_3 = layers.Conv1D(30, 11, padding='same')(min_conv1)
        min_conv2 = layers.concatenate([min_conv2_1, min_conv2_2, min_conv2_3])
        min_conv2 = layers.MaxPool1D(5)(min_conv2)
        min_conv3_1 = layers.Conv1D(30, 50, padding='same')(min_conv2)
        min_conv3_2 = layers.Conv1D(30, 21, padding='same')(min_conv2)
        min_conv3_3 = layers.Conv1D(30, 11, padding='same')(min_conv2)
        min_conv3 = layers.concatenate([min_conv3_1, min_conv3_2, min_conv3_3])
        min_conv3 = layers.MaxPool1D(5)(min_conv3)
        min_flat1 = layers.Flatten()(min_conv3)
        min_dense1 = layers.Dense(512, activation='softmax')(min_flat1)
        min_dense2 = layers.Dense(512, activation='softmax')(min_dense1)
        min_dense3 = layers.Dense(3, activation='softmax')(min_dense2)

        model = Model(input=min_inputs, outputs=min_dense3)
        model.compile(optimizer='rmsprop',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        one_hot_labels = utils.to_categorical(y, num_classes=3)

        model.fit(x, one_hot_labels, epochs=3, batch_size=32)

        predictions = model.predict(x)
        np.savez('preds', x=x, y_hat=predictions, y=y)


if __name__ == '__main__':
    simple_model = SimpleModel2()
    simple_model.train()