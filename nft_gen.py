import os
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageChops 
import time
import random
SIZE = 2000
WIDTH_PER_LETTER = 46

def getFileNamesInDirectory(dirName):
    path = 'images/' + dirName
    files = os.listdir(path)
    return files

backdrops = getFileNamesInDirectory("backdrop")
individuals = getFileNamesInDirectory("individual")
verticalLines = getFileNamesInDirectory("verticalLines")

def addIndividual(im1, im2):
    dst = Image.new('RGBA', (im1.width, im1.height))
    dst.paste(im1, (0,0))
    dst.paste(im2, (840, 1510), im2)
    dst = Image.blend(im1, dst, 0.4)
    
    return dst

def addVerticalLines(im1, im2, mask=None):
    dst = Image.new('RGBA', (im1.width, im1.height))
    dst.paste(im1, (0, 0))
    im2 = im2.resize((SIZE, SIZE))
    dst.paste(im2, (0, 0), im2)
    return dst

def addText(im1, color, text, left, long, parallel, xor_f = False):
    # result w, h
    width = len(text) * WIDTH_PER_LETTER
    gap = width
    height = SIZE if long else 650

    # get text size
    font = ImageFont.truetype("Retro Gaming.ttf", 400)
    w, h = font.getsize(text)
    rh = int(h * 0.73)

    # text -> image
    num_image = Image.new("RGBA", (w, rh), color=None)
    draw = ImageDraw.Draw(num_image)
    draw.text((0, rh-h), text=text, fill=color, font=font)
    num_image = num_image.resize((width, height))

	# past 1
    num_image1 = Image.new('RGBA', (SIZE, SIZE))
    if not parallel:
        num_image1.paste(num_image, (int(SIZE/2) - int(width/2), int(SIZE/2)- int(height/2)))
    else:
        num_image1.paste(num_image, (int(SIZE/2) - width - int(gap/2), int(SIZE/2)- int(height/2)))
        num_image1.paste(num_image, (int(SIZE/2) + int(gap/2), int(SIZE/2)- int(height/2)))

    # rotate
    rotate = 45 if left else -45
    num_image1 = num_image1.rotate(rotate)

    # paste 2
    if xor_f:
        im3 = ImageChops.logical_xor(im1.convert("1"), num_image1.convert("1"))
        return im3
    else:
        im1.paste(num_image1, (0, 0), num_image1)
        return im1

def get_color(white = True):
    return (255,255,255) if white else (0,0,0)

def generateParcel1(individual, digits, numbers, white=True):
    individual_img = Image.open('images/individual/' + individual).convert("RGBA")
    if white:
        background_img = Image.open("images/backdrop/white.png").convert("RGBA")
        verticalLine_img = Image.open('images/verticalLines/black.png').convert("RGBA")
    else:
        background_img = Image.open("images/backdrop/black.png").convert("RGBA")
        verticalLine_img = Image.open('images/verticalLines/white.png').convert("RGBA")
    if numbers == 1:
        text_right = text_left = random_number(digits, digits)
    else:
        text_left = random_number(digits, digits)
        text_right = random_number(digits, digits)

    ret = addIndividual(background_img, individual_img)
    ret = addVerticalLines(ret, verticalLine_img)
    ret = addText(ret, get_color(not white), text_left,left= True, long = True, parallel = False)
    ret = addText(ret, get_color(not white), text_right,left= False, long = True, parallel = False)

    return ret

