# DSPExport Tool

## Purpose

The `Export Mapped DSPs` tool is designed to retrieve Mapped DSPs (Demand Side Platforms) from INTERAct on a per-market basis. This script simplifies the process of extracting and organizing DSP data for further analysis or reporting.

## Usage

### *NOTE*

You may need to install uv. To do so, follow the instructions provided [here](https://docs.astral.sh/uv/getting-started/installation/).

1. **Setup**: Ensure you have the required dependencies installed. Refer to the `pyproject.toml` file for a list of necessary Python packages.
These may be installed using the command `uv pip install -r pyproject.toml`

2. **Execution**:
    - Run the script using Python:

      ```bash
      python export_mapped_dsps.py 
      ```

    - You will need to provide:
        - Bearer Authorization token
        - ISO Market code (two characters: e.g. US, DE, FR, etc.)

3. **Output**: The script will generate a CSV file containing the Mapped DSP data for the specified market(s). The output format and location can be customized in the script's settings.

## Notes

- Ensure you have the necessary permissions to access INTERAct and retrieve DSP data.
- For troubleshooting or additional help, refer to the comments within the script or contact the development team.

## License

This tool is intended for internal use only. Redistribution or modification without proper authorization is prohibited
