### README for Energia Lab

**Project Overview:**
Energia Lab focuses on the analysis and enhancement of energy efficiency. It integrates various tools and technologies to manage and analyze energy project data effectively.


**Key Components:**
- **Jupyter Notebooks**: For data manipulation and visualization.
- **Streamlit Apps**: Interactive web apps for visualizing energy efficiency data.
- **Data Processing Scripts**: Handling and preprocessing energy data.

**Technology Stack:**
- **Python**: Primary language for data processing.
- **Folium**: Used for geospatial data visualization.
- **Pandas**: For data manipulation.
- **Streamlit**: To create interactive web applications.
- **Linear Colormap**: For generating color scales in visualizations.

**Setup and Installation:**
- Ensure Python and required libraries (`folium`, `pandas`, `streamlit`, `streamlit_folium`) are installed.
- Clone the repository and navigate to the appropriate directories to run the notebooks or streamlit applications.

**Features:**
- **Data Visualization**: Utilize `folium` for mapping energy efficiency across different states with color-coded markers.
- **Interactive Tables**: Display processed data within the Streamlit app, enhancing user interaction and data readability.
- **Efficiency Metrics**: Calculation and display of energy efficiency scores, providing insights into the performance of energy projects.

**Usage:**
1. **Running Notebooks**: Open Jupyter notebooks to perform detailed data analysis.
2. **Launching Streamlit Apps**: Run Streamlit apps to interact with processed data and visualizations.

**Data Analysis Workflow:**
1. Load and clean data using pandas.
2. Map state data to geospatial coordinates.
3. Visualize data using `folium` with interactive color scales based on efficiency scores.
4. Integrate visualizations into Streamlit for interactive user experiences.

**App Streamlit:**
1. Clone project from github to WSL.
2. Install docker dependencies on WSL.
3. Create a container for the application .
4. Create service in GCP cloud run.
cloud run: https://energia-7g5gf6xo6q-uc.a.run.app
