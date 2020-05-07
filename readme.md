# Simple Exercise Statistics

Simple data visualization for workout records via [Python 3](https://www.python.org/downloads/) and [Matplotlib](https://matplotlib.org/).

## Getting Started

Currently, three types of plots are supported:

1. 3D bar chart for daily repetition values;
2. 2D trend predictions for the 1st set repetition value and daily total repetition value;
3. 2D trend plot for daily workout time.

All resultant figures are output as .png files. Example figure outputs (with inverted color effect) can be seen in [this demo video](https://www.bilibili.com/video/BV19C4y1W7cZ/).

### Prerequisites

One would need to (1) install Python 3 with required libraries, and (2) store workout records in a csv file with the structure specified below.

### Data File Structure

As shown in the example data file `20200401_PullUps.csv`, the csv record file for workout data should have a header like:

```
"Date","Set 1","Set 2","Set 3", ... ,"Set N","Sum"
```

with each row being the results for one day. For function `plotDailyTimeSpent`, anther field `"WorkoutTime"` with the dat format `h:mm:ss` is needed.

### Project Structure

Key functions are wrapped in `./libs/exerciseStatistics.py`. An example on how to use them is provided in `./plotPullUpStatistics.py`. The data for the example is stored in `./20200401_PullUps.csv`.

## Examples

For easy modification and debugging of the key code set, one can run under `./libs`:

```
python exerciseStatistics.py
```

to see some test plots.

A more comprehensive example can be run under `.` via:

```
python plotPullUpStatistics.py
```

where all output figures will be stored in a new subdirectory `./Output`.

## Contact

* **Yaguang Zhang** | Email: yaguangz@outlook.com

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
