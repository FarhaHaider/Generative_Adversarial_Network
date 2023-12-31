from keras.optimizers import Adam, RMSprop
from shutil import copyfile
import os
from keras.preprocessing.image import load_img ,img_to_array
import matplotlib.pyplot as plt
import keras
from keras import layers
import os
import tensorflow as tf
from keras.layers import BatchNormalization
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from keras.utils.vis_utils import plot_model
import numpy as np
from skimage.io import imread
from skimage.transform import resize
import numpy as np
from tqdm import tqdm_notebook
import os
from keras.preprocessing import image
from tqdm import tqdm_notebook

latent_dim = 100
height = 64
width = 64

channels = 3
import keras
from keras import layers
import os
import tensorflow as tf
from keras.layers import BatchNormalization

generator_input = keras.Input(shape=(latent_dim,))
x = layers.Dense(128 * 32 * 32)(generator_input)
x = layers.LeakyReLU()(x)
x = layers.Reshape((32, 32, 128))(x)
x = layers.Conv2D(256, 5, padding='same')(x)
x = layers.LeakyReLU()(x)
x = layers.Conv2DTranspose(256, 4, strides=2, padding='same')(x)
x = layers.LeakyReLU()(x)
x = layers.Conv2D(256, 5, padding='same')(x)
x = layers.LeakyReLU()(x)
x = layers.Conv2D(256, 5, padding='same')(x)
x = layers.LeakyReLU()(x)
x = layers.Conv2D(channels, 7, activation='tanh', padding='same')(x)
generator = keras.models.Model(generator_input, x)
generator.summary()


discriminator_input = layers.Input(shape=(height, width, channels))
x = layers.Conv2D(128, 3)(discriminator_input)
x = layers.LeakyReLU()(x)
x = layers.Conv2D(128, 4, strides=2)(x)
x = layers.LeakyReLU()(x)
x = layers.Conv2D(128, 4, strides=2)(x)
x = layers.LeakyReLU()(x)
x = layers.Conv2D(128, 4, strides=2)(x)
x = layers.LeakyReLU()(x)
x = layers.Flatten()(x)
x = layers.Dropout(0.4)(x)
x = layers.Dense(1, activation=sigmoid)(x)
discriminator = keras.models.Model(discriminator_input, x)
discriminator.summary()

discriminator_optimizer = keras.optimizers.RMSprop(lr=0.0008, clipvalue=1.0,
decay=1e-8)
discriminator.compile(optimizer=discriminator_optimizer, loss=binary_crossentropy)
discriminator.trainable = False
gan_input = keras.Input(shape=(latent_dim,))

gan_output = discriminator(generator(gan_input))
gan = keras.models.Model(gan_input, gan_output)
gan_optimizer = keras.optimizers.RMSprop(lr=0.0004, clipvalue=1.0, decay=1e-8)
gan.compile(optimizer=gan_optimizer, loss=binary_crossentropy)
gan.summary()

from skimage.transform import rescale
list_file = os.listdir('/data')
# random.shuffle(list_file)
data_train_gan = np.array([resize(imread(os.path.join('/data',file_name)), (64, 64, 3)) for file_name in list_file])
data_train_gan.shape
x_train =data_train_gan
iterations = 20000
batch_size = 36
save_dir = '.';
start = 0
import matplotlib.pyplot as plt

for step in tqdm_notebook(range(iterations)):
random_latent_vectors = np.random.normal(size = (batch_size, latent_dim)


generated_images = generator.predict(random_latent_vectors)
stop = start + batch_size
real_images = x_train[start: stop]

combined_images = np.concatenate([generated_images, real_images])
# combined_images = np.concatenate([generated_images,real_images[:,-1]], axis=1)
labels = np.concatenate([np.ones((batch_size,1)), np.zeros((batch_size, 1))])
labels += 0.05 * np.random.random(labels.shape)
d_loss = discriminator.train_on_batch(combined_images, labels)
random_latent_vectors = np.random.normal(size=(batch_size, latent_dim))
misleading_targets = np.zeros((batch_size, 1))
a_loss = gan.train_on_batch(random_latent_vectors, misleading_targets)
start += batch_size

if start &gt; len(x_train) - batch_size:
start = 0

if step % 10 == 0:
print('discriminator loss:', d_loss)
print('advesarial loss:', a_loss)
fig, axes = plt.subplots(2, 2)

fig.set_size_inches(2,2)
count = 0
for i in range(2):
for j in range(2):
axes[i, j].imshow(resize(generated_images[count], (64,64)))
axes[i, j].axis('off')
count += 1
plt.show()

if step % 100 == 0:
gan.save_weights(model.h5)

print('discriminator loss:', d_loss)
print('adversarial loss:', a_loss)
