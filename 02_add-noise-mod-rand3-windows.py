#!/usr/bin/env python
# This file copies from kaldi/thchs30/s5/utils and modified by me.

from __future__ import print_function
import optparse
import random
import re
import logging
import wave
import math
import struct
import sys
import os
import importlib

try:
    import pyximport
    pyximport.install()
    from util import *
except:
    print(
        "Cython possibly not installed, using standard python code. The process might be slow",
        file=sys.stderr)

    def energy(mat):
        return float(sum([x * x for x in mat])) / len(mat)

    def mix(mat, noise, pos, scale):
        ret = []
        l = len(noise)
        for i in range(len(mat)):
            x = mat[i]
            d = int(x + scale * noise[pos])
            #if d > 32767 or d < -32768:
            #    logging.debug('overflow occurred!')
            d = max(min(d, 32767), -32768)
            ret.append(d)
            pos += 1
            if pos == l:
                pos = 0
        return (pos, ret)


def findNoisename(noisename, noiseArray=[]):
    for index in range(len(noiseArray)):
        if (noisename == noiseArray[index]):
            return index
    return -1


def wave_mat(wav_filename):
    f = wave.open(wav_filename, 'r')
    n = f.getnframes()
    ret = f.readframes(n)
    f.close()
    return list(struct.unpack('%dh' % n, ret))


def num_samples(mat):
    return len(mat)


def scp(scp_filename):
    with open(scp_filename, encoding="utf-8") as f:
        for l in f:
            # print(l.strip().split())
            yield tuple(l.strip().split())


def wave_header(sample_array, sample_rate):
    byte_count = (len(sample_array)) * 2  # short
    # write the header
    hdr = struct.pack(
        '<ccccIccccccccIHHIIHH',
        b'R',
        b'I',
        b'F',
        b'F',
        byte_count + 0x2c - 8,  # header size
        b'W',
        b'A',
        b'V',
        b'E',
        b'f',
        b'm',
        b't',
        b' ',
        0x10,  # size of 'fmt ' header
        1,  # format 1
        1,  # channels
        sample_rate,  # samples / second
        sample_rate * 2,  # bytes / second
        2,  # block alignment
        16)  # bits / sample
    hdr += struct.pack('<ccccI', b'd', b'a', b't', b'a', byte_count)
    return hdr


def output(tag, mat):
    sys.stdout.write(tag + ' ')
    sys.stdout.write(wave_header(mat, 16000))
    sys.stdout.write(struct.pack('%dh' % len(mat), *mat))


def output_wave_test_file(dir, tag, type, mat):
    type = str(type).zfill(
        2)  # here type marking the length of type 1-9 is 1, 10-99 is 2, so on
    with open('%s/%s_%s.wav' % (dir, tag, type), 'w') as f:
        f.write(wave_header(mat, 16000))
        f.write(struct.pack('%dh' % len(mat), *mat))


def output_wave_file(dir, tag, mat):
    savepath = dir
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    with open('%s/%s' % (savepath, tag), 'wb') as f:
        f.write(wave_header(mat, 16000))
        f.write(struct.pack('%dh' % len(mat), *mat))


