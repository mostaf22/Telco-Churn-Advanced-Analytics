#!/usr/bin/env python
# coding: utf-8

# # Customer retention matrix and the financial impact on telecommunications companies

# In[73]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[61]:


file_name = 'Telco_customer_churn.xlsx'


# In[62]:


df = pd.read_excel(file_name)


# In[ ]:


df


# # Data Overview

# In[ ]:


print("--- First 5 Rows ---")
print(df.head())


# In[ ]:


print("\n--- Data Info ---")
print(df.info())


# In[ ]:


print("\n--- Summary Statistics ---")
print(df.describe())


# # Data Cleaning

# In[ ]:


df.columns = df.columns.str.strip()
df


# In[ ]:


df['Total Charges'] = pd.to_numeric(df['Total Charges'], errors='coerce')
df


# In[ ]:


df['Total Charges'] = df['Total Charges'].fillna(0)


# In[ ]:


df


# In[ ]:


df.drop_duplicates(inplace=True)
df


# In[ ]:


df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df


# In[91]:


print("\n✅ Cleaning Done! No duplicates, No missing numeric values.")


# # Visual Show

# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation between Numeric Features')
plt.show()


# In[ ]:


df[['Tenure Months', 'Monthly Charges']].hist(bins=30, figsize=(12, 5), color='skyblue', edgecolor='black')
plt.suptitle('Distribution of Key Numerical Features')
plt.show()


# In[ ]:


plt.figure(figsize=(6, 4))
sns.countplot(x='Churn Label', data=df, palette='magma')
plt.title('Count of Churn vs Non-Churn Customers')
plt.show()


# # TELCO CUSTOMER RETENTION & FINANCIAL IMPACT MATRIX

# In[ ]:


title = "TELCO CUSTOMER RETENTION & FINANCIAL IMPACT MATRIX"
subtitle = "Strategic Data Analysis - 2026 Q2 Report"
border = "=" * 60

print(f"\n{border}")
print(f"{title:^60}")
print(f"{subtitle:^60}")
print(f"{border}\n")


# # Overall Churn Rate

# In[63]:


# --- HEADER ---
title = "TELCO CUSTOMER RETENTION & FINANCIAL IMPACT MATRIX"
border = "=" * 60

# --- 1. Overall Churn Rate ---
churn_rate = (df['Churn Label'].value_counts(normalize=True)['Yes']) * 100

# --- 2. Total Customers ---
total_customers = df['CustomerID'].nunique()

# --- 3. Average Tenure Months ---
avg_tenure = df['Tenure Months'].mean()

# --- 4. Lost Revenue (Monthly) ---
lost_revenue = df[df['Churn Label'] == 'Yes']['Monthly Charges'].sum()

# --- 5. Monthly ARPU ---
arpu = df['Monthly Charges'].mean()

# --- 6. High-Value Churners ---
high_value_churn = df[(df['Churn Label'] == 'Yes') & (df['Monthly Charges'] > arpu)].shape[0]

# --- 7. Estimated CLV ---
avg_clv = (df['Monthly Charges'] * df['Tenure Months']).mean()



# In[64]:


print(f"\n{border}\n{title:^60}\n{border}\n")
# --- PRINTING THE MATRIX ---
print(f"1. Overall Churn Rate        : {churn_rate:.2f}%")
print(f"2. Total Customer Base      : {total_customers:,} Subscribers")
print(f"3. Average Loyalty Lifespan : {avg_tenure:.1f} Months")
print(f"4. Monthly Revenue Leakage  : ${lost_revenue:,.2f}")
print(f"5. Monthly ARPU             : ${arpu:.2f}")
print(f"6. VIP Attrition Alert      : {high_value_churn} High-Value Customers")
print(f"7. Future Value Projection  : ${avg_clv:,.2f} (Avg. CLV)")
print(f"\n{border}")


# In[71]:


import plotly.io as pio
pio.renderers.default = 'jupyterlab'
pio.renderers.default = 'notebook'


# # Overall Churn Rate

# In[74]:


churn_counts = df['Churn Label'].value_counts()
labels = churn_counts.index # Stay vs Churn
values = churn_counts.values

fig = go.Figure(data=[go.Pie(
    labels=labels, 
    values=values, 
    hole=.5,
    marker=dict(colors=['#1E3A8A', '#EF4444']), # أزرق للـ No وأحمر للـ Yes
    textinfo='percent+label'
)])

fig.update_layout(
    title_text="<b>The Grand Summary (Churn Rate & Counts)</b>",
    annotations=[dict(text='CHURN', x=0.5, y=0.5, font_size=20, showarrow=False)],
    showlegend=True
)

fig.show()


#  # "Money" (ARPU & Lost Revenue)

# In[79]:


money_analysis = df.groupby('Churn Label')['Monthly Charges'].mean().reset_index()

fig = go.Figure()

fig.add_trace(go.Bar(
    x=money_analysis['Churn Label'], 
    y=money_analysis['Monthly Charges'],
    text=money_analysis['Monthly Charges'].round(2),
    textposition='auto',
    marker_color=['#1E3A8A', '#EF4444'], 
    name='Avg Monthly Charges'
))

