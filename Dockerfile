# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /1_energy_save

# Copy the current directory contents into the container at /app
COPY . ./

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable to control the Streamlit port
ENV STREAMLIT_SERVER_PORT=8501

# Run 1_energy_save.py when the container launches
CMD ["streamlit", "run", "1_energy_save.py", "--server.port=8501", "--server.address=0.0.0.0"]
