import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import glob
import os.path

module_handle="https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4"
module = hub.load(module_handle)

def load_img(path):
    img = tf.io.read_file(path)
    img = tf.io.decode_png(img, channels=3)
    img = tf.image.resize_with_pad(img, 224, 224)
    img = tf.image.convert_image_dtype(img,tf.float32)[tf.newaxis, ...]
    return img

def create_image_vector_save_to_file(imgPath, outpath):
    img = load_img(imgPath)
    features = module(img)
    feature_set = np.squeeze(features)
    np.savetxt(outpath, feature_set, delimiter=',')