fig.update_layout(
    title_text="<b>Money (ARPU & Lost Revenue Analysis)</b>",
    xaxis_title="Customer Status (Churn vs Stay)",
    yaxis_title="Average Monthly Bill ($)",
    template='plotly_white',
    height=500
)

fig.show()


# # Percentage of long-term contract customers (CLT - Customer Loyalty Tracking)

# In[77]:


contract_churn = pd.crosstab(df['Contract'], df['Churn Label'], normalize='index') * 100
contract_churn = contract_churn.reset_index()

fig = go.Figure()

fig.add_trace(go.Bar(
    name='Stay (Loyal)',
    x=contract_churn['Contract'],
    y=contract_churn['No'],
    marker_color='#1E3A8A',
    text=contract_churn['No'].round(1).astype(str) + '%',
    textposition='inside'
))

fig.add_trace(go.Bar(
    name='Churn (Lost)',
    x=contract_churn['Contract'],
    y=contract_churn['Yes'],
    marker_color='#EF4444',
    text=contract_churn['Yes'].round(1).astype(str) + '%',
    textposition='inside'
))

fig.update_layout(
    title_text="<b>CLT: Loyalty Tracking by Contract Duration (%)</b>",
    barmode='stack',
    xaxis_title="Contract Type",
    yaxis_title="Percentage of Customers (%)",
    legend_title="Status",
    template='plotly_white'
)

fig.show()


# # Average Tenure

# In[81]:


fig = px.histogram(df, x='Tenure Months', 
                   color='Churn Label',
                   marginal='box', # بيضيف Box Plot فوق عشان نشوف الـ Outliers والـ Median
                   title='<b>Customer Tenure Distribution & Loyalty Trends</b>',
                   color_discrete_map={'Yes': '#EF4444', 'No': '#1E3A8A'},
                   nbins=30)

avg_tenure_val = df['Tenure Months'].mean()
fig.add_vline(x=avg_tenure_val, line_dash="dash", line_color="green", 
              annotation_text=f"Average: {avg_tenure_val:.1f} Months")

fig.update_layout(
    xaxis_title="Months with Company",
    yaxis_title="Number of Customers",
    template='plotly_white',
    barmode='overlay'
)

fig.show()


# The U-Shape: In telecom companies, you'll often find a surge in customers around month 1 (people trying out and then quitting) and another surge around month 70 (long-standing, loyal customers). The area in the middle is where we focus.
# 
# The Box Plot (at the top): The line in the middle of the box shows you the median. If the median for customers who quit (Yes) is very low (for example, 5 months), then we have a problem with the service's "first impression."
# 
# The Gap Between Colors: The more red (Yes) there is in the first few months, the more it means the company is spending a lot of money on advertising that attracts "flash" customers who don't last long enough to cover their costs.

# # "Loyalty and Time" (Average Tenure)

# In[83]:


tenure_analysis = df.groupby(['Contract', 'Churn Label'])['Tenure Months'].mean().reset_index()

fig = go.Figure()

fig.add_trace(go.Bar(
    x=tenure_analysis[tenure_analysis['Churn Label'] == 'No']['Contract'],
    y=tenure_analysis[tenure_analysis['Churn Label'] == 'No']['Tenure Months'],
    name='Still with us (Loyal)',
    marker_color='#1E3A8A', 
    text=tenure_analysis[tenure_analysis['Churn Label'] == 'No']['Tenure Months'].round(1),
    textposition='auto'
))

fig.add_trace(go.Bar(
    x=tenure_analysis[tenure_analysis['Churn Label'] == 'Yes']['Contract'],
    y=tenure_analysis[tenure_analysis['Churn Label'] == 'Yes']['Tenure Months'],
    name='Left the company (Churn)',
    marker_color='#EF4444', 
    text=tenure_analysis[tenure_analysis['Churn Label'] == 'Yes']['Tenure Months'].round(1),
    textposition='auto'
))

