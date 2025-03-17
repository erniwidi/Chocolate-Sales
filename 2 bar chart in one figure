import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("/content/Chocolate Sales.csv")

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

# Amount and Boxes Shipped by Product
# Filter data for Q2 and Q1
Q2_data = df[df['Quarter'] == 'Q2']
Q1_data = df[df['Quarter'] == 'Q1']

# Group by Product, sum Boxes Shipped and Amount for Q2 and Q1
product_data_Q2 = Q2_data.groupby('Product')[['Boxes Shipped', 'Amount']].sum().reset_index()
product_data_Q1 = Q1_data.groupby('Product')[['Boxes Shipped', 'Amount']].sum().reset_index()

# Sort 
product_data_Q2 = product_data_Q2.sort_values(by='Boxes Shipped', ascending=False)

# Merge Q1 and Q2 data to calculate differences
product_data = pd.merge(product_data_Q2, product_data_Q1, on='Product', suffixes=('_Q2', '_Q1'))

# Calculate differences and percentage change from previous quarter (Q1)
product_data['Boxes Shipped Diff'] = product_data['Boxes Shipped_Q2'] - product_data['Boxes Shipped_Q1']
product_data['Amount Diff'] = product_data['Amount_Q2'] - product_data['Amount_Q1']
product_data['Boxes Shipped % Change'] = (product_data['Boxes Shipped Diff'] / product_data['Boxes Shipped_Q1']) * 100
product_data['Amount % Change'] = (product_data['Amount Diff'] / product_data['Amount_Q1']) * 100


# Create subplots with shared y-axis
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01,
                    column_widths=[0.3, 0.3], specs=[[{"secondary_y": True}, {"secondary_y": True}]])

# Boxes Shipped Bar Chart (Left)
fig.add_trace(go.Bar(
    y=product_data['Product'],
    x=product_data['Boxes Shipped_Q2'],
    orientation='h',
    name='Boxes Shipped',
    marker_color='blue'
), row=1, col=1, secondary_y=False)

# Amount Bar Chart (Right)
fig.add_trace(go.Bar(
    y=product_data['Product'],
    x=product_data['Amount_Q2'],
    orientation='h',
    name='Amount',
    marker_color='green'
), row=1, col=2, secondary_y=False)

# Add annotations for values and differences with color formatting
for i, row in product_data.iterrows():
    # Boxes Shipped Annotation
    fig.add_annotation(
        y=row['Product'],
        x=row['Boxes Shipped_Q2'],
        text=f"{row['Boxes Shipped_Q2']:,.0f} ({row['Boxes Shipped % Change']:+,.2f}%)",
        showarrow=False,
        xanchor='left',
        font=dict(color='red' if row['Boxes Shipped % Change'] < 0 else 'black'),  # Red for minus percentage
        row=1, col=1
    )

    # Amount Annotation
    fig.add_annotation(
        y=row['Product'],
        x=row['Amount_Q2'],
        text=f"{row['Amount_Q2']:,.0f} ({row['Amount % Change']:+,.2f}%)",
        showarrow=False,
        xanchor='left',
        font=dict(color='red' if row['Amount % Change'] < 0 else 'black'),  # Red for minus percentage
        row=1, col=2
    )
# Update layout
fig.update_layout(
    title='Product (Q2)',
    title_x=0.5,
    barmode='relative',
    xaxis=dict(title='Boxes Shipped', side='bottom'),
    xaxis2=dict(title='Amount', side='bottom'),
    yaxis=dict(autorange="reversed"),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='rgba(0,0,0,0)'
)
fig.update_yaxes(secondary_y=dict(showgrid=False, zeroline=False, showticklabels=False), row=1, col=3)  # Hide secondary y-axis grid and labels

fig.show()
