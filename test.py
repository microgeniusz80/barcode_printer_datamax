from sklearn.datasets import make_circles
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


n_samples = 1000

X, y = make_circles(n_samples, noise=0.03, random_state=42)

# print(X.shape, y.shape)  # (1000, 2) (1000,)

circles = pd.DataFrame(
    {
        'X0': X[:, 0],
        'X1': X[:, 1],
        'label': y
    }
)

tf.random.set_seed(42)

model_1 = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model_1.compile(
    loss=tf.keras.losses.BinaryCrossentropy(),
    optimizer=tf.keras.optimizers.Adam(),
    metrics=['accuracy']
)

model_1.fit(X, y, epochs=10)
# model_1.evaluate(X, y)
# data = model_1.summary()
# print(data)

x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
print(x_min, x_max, y_min, y_max)

xx, yy = np.meshgrid(
    np.linspace(x_min, x_max, 100),
    np.linspace(y_min, y_max, 100)
)

x_in = np.c_[xx.ravel(), yy.ravel()]


y_pred = model_1.predict([[-2.05950246, -2.06776832]])
print(y_pred)



# plt.scatter(
#     X[:,0],
#     X[:,1],
#     c=y,
#     cmap='RdYlBu',
# )

# plt.show()


# a = np.array([1, 2, 3, 4, 5]) 
# print(a)
# print(X[0])
# print(y)