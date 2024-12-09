import glob
import pandas as pd
import os

def process_csvs(input_dir, output_dir):
    dfs = []
    for file in glob.glob(os.path.join(input_dir, "part-*.csv")):
        df = pd.read_csv(file, header=None)
        df.columns = ['filename', 'word', 'count']
        dfs.append(df)
    
    result = pd.concat(dfs, ignore_index=True)
    
    os.makedirs(output_dir, exist_ok=True)

    totals = result.groupby('word')['count'].sum().reset_index().sort_values('count', ascending=False)
    totals.to_csv(f'{output_dir}/total_counts.csv', index=False)

    for filename in result['filename'].unique():
        file_df = result[result['filename'] == filename].sort_values('word')
        dest_file = output_dir + "/" + filename.split('/')[-1]
        file_df.to_csv(f'{dest_file}_counts.csv', index=False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input path")
    parser.add_argument("--output", required=True, help="Output path")
    args = parser.parse_args()

    process_csvs(args.input, args.output)