def main():
    parser = optparse.OptionParser()
    parser.add_option('--noise-level-low', default=-10, type=float, help='')
    parser.add_option('--noise-level-high', default=15, type=float, help='')
    parser.add_option('--noise-src', default="noise.scp", type=str, help='')
    parser.add_option('--seed', default=32, type=int, help='')
    parser.add_option('--sigma0', default=0, type=float, help='')
    parser.add_option('--wav-src', default="wav.scp", type=str, help='')
    parser.add_option('--verbose', default=0, type=int, help='')
    parser.add_option('--wavdir', default=r"output", type=str, help='')
    (args, dummy) = parser.parse_args()
    random.seed(args.seed)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    global noises
    noise_energies = []
    noises = []

    # Making noise type label matrix
    noise_count = len(open(
        args.noise_src, encoding="utf-8").readlines())  # Count of noise types

    noiseName = []
    for tag, wav in scp(args.noise_src):
        noiseName.append(tag)
        logging.debug('noise wav: %s', wav)
        mat = wave_mat(wav)
        e = energy(mat)
        # print(e, tag)
        logging.debug('noise energy: %f', e)
        noise_energies.append(e)
        noises.append((0, mat))

    wavType = os.path.basename(args.wav_src).split(".")[0]
    src_count = len(open(args.wav_src).readlines())  # Count of wav files
    doneCount = 0
    if ("test" != wavType):  # for situation train.scp and dev.scp
        for tag, wav in scp(args.wav_src):
            #print(tag)
            #print(wav) #####
            logging.debug('wav: %s', wav)
            noise_level = random.uniform(args.noise_level_low,
                                         args.noise_level_high)
            noise_level = random.gauss(noise_level, args.sigma0)
            logging.debug('noise level: %f', noise_level)
            mat = wave_mat(wav)
            signal = energy(mat)
            logging.debug('signal energy: %f', signal)
            noise = signal / (10**(noise_level / 10.))
            #print(noise) ##############
            logging.debug('noise energy: %f', noise)
            type = random.randint(
                0, noise_count -
                1)  # generatae a random type from the input noise types
            logging.debug('selected type: %d', type)
            __, fname = os.path.split(wav)
            p, n = noises[type]
            #print(p)
            if p + len(mat) > len(n):
                noise_energies[type] = energy(n[p::] + n[0:len(n) - p:])
            else:
                noise_energies[type] = energy(n[p:p + len(mat):])
            #print(noise_energies[type]) ########
            while (noise_energies[type] == 0.0):
                type = random.randint(0, noise_count - 1)
                p, n = noises[type]
                if p + len(mat) > len(n):
                    noise_energies[type] = energy(n[p::] + n[0:len(n) - p:])
                else:
                    noise_energies[type] = energy(n[p:p + len(mat):])
                print("!!!!!!!!!!!!!!!")

            scale = math.sqrt(noise / noise_energies[type])
            #print("sclae=",scale) ###########
            logging.debug('noise scale: %f', scale)
            pos, result = mix(mat, n, p, scale)
            noises[type] = (pos, n)
            if args.wavdir != 'NULL':
                savepath = os.path.join(os.getcwd(), args.wavdir)
                output_wave_file(savepath, fname, result)
                doneCount += 1
                print("%d/%d\t%d" % (doneCount, src_count, type))
            else:
                output(tag, result)
    else:  # when processing test.scp
        src_count *= noise_count
        for tag, wav in scp(args.wav_src):
            logging.debug('wav: %s', wav)
            noise_level = random.uniform(args.noise_level_low,
                                         args.noise_level_high)
            noise_level = random.gauss(noise_level, args.sigma0)
            logging.debug('noise level: %f', noise_level)
            mat = wave_mat(wav)
            signal = energy(mat)
            logging.debug('signal energy: %f', signal)
            noise = signal / (10**(noise_level / 10.))
            logging.debug('noise energy: %f', noise)

            for type in range(0, noise_count):
                type = random.randint(
                    0, noise_count -
                    1)  # generatae a random type from the input noise types
                logging.debug('selected type: %d', type)
                p, n = noises[type]
                if p + len(mat) > len(n):
                    noise_energies[type] = energy(n[p::] + n[0:len(n) - p:])
                else:
                    noise_energies[type] = energy(n[p:p + len(mat):])
                scale = math.sqrt(noise / noise_energies[type])
                logging.debug('noise scale: %f', scale)
                pos, result = mix(mat, n, p, scale)
                noises[type] = (pos, n)
                if args.wavdir != 'NULL':
                    output_wave_test_file(args.wavdir, tag, type, result)
                    doneCount += 1
                    print("%d/%d" % (doneCount, src_count))
                else:
                    output(tag, result)


if __name__ == '__main__':
    main()
