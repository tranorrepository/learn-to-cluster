#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np

from utils.misc import TextColors, l2norm, read_probs, read_meta


class BasicDataset():
    def __init__(self, name, prefix='data', dim=256, normalize=True, verbose=True):
        self.name = name
        self.dtype=np.float32
        self.normalize = normalize
        if not os.path.exists(prefix):
            raise FileNotFoundError('folder({}) does not exist.'.format(prefix))
        self.prefix = prefix
        self.feat_path = os.path.join(prefix, 'features', name+'.bin')
        self.label_path = os.path.join(prefix, 'labels', name+'.meta')
        self.lb2idxs, self.idx2lb = read_meta(self.label_path, verbose=verbose)
        self.dim = dim
        self.inst_num = len(self.idx2lb)
        self.cls_num = len(self.lb2idxs)
        self.features = read_probs(self.feat_path, self.inst_num, dim, self.dtype, verbose=verbose)
        if self.normalize:
            self.features = l2norm(self.features)

    def info(self):
        print("name:{}{}{}\ninst_num:{}\ncls_num:{}\ndim:{}\nfeat_path:{}\nnormalization:{}{}{}\ndtype:{}".\
                format(TextColors.OKGREEN, self.name, TextColors.ENDC, self.inst_num, self.cls_num, self.dim, \
                        self.feat_path, TextColors.FATAL, self.normalize, TextColors.ENDC, self.dtype))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="example")
    parser.add_argument("--name", type=str, default='part1_test', help="image features")
    parser.add_argument("--prefix", type=str, default='./data', help="prefix of dataset")
    parser.add_argument("--dim", type=int, default=256, help="dimension of feature")
    parser.add_argument("--no_normalize", action='store_true', help="whether to normalize feature")
    args = parser.parse_args()

    ds = BasicDataset(name=args.name, prefix=args.prefix, dim=args.dim, normalize=not args.no_normalize)
    ds.info()
