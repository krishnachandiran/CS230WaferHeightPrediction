from __future__ import division
import torch
import math
import random
from PIL import Image, ImageOps
import numpy as np
import numbers
import types
import scipy.ndimage as ndimage



class Compose(object):

    def __init__(self, co_transforms):
        self.co_transforms = co_transforms

    def __call__(self, input, target_depth, target_label=None):
        for i, t in enumerate(self.co_transforms):
            # print('After transform {}'.format(i))
            # print(np.max(target_label))
            if target_label == None:
                input, target_depth, _ = t(input, target_depth, target_depth)
                return input, target_depth
            else:
                input, target_depth, target_label = t(input, target_depth, target_label)
                return input, target_depth, target_label


class ArrayToTensor(object):
    """Converts a numpy.ndarray (H x W x C) to a torch.FloatTensor of shape (C x H x W)."""

    def __call__(self, array):
        assert (isinstance(array, np.ndarray))
        # handle numpy array
        try:
            tensor = torch.from_numpy(array).permute(2, 0, 1)
        except:
            tensor = torch.from_numpy(np.expand_dims(array, axis=2)).permute(2, 0, 1)
        # put it from HWC to CHW format
        return tensor.float()


class Scale_Single(object):
    """ Rescales a single object, for example only the ground truth dpeth map """

    def __init__(self, size, order=2):
        self.size = size
        self.order = order

    def __call__(self, inputs):
        h, w = inputs.shape

        if (w <= h and w == self.size) or (h <= w and h == self.size):
            return inputs

        if w < h:
            ratio = self.size / w
        else:
            ratio = self.size / h

        inputs = ndimage.interpolation.zoom(inputs, ratio, order=self.order)

        return inputs


class Scale(object):

    def __init__(self, size, order=2):
        self.size = size
        self.order = order

    def __call__(self, inputs, target_depth=None, target_label=None):
        h, w, _ = inputs.shape

        if (w <= h and w == self.size) or (h <= w and h == self.size):
            if target_depth is not None and target_labels is not None:
                return inputs, target_depth, target_labels
            elif target_depth is not None:
                return inputs, target_depth
            elif target_labels is not None:
                return inputs, target_labels

        if w < h:
            ratio = self.size / w
        else:
            ratio = self.size / h

        inputs = np.stack((ndimage.interpolation.zoom(inputs[:, :, 0], ratio, order=self.order),
                           ndimage.interpolation.zoom(inputs[:, :, 1], ratio, order=self.order), \
                           ndimage.interpolation.zoom(inputs[:, :, 2], ratio, order=self.order)), axis=2)

        if target_label is not None and target_depth is not None:

            target_label = ndimage.interpolation.zoom(target_label, ratio, order=self.order)
            target_depth = ndimage.interpolation.zoom(target_depth, ratio, order=self.order)
            return inputs, target_depth, target_label

        elif target_depth is not None:
            target_depth = ndimage.interpolation.zoom(target_depth, ratio, order=self.order)
            return inputs, target_depth

        elif target_label is not None:
            target_label = ndimage.interpolation.zoom(target_label, ratio, order=self.order)
            return inputs, target_label

        else:
            return inputs