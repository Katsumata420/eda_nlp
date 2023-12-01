# Easy data augmentation techniques for text classification
# Jason Wei and Kai Zou
import functools

from .eda import eda as eda_en
from .eda_japanese import eda_ja
from .tokenizer import get_tokenizer
from .synonym_extractor import get_synonym_extractor

#arguments to be parsed from command line
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str, help="input file of unaugmented data")
ap.add_argument("--output", required=False, type=str, help="output file of unaugmented data")
ap.add_argument("--num_aug", required=False, type=int, help="number of augmented sentences per original sentence")
ap.add_argument("--alpha_sr", required=False, type=float, help="percent of words in each sentence to be replaced by synonyms")
ap.add_argument("--alpha_ri", required=False, type=float, help="percent of words in each sentence to be inserted")
ap.add_argument("--alpha_rs", required=False, type=float, help="percent of words in each sentence to be swapped")
ap.add_argument("--alpha_rd", required=False, type=float, help="percent of words in each sentence to be deleted")
ap.add_argument("--add_original", required=False, type=bool, help="whether to add original sentence in augmented data", default=False)
# For Japanese
ap.add_argument("--lang", required=False, type=str, help="language", default="en", choices=["en", "ja"])
ap.add_argument("--tokenizer", required=False, type=str, help="tokenizer to use", default="sudachi")
ap.add_argument("--mecab-dict", required=False, type=str, help="mecab dictionary to use", default="ipadic")
ap.add_argument("--synonym_extractor", required=False, type=str, help="synonym extractor to use", default="sudachi")

args = ap.parse_args()

#the output file
output = None
if args.output:
    output = args.output
else:
    from os.path import dirname, basename, join
    output = join(dirname(args.input), 'eda_' + basename(args.input))

#number of augmented sentences to generate per original sentence
num_aug = 9 #default
if args.num_aug:
    num_aug = args.num_aug

#how much to replace each word by synonyms
alpha_sr = 0.1#default
if args.alpha_sr is not None:
    alpha_sr = args.alpha_sr

#how much to insert new words that are synonyms
alpha_ri = 0.1#default
if args.alpha_ri is not None:
    alpha_ri = args.alpha_ri

#how much to swap words
alpha_rs = 0.1#default
if args.alpha_rs is not None:
    alpha_rs = args.alpha_rs

#how much to delete words
alpha_rd = 0.1#default
if args.alpha_rd is not None:
    alpha_rd = args.alpha_rd

if alpha_sr == alpha_ri == alpha_rs == alpha_rd == 0:
     ap.error('At least one alpha should be greater than zero')

#generate more data with standard augmentation
def gen_eda(
    eda_func,
    train_orig,
    output_file,
    alpha_sr,
    alpha_ri,
    alpha_rs,
    alpha_rd,
    num_aug=9,
) -> None:

    writer = open(output_file, 'w')
    lines = open(train_orig, 'r').readlines()

    for i, line in enumerate(lines):
        parts = line[:-1].split('\t')
        label = parts[0]
        sentence = parts[1]
        aug_sentences = eda_func(sentence, alpha_sr=alpha_sr, alpha_ri=alpha_ri, alpha_rs=alpha_rs, p_rd=alpha_rd, num_aug=num_aug)
        for aug_sentence in aug_sentences:
            writer.write(label + "\t" + aug_sentence + '\n')

    writer.close()
    print("generated augmented sentences with eda for " + train_orig + " to " + output_file + " with num_aug=" + str(num_aug))

#main function
if __name__ == "__main__":

    if args.lang == "en":
        eda_func = eda_en
    elif args.lang == "ja":
        tokenizer = get_tokenizer(args.tokenizer, args.mecab_dict)
        extractor = get_synonym_extractor(args.synonym_extractor, tokenizer)
        eda_func = functools.partial(
            eda_ja,
            tokenizer=tokenizer,
            synonym_extractor=extractor,
        )
    else:
        raise ValueError("Invalid language.")
    #generate augmented sentences and output into a new file
    gen_eda(
        eda_func,
        args.input,
        output,
        alpha_sr=alpha_sr,
        alpha_ri=alpha_ri,
        alpha_rs=alpha_rs,
        alpha_rd=alpha_rd,
        num_aug=num_aug,
    )