def generateParcel2(individual, digits, numbers, white=True, left=True):
    individual_img = Image.open('images/individual/' + individual).convert("RGBA")
    if white:
        background_img = Image.open("images/backdrop/white.png").convert("RGBA")
        verticalLine_img = Image.open('images/verticalLines/black.png').convert("RGBA")
    else: # black
        background_img = Image.open("images/backdrop/black.png").convert("RGBA")
        verticalLine_img = Image.open('images/verticalLines/white.png').convert("RGBA")

    if numbers == 1:
        text_right = text_left = random_number(digits, digits)
    else:
        text_left = random_number(digits, digits)
        text_right = random_number(digits, digits)

    ret = addIndividual(background_img, individual_img)
    ret = addVerticalLines(ret, verticalLine_img)
    ret = addText(ret, get_color(not white), text_left,left= left, long = True, parallel = False)
    ret = addText(ret, get_color(not white), text_right,left= not left, long = False, parallel = False)

    horizontal_image = "horizontallines_" + ("right_" if left else "left_") + ("white" if white else "black") + ".png"
    horizontal_image = Image.open('images/horizontal/' + horizontal_image).convert("RGBA")
    
    opacity = 0.75 if white else 0.3
    orig = ret.copy()
    ret.paste(horizontal_image, (625, 625), horizontal_image)
    ret = Image.blend(orig, ret, opacity)

    return ret

def generateParcel3( digits, numbers, white=True ):
    if white:
        background_img = Image.open("images/backdrop/white.png").convert("RGBA")
        verticalLine_img = Image.open('images/verticalLines/black.png').convert("RGBA")
    else:
        background_img = Image.open("images/backdrop/black.png").convert("RGBA")
        verticalLine_img = Image.open('images/verticalLines/white.png').convert("RGBA")

    if numbers == 1:
        text_left_p = text_right_p = text_right = text_left = random_number(digits, digits)
    elif numbers == 2:
        text_left = text_right = random_number(digits, digits)
        text_left_p = text_right_p = random_number(digits, digits)
    elif numbers == 3:
        text_right = random_number(digits, digits)
        text_left = random_number(digits, digits)
        text_left_p = text_right_p = random_number(digits, digits)
    else: # 4
        text_right = random_number(digits, digits)
        text_left = random_number(digits, digits)
        text_left_p = random_number(digits, digits)
        text_right_p = random_number(digits, digits)

    ret = addVerticalLines(background_img, verticalLine_img)
    ret = addText(ret, get_color(white), text_left_p,left= True, long = True, parallel = True)
    ret = addText(ret, get_color(not white), text_right_p,left= False, long = True, parallel = True)

    
    ret = addText(ret, get_color(not white), text_left,left= True, long = True, parallel = False)
    ret = addText(ret, get_color(white), text_right,left= False, long = True, parallel = False)

    return ret

def generateParcel4( individual, digits, numbers, white=True):
    verticalLine_img = Image.open('images/diagonallines_black.png').convert("RGBA")
    verticalLine_mask = Image.open('images/diagonallines_mask.png').convert("L")
    background_img = Image.open("images/backdrop/white.png").convert("RGBA")

    if white:
        backright_img = Image.open('images/back/backright_white.png').convert("RGBA")
        backleft_img = Image.open('images/back/backleft_white.png').convert("RGBA")
    else:
        backright_img = Image.open('images/back/backright_black.png').convert("RGBA")
        backleft_img = Image.open('images/back/backleft_black.png').convert("RGBA")

    verticalLine_mask = verticalLine_mask.resize(backright_img.size)

    individual_img = Image.open('images/individual/' + individual).convert("RGBA")
    
    if numbers == 1:
        text_right = text_left = random_number(digits, digits)
    else:
        text_left = random_number(digits, digits)
        text_right = random_number(digits, digits)
    
    ret = addIndividual(background_img, individual_img)
    ret = addVerticalLines(ret, verticalLine_img)

    ret = addVerticalLines(ret, backright_img)
    ret = addVerticalLines(ret, backleft_img)

    ret = addText(ret, get_color(not white), text_left,left= True, long = True, parallel = False)
    ret = addText(ret, get_color(not white), text_right,left= False, long = True, parallel = False)

    return ret

def random_number(bottom=6, top=12):
    length = random.randint(bottom,top)
    ret = []
    digits = "0123456789"
    for i in range(length):
        index = random.randint(0,9)
        ret.append(digits[index])
    return "".join(ret)

