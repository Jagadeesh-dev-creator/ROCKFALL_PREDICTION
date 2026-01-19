import pandas as pd
import numpy as np
from pathlib import Path


def merge_datasets():
    root = Path(__file__).resolve().parents[1]
    weather_path = root / 'dataset' / 'weather_forecast_data.csv'
    slope_path = root / 'dataset' / 'slope_stability_dataset.csv'
    rock_path = root / 'dataset' / 'rock_samples_Gecamines.csv'
    out_path = root / 'dataset' / 'merged_dataset.csv'

    weather = pd.read_csv(weather_path)
    slope = pd.read_csv(slope_path)
    rock = pd.read_csv(rock_path)

    weather = weather.rename(columns={
        'Temperature': 'temperature_c',
        'Humidity': 'humidity_pct',
        'Wind_Speed': 'wind_speed',
        'Cloud_Cover': 'cloud_cover_pct',
        'Pressure': 'pressure_hpa',
        'Rain': 'rain_raw'
    })
    weather['rain_flag'] = weather['rain_raw'].str.lower().str.strip().eq('rain').astype(int)

    slope = slope.rename(columns={
        'Unit Weight (kN/m³)': 'unit_weight_knm3',
        'Cohesion (kPa)': 'cohesion_kpa',
        'Internal Friction Angle (°)': 'friction_angle_deg',
        'Slope Angle (°)': 'slope_angle_deg',
        'Slope Height (m)': 'slope_height_m',
        'Pore Water Pressure Ratio': 'pore_water_pressure_ratio',
        'Reinforcement Type': 'reinforcement_type',
        'Reinforcement Numeric': 'reinforcement_numeric',
        'Factor of Safety (FS)': 'factor_of_safety'
    })

    n = len(weather)
    slope = slope.head(n)

    comp_series = np.resize(rock['CompressiveStrength'].values, n)
    comp_series = pd.Series(comp_series, name='compressive_strength_mpa')

    merged = pd.concat([
        weather[['temperature_c', 'humidity_pct', 'wind_speed', 'cloud_cover_pct', 'pressure_hpa', 'rain_flag']],
        slope[['slope_angle_deg', 'cohesion_kpa', 'friction_angle_deg', 'slope_height_m', 'unit_weight_knm3', 'pore_water_pressure_ratio', 'reinforcement_type', 'reinforcement_numeric', 'factor_of_safety']],
        comp_series
    ], axis=1)

    merged.to_csv(out_path, index=False)
    print(f"Merged rows: {len(merged)}")
    print(f"Saved to: {out_path}")
    print(merged.head())


if __name__ == '__main__':
    merge_datasets()
