# Olympic Performance Analyzer

This project analyzes historical Olympic athlete and medal data to find patterns in country's performance, medal trends and sport specialization. The goal of the project was to answer questions such as "which countries perform best overall", "which sports produce the most medals" and "which countries rely most on one specific sport".

## Project Overview 

I used Python, pandas, NumPy and Matplotlib to clean and analyze the Olympic data. 

This project includes: 
  - Cleaning and filtering Olympic athlete records
  - Removing duplicate medal records from team events
  - Ranking countries by total medals
  - Creating a weighted medal points system
  - Analyzing medal trends over time
  - Measuring country sport specialization
  - Saving processed datasets and chart outputs for future Streamlit dashboard

## Dataset 

The project uses two CSV files: 
  - `athlete_events.csv`
  - `noc_regions.csv`

The raw data is stored in: 
  - `data/raw/`

The processed data is stored in: 
  - `data/processed/`

## Data Cleaning 

The original dataset is athlete-based which means that team events can create duplicate medal rows. For example, one team medal may appear once for every athlete on that team. 

To avoid overcounting medals, I created a deduplicated medal dataset using columns such as year, sport, event, country code and medal type. 

This reduced the medal records from about 39,000+ athlete level medal rows to about 18,000+ unique medal results. 

## What I Analyzed 

The main questions that I explored were: 
  - Which countries have won the most Olympic medals?
  - How do rankings change when gold, silver and bronze medals are weighted differently?
  - Which sports have produced the most medals?
  - How have medal counts changed over time?
  - Which countries are most specialized in one sport?
  - What is each country's strongest Olympic sport?

## Custom Scorings 

### Medal Points 

I used a simple point system to give more weight to higher medal finishes: 
  - Gold = 3 points
  - Silver = 2 points
  - Bronze = 1 point

This gives a different way to look at the total medal count because countries with more gold medals score higher. 

### Sport Specialization Score

I created a specialization score to measure how much of a country's medal success comes from one sport. 
  - Specialization Score: Sport Medal Count / Total Country Medals

For example, if a country has 100 total medals and 60 came from Athletics, then its Athletics specialization score would be: 60 / 100 = 0.60. This means that 60% of that country's medals came from Athletics. In order to make the ranking more useful, I filtered out countries with less than 10 total medals. Countries with 1 or 2 medals can easily have a score of 1.0 which makes the results misleading. 

## Key Findings

The United States had the highest total medal count and medal points in the dataset. Other countries such as the Soviet Union, Germany, Great Britain, France and Italy also ranked near the top. 

Athletics showed up more often as the strongest sport for highly specialized countries. Countries such as Ethiopia, Jamaica, Kenya, Bahamas and Morocco, Trinidad and Tobago, Nigeria and Algeria all had Athletics as their top sport. 

The specialization analysis showed that total medals do not explain everything. Some countries may not have the highest medal totals overall but they can still be very strong in one specific sport.

## Project Structure

  - `data/raw/` - Original dataset files
  - `data/processed/` - Cleaned data and summary tables used for analysis and the dashboard
  - `notebooks/` - Jupyter notebook containing the full analysis
  - `outputs/charts/` - Saved chart images from the analysis
  - `requirements.txt` - Python libraries needed to run the project

## How to Run

  1. Install the required libraries: `pip install -r requirements.txt` 
  2. Open the notebook: `notebooks/olympics_analysis.ipynb` 
  3. Then run all cells from top to bottom. 

## Next Steps 
  - Build the Streamlit Dashboard
  - Add filters for country, sport, year range and medal type
  - Used processed CSV files inside the dashboard
  - Separate Summer and Winter Olympics for cleaner analysis
  - Add population data for fair country comparisons

