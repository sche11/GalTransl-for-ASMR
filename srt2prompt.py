# convert srt file to prompt file

import json, argparse
from datetime import timedelta
import pysrt

def merge_srt_files(input_files, output_file):
    merged_subs = pysrt.SubRipFile()

    for input_file in input_files:
        subs = pysrt.open(input_file)
        merged_subs.extend(subs)

    merged_subs.save(output_file, encoding='utf-8')

def make_prompt(input_file, output_file=None):
    # read srt file
    subs = pysrt.open(input_file)

    # parse srt file
    data = []
    for i in range(len(subs)):
        start = subs[i].start
        end = subs[i].end

        # time to seconds
        start = start.hours * 3600 + start.minutes * 60 + start.seconds + start.milliseconds / 1000

        end = end.hours * 3600 + end.minutes * 60 + end.seconds + end.milliseconds / 1000

        message = subs[i].text
        data.append({"start": start, "end": end, "message": message})

    if not output_file:
        return data

    # write prompt file
    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input_file", type=str, required=True)
    parser.add_argument("-o","--output_file", type=str, required=True)
    args = parser.parse_args()
    make_prompt(args.input_file, args.output_file)