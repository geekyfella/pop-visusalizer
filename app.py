from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__, static_url_path='/static')

# Load the dataset
df = pd.read_csv('countries-table.csv')

# List of cca3s for the dropdown menu
country_codes = df['cca3'].unique()

@app.route('/')
def index():
    return render_template('index.html', countries=country_codes)

@app.route('/visualize', methods=['POST'])
def visualize():
    selected_countries = request.form.getlist('cca3')
    print(f"Selected countries: {selected_countries}")  # Debug statement

    if not selected_countries or len(selected_countries) < 3:
        return render_template('error.html', message="Please select at least three countries.")

    try:
        selected_data = df[df['cca3'].isin(selected_countries)]
        print(f"Selected data: {selected_data}")  # Debug statement

        # Create and save heatmap
        plt.figure(figsize=(10, 8))
        heatmap_data = selected_data.set_index('cca3')[['pop1980', 'pop2000', 'pop2010', 'pop2022', 'pop2023', 'pop2030', 'pop2050']]
        sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu")
        heatmap_path = os.path.join('static', 'heatmap.png')
        plt.savefig(heatmap_path)
        print(f"Heatmap saved to: {heatmap_path}")  # Debug statement
        plt.close()

        # Create and save bubble chart
        plt.figure(figsize=(10, 8))
        years = ['pop1980', 'pop2000', 'pop2010', 'pop2022', 'pop2023', 'pop2030', 'pop2050']
        bubble_data = selected_data.melt(id_vars='cca3', value_vars=years, var_name='Year', value_name='Population')
        plt.scatter(bubble_data['Year'], bubble_data['cca3'], s=bubble_data['Population'] / 1e6, alpha=0.5)
        plt.xlabel('Year')
        plt.ylabel('Country')
        plt.title('Population Bubble Chart')
        bubble_chart_path = os.path.join('static', 'bubble_chart.png')
        plt.savefig(bubble_chart_path)
        print(f"Bubble chart saved to: {bubble_chart_path}")  # Debug statement
        plt.close()

        # Create and save pie chart
        plt.figure(figsize=(10, 8))
        latest_year_data = selected_data[['cca3', 'pop2023']]
        plt.pie(latest_year_data['pop2023'], labels=latest_year_data['cca3'], autopct='%1.1f%%')
        plt.title('Population Distribution (2023)')
        pie_chart_path = os.path.join('static', 'pie_chart.png')
        plt.savefig(pie_chart_path)
        print(f"Pie chart saved to: {pie_chart_path}")  # Debug statement
        plt.close()

        # Create and save bar chart
        plt.figure(figsize=(10, 8))
        sns.barplot(x='Year', y='Population', hue='cca3', data=bubble_data)
        plt.xlabel('Year')
        plt.ylabel('Population')
        plt.title('Population Bar Chart')
        bar_chart_path = os.path.join('static', 'bar_chart.png')
        plt.savefig(bar_chart_path)
        print(f"Bar chart saved to: {bar_chart_path}")  # Debug statement
        plt.close()

        # Generate and save choropleth map
        choropleth_path = os.path.join('static', 'choropleth.html')
        # Assuming the code to generate the choropleth is here

        images = ['static/heatmap.png', 'static/bubble_chart.png', 'static/pie_chart.png', 'static/bar_chart.png', 'static/choropleth.html']
        print(f"Images: {images}")  # Debug statement

        return render_template('visualization.html', images=images)
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug statement
        return render_template('error.html', message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
