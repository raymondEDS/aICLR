import argparse
import csv
import glob
import json

parser = argparse.ArgumentParser(description="")
parser.add_argument("-d", "--disapere_dir", default="", type=str, help="")
parser.add_argument("-l", "--label", default="", type=str, help="")
parser.add_argument("-r", "--rr", default="", type=str, help="")

def make_identifier(sentence_dict):
  return sentence_dict["review_id"] + "|||" + str(
      sentence_dict["sentence_index"])


def extract_review_examples(filename, label, rr):
  examples = []
  with open(filename, "r") as f:
    obj = json.load(f)
    for sentence in obj[rr]: #review_sentences, rebuttal_sentences
      examples.append((
          make_identifier(sentence),
          sentence["text"].replace("\t", " "),
          sentence[label],
      ))
  return examples


def main():
  args = parser.parse_args()
  assert args.label in "review_action fine_review_action aspect polarity rebuttal_stance rebuttal_action".split(
  )

  for subset in "train dev test".split():
    examples = []
    with open(f"../data/disapere_tsv/disapere_processed_{args.label}_{subset}.tsv", "w") as f:

      writer = csv.DictWriter(f,
                              fieldnames="identifier text label".split(),
                              delimiter="\t")
      writer.writeheader()

      for filename in glob.glob(
          f"{args.disapere_dir}/final_dataset/{subset}/*"):
        for identifier, text, label in extract_review_examples(
            filename, args.label, args.rr):
          writer.writerow({
              "identifier": identifier,
              "text": text,
              "label": label
          })


if __name__ == "__main__":
  main()