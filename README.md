# Smgnr3000: Efficient Data Logging and Visualization for Homebrewers

![Smgnr3000](https://img.shields.io/badge/Smgnr3000-v1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-orange.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.0-red.svg)

## Overview

Smgnr3000 is a powerful parser designed to fetch and log runtime and temperature data from the Samogoner AE3000. This tool not only records data into CSV or PostgreSQL formats but also generates daily graphs for better visualization. The included PyQt5 GUI allows users to interactively plot the data, making it easier to analyze trends over time. Additionally, a "Test Panel" feature lets users manually send test commands for immediate feedback.

## Features

- **Data Fetching**: Periodically retrieves runtime and temperature data from the Samogoner AE3000.
- **Data Logging**: Stores data in CSV or PostgreSQL for easy access and analysis.
- **Graph Generation**: Automatically creates daily graphs for quick visualization of trends.
- **Interactive GUI**: A user-friendly PyQt5 interface for plotting data.
- **Test Panel**: Manually send commands to the device for testing and troubleshooting.

## Topics

This project covers a range of topics relevant to homebrewing and data analysis:

- **ESP8266**: The microcontroller used for wireless communication.
- **Ethanol**: The primary product being monitored.
- **Homebrew**: Focused on homebrewing enthusiasts.
- **HW-364A**: Hardware used in the setup.
- **Matplotlib**: The library for generating graphs.
- **Parser**: The core functionality of the application.
- **PostgreSQL**: The database used for data storage.
- **PyQt5**: The framework for the graphical user interface.
- **Python3**: The programming language used for development.
- **Vodka**: A common product of the homebrewing process.

## Getting Started

To get started with Smgnr3000, you will need to clone the repository and install the required dependencies.

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- PyQt5 5.15.0 or higher

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mizaela/Smgnr3000.git
   cd Smgnr3000
   ```

2. **Install Dependencies**:
   Use pip to install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   Ensure you have PostgreSQL installed and create a database for logging data.

4. **Configuration**:
   Edit the configuration file to set your database connection details and other parameters.

### Running the Application

You can run the application using the following command:
```bash
python main.py
```

### Download Releases

For the latest releases, visit the [Releases section](https://github.com/mizaela/Smgnr3000/releases). You can download the latest version and execute it to get started.

## Usage

### Data Logging

Once the application is running, it will automatically fetch data from the Samogoner AE3000 at set intervals. The data will be logged in the specified format (CSV or PostgreSQL).

### Viewing Graphs

The PyQt5 GUI allows you to view graphs of the logged data. You can select the date range and the type of data you want to visualize.

### Sending Test Commands

The Test Panel in the GUI allows you to manually send commands to the Samogoner AE3000. This feature is useful for testing and troubleshooting.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

### How to Contribute

1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the creators of the Samogoner AE3000 for their innovative design.
- Thanks to the contributors of the PyQt5 and Matplotlib libraries for their invaluable tools.

## Contact

For questions or support, please open an issue on GitHub or contact the repository owner.

## Additional Resources

For more information about the tools and technologies used in this project, consider checking out the following links:

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

For the latest updates, visit the [Releases section](https://github.com/mizaela/Smgnr3000/releases) and download the latest version. 

![Homebrewing](https://example.com/homebrewing-image.jpg) 

## FAQs

### What is the Samogoner AE3000?

The Samogoner AE3000 is a device used for monitoring and controlling the fermentation process in homebrewing. It provides real-time data on runtime and temperature.

### Can I use other databases?

Currently, the application supports PostgreSQL. Future versions may include support for other databases.

### Is there a mobile version of the GUI?

At this time, the GUI is designed for desktop use only. A mobile version may be considered in future updates.

### How often does the application fetch data?

The default interval for fetching data can be configured in the settings. The application is designed to run continuously and log data at regular intervals.

### Can I customize the graphs?

Yes, the PyQt5 GUI allows for some customization of the graphs, including the date range and types of data displayed.

### How do I report bugs?

If you encounter any bugs, please open an issue in the GitHub repository, providing as much detail as possible about the problem.

## Community

Join our community of homebrewers and developers! Share your experiences, ask questions, and collaborate on projects related to homebrewing and data logging.

![Community](https://example.com/community-image.jpg)

## Conclusion

Smgnr3000 is an essential tool for homebrewers looking to monitor and analyze their fermentation process. With its robust features and user-friendly interface, it simplifies the complexities of data logging and visualization. 

Explore the project, contribute, and enhance your homebrewing experience!