# generate rate arrary from rates 
def generate_rates(rate, total):
    res = 0
    ret = [0]
    rate_sum = 0
    #calc rate sum
    for r in rate:
        rate_sum += r
    #calc rates
    for r in rate:
        res += int(r/rate_sum * total)
        ret.append(res)
    ret[-1] = total # fill gap
    return ret

def find_in_rates(index, rates):
    for i in range(len(rates) - 1):
        if rates[i] <= index and index < rates[i+1]:
            return i

def get_random_individual(white=True):
    color = "white" if white else "black"
    while True:
        index = random.randint(0, len(individuals)-1 )
        if color in individuals[index]:
            return individuals[index]
            
def main():
    random.seed(time.time())
    index = 0

    N = 40
    P = []

    p1_count = int(N * 0.32)
    p2_count = int(N * 0.32)
    p3_count = int(N * 0.32)
    p4_count = int(N - p1_count - p2_count - p3_count)

    # parcel 1
    black = int(p1_count * 8.8 / 32.0)
    white = p1_count - black
    
    rate = [0.96, 1.60, 3.20, 9.60, 12.80, 3.20, 0.64]# 6-12 rate
    digits = generate_rates(rate, p1_count)

    one_number = int(p1_count*22.4/32.0)
    for i in range(p1_count):
        item = dict()
        item["parcel"] = 1
        item["white"] = True if i<black else False
        item["numbers"] = 1 if i<one_number else 2
        item["digits"] = 6 + find_in_rates(i, digits)
        P.append(item)
    
    # parcel 2
    rate = [0.96, 1.60, 3.20, 9.60, 12.80, 3.20, 0.64]# 6-12 rate
    digits = generate_rates(rate, p2_count)
    one_number = int(p2_count*22.4/32.0)

    for i in range(p2_count):
        item = dict()
        item["parcel"] = 2
        item["white"] = True if i<black else False
        item["numbers"] = 1 if i<one_number else 2
        #calc digits
        item["digits"] = 6 + find_in_rates(i, digits)
        P.append(item)

    # parcel 3
    rate = [19.2, 6.4, 4.8, 3.2]
    numbers = generate_rates(rate, p3_count)
    digits =generate_rates(rate, p3_count)
    for i in range(p3_count):
        item = dict()
        item["parcel"] = 3
        item["white"] = True if i<black else False
        item["numbers"] = 1 + find_in_rates(i, numbers)
        item["digits"] = 6 + find_in_rates(i, digits)
        P.append(item)
    # parcel 4
    rate = [2.80, 1.2]
    numbers = generate_rates(rate,p4_count)
    rate = [0.96, 1.60, 3.20, 9.60, 12.80, 3.20, 0.64]# 6-12 rate
    digits = generate_rates(rate,p4_count)

    for i in range(p4_count):
        item = dict()
        item["parcel"] = 4
        item["white"] = bool(i%2)
        item["numbers"] = 1 + find_in_rates(i, numbers)
        item["digits"] = 1 + find_in_rates(i, digits)
        P.append(item)

    # genrate all
    index = 0
    for p in P: # iterate parcels
        white = p["white"]
        individual = get_random_individual(white)
        numbers = p["numbers"]
        digits = p["digits"]
        color = "white" if white else "black"
        parcel = p["parcel"]
        if parcel != 4:
            continue
        if p["parcel"] == 1: #parcel 1
            result = generateParcel1(individual, digits, numbers, white=white)
        elif p["parcel"] == 2: #parcel 2
            result = generateParcel2(individual, digits, numbers, white=white, left=False)
        elif p["parcel"] == 3: #parcel 3
            result = generateParcel3( digits, numbers,white= white)
        else: # 4
            result = generateParcel4(individual, digits, numbers, bool(index%2))
        result.save("output/" + str(index) + ".png", "PNG")
        # increase index
        print("Generated {}th item [parcel: {}, color: {}, numbers={}, digits={}] ".format( index, p["parcel"], color, numbers, digits ) )
        index += 1
    
if __name__ == '__main__':
    main()
