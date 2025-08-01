# Import Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import numpy as np

# Import Dataset
df = pd.read_csv("/content/Chocolate Sales.csv")
df

# Convert data type
df['Amount'] = df['Amount'].str.replace(',', '').str.replace('$', '').str.strip().astype(int)

# Convert to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
df['Month'] = df['Date'].dt.strftime('%b')

# Define the desired order of months
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']

# Convert 'Month' column to Categorical with specified order
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

# Create a dictionary to map months to quarters
month_to_quarter = {
    'Jan': 'Q1', 'Feb': 'Q1', 'Mar': 'Q1',
    'Apr': 'Q2', 'May': 'Q2', 'Jun': 'Q2',
    'Jul': 'Q3', 'Aug': 'Q3'
}
# Drop Q3
df = df[df['Month'] != 'Jul']
df = df[df['Month'] != 'Aug']

# Add a 'Quarter' column to the DataFrame
df['Quarter'] = df['Month'].map(month_to_quarter)
df

# Country vs Product (TOP 3)
# Filter data for Q2
Q2_data = df[df['Quarter'] == 'Q2']

# Group by Country and Product, sum Boxes Shipped and Amount
agg_data = Q2_data.groupby(['Country', 'Product'])[['Boxes Shipped', 'Amount']].sum().reset_index()

# Get top 3 products for each country based on Boxes Shipped
top3_products = agg_data.groupby('Country').apply(lambda x: x.nlargest(3, 'Boxes Shipped')).reset_index(drop=True)

# Create bubble chart with matplotlib
fig, ax = plt.subplots(figsize=(16, 8))  # Figure size

# Get unique product names
unique_products = top3_products['Product'].unique()

# Create a color map with a unique color for each product
color_map = {product: i for i, product in enumerate(unique_products)}

# Map product names to numerical values for color
top3_products['Product_Color'] = top3_products['Product'].map(color_map)


# Scatter plot for bubbles
scatter = ax.scatter(
    top3_products['Country'],
    top3_products['Product'],
    s=top3_products['Boxes Shipped'],  # Bubble size
    c=top3_products['Product_Color'],  # Bubble color
    cmap='viridis',  # Choose a colormap
    alpha=0.7  # Adjust transparency
)

# add annotation
for i, row in top3_products.iterrows():
    ax.annotate(
        row['Product'],
        xy=(row['Country'], row['Product']), # annotation loc
        xytext=(row['Country'], row['Product']), # annotation text
        ha='left',
        va='bottom',)

# Customize chart
ax.set_title("Top 3 Products Q2")

# Remove y-axis
ax.yaxis.set_visible(False) 

# Remove amount legend (colorbar)
cbar = fig.colorbar(scatter)
cbar.remove()

# Remove border
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)


plt.show()