fig.update_layout(
    title_text="<b>Loyalty and Time (Average Tenure per Contract)</b>",
    xaxis_title="Contract Type",
    yaxis_title="Average Months of Loyalty",
    barmode='group', 
    template='plotly_white',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.show()


# The key difference: Look at the difference between a month-to-month contract and a two-year contract. In most data, you'll find that people who leave two-year contracts often stayed for a long time, meaning they were "disgruntled" in the end, unlike with month-to-month contracts where they leave while still "guests."
# 
# The strategy: This statistic will tell you exactly where you need to focus your retention efforts. If the average person who leaves a month leaves after 5 months, then the "renewal offer" should be sent to them in the fourth month!

# # Estimated Customer Lifetime Value (CLV)

# In[86]:


clv_data = df.groupby('Contract').agg({
    'Monthly Charges': 'mean',
    'Tenure Months': 'mean'
}).reset_index()

fig = go.Figure()

fig.add_trace(go.Bar(
    x=clv_data['Contract'],
    y=clv_data['Monthly Charges'],
    name='Avg Monthly Charges',
    marker_color='#3182CE',  
    text=clv_data['Monthly Charges'].round(2),
    textposition='auto'
))

fig.add_trace(go.Bar(
    x=clv_data['Contract'],
    y=clv_data['Tenure Months'],
    name='Avg Tenure Months',
    marker_color='#E53E3E', 
    text=clv_data['Tenure Months'].round(1),
    textposition='auto'
))

fig.update_layout(
    title_text="<b>Estimated Customer Lifetime Value (CLV) Components</b>",
    xaxis_title="Contract Type",
    yaxis_title="Values",
    barmode='group', 
    template='plotly_white',
    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
)

fig.show()


# Monthly contracts: High bills (long blue column) but very low loyalty (short red column). This is the danger zone.
# 
# Two-year contracts: Slightly lower bills, but huge loyalty. These are the ones carrying the company's CLV (Cost, Value, Value) up.

# # Fiber Optic Technology Switching Rate

# In[88]:


total_count = len(df)
tech_analysis = df.groupby(['Internet Service', 'Churn Label']).size().reset_index(name='count')
tech_analysis['percentage'] = (tech_analysis['count'] / total_count) * 100

fig = go.Figure()

fig.add_trace(go.Bar(
    y=tech_analysis[tech_analysis['Churn Label'] == 'No']['Internet Service'],
    x=tech_analysis[tech_analysis['Churn Label'] == 'No']['percentage'],
    name='Stay (No)',
    orientation='h',
    marker_color='#4A90E2',   
    text=tech_analysis[tech_analysis['Churn Label'] == 'No']['percentage'].round(2).astype(str) + '%',
    textposition='auto'
))

fig.add_trace(go.Bar(
    y=tech_analysis[tech_analysis['Churn Label'] == 'Yes']['Internet Service'],
    x=tech_analysis[tech_analysis['Churn Label'] == 'Yes']['percentage'],
    name='Churn (Yes)',
    orientation='h',
    marker_color='#C0504D', 
    text=tech_analysis[tech_analysis['Churn Label'] == 'Yes']['percentage'].round(2).astype(str) + '%',
    textposition='auto'
))

fig.update_layout(
    title_text="<b>Fiber Optic Technology Switching Rate</b>",
    xaxis_title="Percentage of Total Customers (%)",
    yaxis_title="Internet Service Type",
    barmode='group',
    template='plotly_white',
    height=500,
    legend=dict(title="Churn Label", orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02)
)

fig.show()


# The unfair comparison: DSL has many customers (27.86%), but very few have switched (6.52%).
# 
# The trap (Fiber Optic): Although fiber optic technology is faster and more expensive, its churn rate is alarming (18.42%).
# 
# The conclusion: This means there is a technical problem with the fiber optic service, or that its price is inflated for its quality. This is the first clue you should give engineers to fix the service.

# In[92]:


print("-" * 30)
print(f"✅ Data Cleaning Complete!")
print(f"🔹 Rows remaining: {len(df)}")
print(f"🔹 Missing values fixed: {df.isnull().sum().sum()}")
print(f"🔹 Duplicates removed: {df.duplicated().sum()}")
print("-" * 30)


# In[90]:


from IPython.display import display, Markdown

summary_text = f"""
# 🎯 Project Conclusion: Strategic Insights & Recommendations
---
## 📊 Executive Summary
* **Final Churn Rate:** <span style='color:red; font-weight:bold;'>{churn_rate:.2f}%</span>
* **Total Revenue Loss (Monthly):** <span style='color:red; font-weight:bold;'>${lost_revenue:,.2f}</span>
* **Average Customer Lifetime Value (CLV):** <span style='color:green; font-weight:bold;'>${avg_clv:,.2f}</span>

---
## 💡 Key Actionable Insights

1.  **The Fiber Optic Trap:** * بناءً على تحليل **Technology Switching Rate**، وجدنا إن عملاء الفايبر بيمشوا بمعدلات مقلقة. 
    * **التوصية:** مراجعة جودة الخدمة الفنية للفايبر فوراً وعمل استقصاء (Survey) للعملاء الحاليين.

2.  **Contract Strategy (CLT):**
    * لاحظنا إن العقود الشهرية (**Month-to-month**) هي المصدر الأساسي لنزيف العملاء.
    * **التوصية:** تقديم عروض "Loyalty Rewards" لتحويل العملاء لعقود سنوية لضمان استقرار الـ Revenue.

3.  **High-Value Retention:**
    * عندنا **{high_value_churn}** عميل من الفئة الذهبية مشيوا الشهر ده.
    * **التوصية:** تفعيل خط "VIP Support" للعملاء اللي فاتورتهم أعلى من **${arpu:.2f}** لتقليل احتمالية رحيلهم.

---
### *Analysis Completed by: Mostafa Abdelhamed*
*Data Analysis Project - 2026*
"""

display(Markdown(summary_text))



# In[93]:


print(f"✅ END ")

