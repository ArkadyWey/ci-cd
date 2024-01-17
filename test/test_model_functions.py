import pytest

import tensorflow as tf

from model_functions import get_keras_model, get_training_set, fit_model


class NeuralNetworkTest(unittest.TestCase):
    def setUp(self):
        self.model = get_keras_model()

    def test_model_output_shape(self):
        image_shape = (1, 28, 28, 1)
        output_shape = (1, 10)
        image = tf.ones(image_shape)
        prediction = self.model.predict(image)
        self.assertEqual(prediction.shape, output_shape)

    def test_layers_number(self):
        expected_layers = 7
        self.assertEqual(len(self.model.layers), expected_layers)

    def test_fit_model(self):
        x_train, y_train = get_training_set()
        initial_bias_weights = (self.model.layers[0].weights[1]).numpy()
        fit_model(self.model, x_train, y_train)
        current_bias_weights = (self.model.layers[0].weights[1]).numpy()
        self.assertNotEqual(initial_bias_weights.tolist(), current_bias_weights.tolist())


if __name__ == '__main__':
    unittest.main()