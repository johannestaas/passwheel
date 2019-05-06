import random


with open('/usr/share/dict/words') as f:
    WORDS = {
        x.strip().lower().replace("'s", '')
        for x in f
    }
    WORDS = sorted({
        x for x in WORDS
        if 3 < len(x) < 12
    })


def get_word():
    return random.choice(WORDS)


def gen_password(num_words, num_digits):
    s = ''
    words = [get_word() for i in range(num_words)]
    digits_fmt = '{{:0{}}}'.format(num_digits)
    digits = digits_fmt.format(random.randint(0, 10**num_digits - 1))
    i = random.randint(0, num_words - 1)
    words[i] = words[i].upper()
    return ''.join(words + [digits])
