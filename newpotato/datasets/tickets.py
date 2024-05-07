import argparse
import csv
import logging

from newpotato.extractors.graph_extractor import GraphBasedExtractor


def _load_tickets(input_file):
    with open(input_file, newline="") as csvfile:
        lines = csvfile.readlines()
    reader = csv.reader(lines)
    for row in reader:
        (
            doc_id,
            category,
            summary,
            description,
            impact,
            status,
            solution,
            diagnosis,
            label,
            language,
        ) = row

        if language == "Language":
            continue
        elif language == "English":
            lang = "en"
        elif language == "German":
            lang = "de"
        else:
            raise ValueError(f"unrecognized language: {language}")

        yield doc_id, description, lang, label


def load_tickets(input_file, extractor, lang="en"):
    for doc_id, text, doc_lang, label in _load_tickets(input_file):
        if doc_lang != lang:
            continue

        for sen, graph in extractor.parse_text(text):
            yield sen, []


def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-i", "--input_file", default=None, type=str)
    parser.add_argument("-l", "--lang", default=None, type=str)
    return parser.parse_args()


def main():
    args = get_args()
    logging.basicConfig(
        format="%(asctime)s : %(module)s (%(lineno)s) - %(levelname)s - %(message)s",
        force=True,
    )
    logging.getLogger().setLevel(logging.INFO)
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    extractor = GraphBasedExtractor()
    
    for sen, _ in load_tickets(args.input_file, extractor, args.lang):
        print(sen)


if __name__ == "__main__":
    main()
