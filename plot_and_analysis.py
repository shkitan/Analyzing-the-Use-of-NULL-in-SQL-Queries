import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # or 'Agg' for a non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df_benchmark = pd.read_csv('benchmark_queries.csv')
df_queries_github_dataset = pd.read_csv('queries_github_dataset.csv')


plt.rcParams['font.size'] = 14

def plot_histogram_for_each_column(df, title, color):
    for i, column in enumerate(df.columns[1:], 1):  # Skip query_id
        plt.figure()
        sns.histplot(df[column], color=color)  # You can adjust the number of
        # bins
        # if title != "banchmark":
        #     plt.title(f'Histogram of {column}: {title} dataset - log scale')
        # else:
        #     plt.title(f'Histogram of {column}: {title} dataset')
        plt.xlabel('Complexity According to The Score System')
        plt.ylabel('Frequency')
        if title != "banchmark":
            plt.yscale('log')
            plt.savefig(f'Histogram_of_{column}_for_{title}_dataset_log.pdf',
                        dpi=300)
        else:
            plt.savefig(f'Histogram_of_{column}_for_{title}_dataset.pdf',
                        dpi=300)

        # plt.show()

def Plot_incidence_against_complexity(df, title):
    # Plot each incidence column against complexity
    df_grouped = df.groupby('complexity').mean().reset_index()
    columns = df.columns
    col_i = 2
    plt.figure(figsize=(10, 6))
    for col in df_grouped.columns[2:]:
        plt.plot(df_grouped['complexity'], df_grouped[col], label=col, marker='o')
        plt.xlabel('Complexity')
        plt.ylabel(f'Incident Count (Averaged) of {columns[col_i]}')
        col_i += 1
        plt.title(f'Average Incident Counts vs. Complexity for {title} '
                  f'dataset')
        plt.legend()
        plt.grid(True)
        plt.yscale('log')
        plt.xlim(0, 20)
        plt.show()


def display_summary_table_avg_min_max(df):
    summary_data = {}

    for column in df.columns[1:]:  # Skip query_id
        summary_data[column] = {
            'Mean': df[column].mean(),
            'Min': df[column].min(),
            'Max': df[column].max()
        }
    summary_df = pd.DataFrame(summary_data).T
    summary_df.index.name = 'Column'
    print(summary_df)

def display_summary_table_percentage(df):
    Percentage_val = df.apply(lambda column: ((column > 0).sum() /
                                           column.notna().sum()) * 100)
    print(Percentage_val)


plot_histogram_for_each_column(df_benchmark, "banchmark", 'blue')
plot_histogram_for_each_column(df_queries_github_dataset, "github queries",
                               'orange')
# display_summary_table(df_queries_github_dataset)
# display_summary_table(df_benchmark)
# Plot_incidence_against_complexity(df_queries_github_dataset, "github")

# display_summary_table_percentage(df_benchmark)
# display_summary_table_percentage(df_queries_github_dataset)