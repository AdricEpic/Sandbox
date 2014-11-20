from PIL import Image, ImageFile, ImageStat
import operator

src_img = Image.open("servoskull.jpg")
assert (isinstance(src_img, ImageFile.ImageFile))

src_height, src_width = src_img.size

dest_width = 80
dest_char_ratio = .45
block_width = int(src_width / dest_width)
block_height = int(src_height / (dest_width * dest_char_ratio))

# Calculate character dimensions of final image
blocks_wide = int(src_width / block_width)
blocks_high = int(src_height / block_height)


def brightness(im):
    im = im.convert('L')
    stat = ImageStat.Stat(im)
    return stat.rms[0]


scale = " .:-=+*#%@"

charmap = {
    ((0, 0, 0),) * 3: " ",

    # 1 pxl
    ((0, 0, 0),
     (0, 0, 0),
     (0, 1, 0)): ".",

    # 2 pxl
    ((0, 1, 0),
     (0, 0, 0),
     (0, 1, 0)): ":",

    # 3 pxl
    ((0, 1, 0),) * 3: "|",

    ((0, 0, 1),
     (0, 1, 0),
     (1, 0, 0)): "/",

    ((1, 0, 0),
     (0, 1, 0),
     (0, 0, 1)): "\\",

    ((0, 1, 0),
     (1, 0, 1),
     (0, 0, 0)): "^",

    ((0, 0, 0),
     (1, 0, 1),
     (0, 1, 0)): "v",

    ((0, 0, 0),
     (0, 0, 0),
     (1, 1, 1)): "_",

    ((0, 0, 0),
     (1, 1, 0),
     (1, 0, 0)): "r",

    # 4 pxl
    ((1, 0, 0),
     (0, 1, 1),
     (1, 0, 0)): ">",

    ((0, 0, 1),
     (1, 1, 0),
     (0, 0, 1)): "<",

    ((1, 0, 1),
     (0, 1, 0),
     (0, 1, 0)): "Y",

    # 5 pxl
    ((1, 1, 1),
     (0, 1, 0),
     (0, 1, 0)): "T",

    ((1, 0, 1),
     (0, 1, 0),
     (1, 0, 1)): "X",

    ((0, 1, 0),
     (1, 1, 1),
     (0, 1, 0)): "+",

    ((0, 1, 0),
     (0, 1, 1),
     (0, 1, 1)): "t",

    ((1, 1, 0),
     (1, 0, 0),
     (1, 1, 0)): "[",

    ((0, 1, 1),
     (0, 0, 1),
     (0, 1, 1)): "[",

    ((1, 0, 0),
     (1, 1, 0),
     (1, 1, 0)): "b",

    ((0, 0, 1),
     (0, 1, 1),
     (0, 1, 1)): "d",

    ((1, 1, 0),
     (0, 1, 0),
     (1, 1, 0)): "J",

    ((1, 1, 1),
     (0, 1, 0),
     (0, 1, 0)): "u",

    # 6 pxl
    ((1, 0, 1),
     (1, 1, 0),
     (1, 0, 1)): "K",

    ((1, 1, 1),
     (0, 0, 0),
     (1, 1, 1)): "=",

    ((0, 0, 0),
     (1, 1, 1),
     (1, 1, 1)): "a",

    # 7 pxl
    ((1, 0, 1),
     (1, 0, 1),
     (1, 1, 1)): "U",

    ((1, 0, 1),
     (1, 1, 1),
     (1, 0, 1)): "H",

    ((1, 1, 1),
     (0, 1, 0),
     (1, 1, 1)): "I",

    ((1, 1, 1),
     (1, 1, 1),
     (1, 0, 0)): "P",

    # 8 pxl
    ((1, 1, 1),
     (1, 0, 1),
     (1, 1, 1)): "O",

    # 9 pxl
    ((1, 1, 1),) * 3: "@",
}


def equalize(im):
    im = im.convert("L")
    hstgrm = im.histogram()
    lut = []
    for b in range(0, len(hstgrm), 256):
        # step size
        step = reduce(operator.add, hstgrm[b:b+256]) / 255
        # create equalization lookup table
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + hstgrm[i+b]
    # map image through lookup table
    return im.point(lut)


def chunk_grid(im_chunk, threshold):
    # chunk = equalize(chunk)
    chunk_w, chunk_h = im_chunk.size
    sub_cnt_w = 3
    sub_cnt_h = 3
    sub_w = chunk_w / sub_cnt_w
    sub_h = chunk_h / sub_cnt_h
    array = []
    for ht in range(sub_cnt_h):
        chnk_row = []
        for wd in range(sub_cnt_w):
            chnk_bbox = ((sub_w * wd), (sub_h * ht),
                         sub_w * wd + sub_w, sub_h * ht + sub_h)
            sub_chunk = im_chunk.crop(chnk_bbox)
            bin_bright = 1 if (brightness(sub_chunk) / 255) > threshold else 0
            chnk_row.append(bin_bright)
        array.append(chnk_row)
    return tuple([tuple(chnk_row) for chnk_row in array])


img = []
for h in range(blocks_high):
    row = ""
    for w in range(blocks_wide):
        bbox = ((block_width * w), (block_height * h),
                block_width * w + block_width, block_height * h + block_height)
        chunk = src_img.crop(bbox)
        norm_bright = brightness(chunk) / 255  # normalize brightness value
        # FixMe - chunk_grid too noisy, esp for chunks w/ little overall contrast change
        # try:
        #     bright_char = charmap[chunk_grid(chunk, norm_bright)]
        #     print "found in charmap!"
        # except KeyError:
        bright_char = scale[int(norm_bright * len(scale))]  # Get value from scale
        row += bright_char
    img.append(row)  # print row
for row in img:
    print row