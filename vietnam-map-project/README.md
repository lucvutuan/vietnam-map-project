# Vietnam Map Project

This project reads coordinates from a text file and uses them to draw a map of Vietnam. It is structured to separate the main functionality and utility functions for better organization and maintainability.

## Project Structure

```
vietnam-map-project
├── src
│   ├── draw_map.py      # Main script for drawing the map
│   └── utils.py         # Utility functions for data handling
├── data
│   └── VIETNAM_COORDINATE.txt  # Coordinates data file
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd vietnam-map-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Ensure that the `VIETNAM_COORDINATE.txt` file in the `data` directory contains the coordinates in decimal format, with each point on a new line.

2. Run the main script to draw the map:
   ```
   python src/draw_map.py
   ```

## Dependencies

This project requires the following Python libraries:
- [matplotlib](https://matplotlib.org/) for data visualization
- [numpy](https://numpy.org/) for numerical operations

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.