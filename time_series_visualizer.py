import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(
    'fcc-forum-pageviews.csv',
    parse_dates=True,
    index_col=0,
)

# Clean data
df = df[df['value'] < df['value'].quantile(.974)]
df = df[df['value'] > df['value'].quantile(.025)]
df = df.fillna(method='ffill')
df = df.dropna()

def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(18, 6))
    x = df.index
    y = df['value']

    plt.plot(x, y)
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df

    df_bar['month'] = df_bar.index.month
    df_bar['year'] = df_bar.index.year
    
    # Group by Year and Month, calculate the average page views
    df_grouped = df.groupby(['year', 'month'])['value'].mean().unstack()
    

    # Draw bar plot
    fig, axes = plt.subplots(figsize=(14, 8))
    df_grouped.plot(kind='bar', ax=axes)

    axes.set_xlabel('Years')
    axes.set_ylabel('Average Page Views')

    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
    axes.legend(month_names, title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]


    # Draw box plots (using Seaborn)
    fig = plt.figure(figsize=(20, 8))
    plt.subplot(1, 2, 1)
    sns.boxplot(x='year', y='value', data=df_box)
    plt.title('Year-wise Box Plot (Trend)')
    plt.xlabel('Year')
    plt.ylabel('Page Views')

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.subplot(1, 2, 2)
    sns.boxplot(x='month', y='value', data=df_box, order=month_names)
    plt.title('Month-wise Box Plot (Seasonality)')
    plt.xlabel('Month')
    plt.ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig